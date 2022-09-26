import datetime

import toml

import numpy as np
import pandas as pd
import numpy_financial as npf
from pension_calculator import ROOT

config = toml.load(f"{ROOT}/app.config.toml")

year_of_birth = config.get("basic").get("year_of_birth")
life_expectancy = config.get("basic").get("life_expectancy")
years = np.arange(year_of_birth, year_of_birth + life_expectancy + 1)

current_year = datetime.date.today().year
years_until_death = life_expectancy - (current_year - year_of_birth)

cagr_min = config.get("sensitivities").get("cagr_min")
cagr_max = config.get("sensitivities").get("cagr_max")
price_min = config.get("sensitivities").get("price_min")
price_max = config.get("sensitivities").get("price_max")

growth_rates = np.linspace(cagr_min, cagr_max, 11)
energy_prices = np.linspace(price_min, price_max, 16)


def make_column_index() -> pd.MultiIndex:
    house_types = [house_type for house_type, _ in config.get("energy_use").items()]
    iterables = [house_types, energy_prices]
    return pd.MultiIndex.from_product(iterables, names=["house_type", "energy_price"])


def compute_annual_energy_cost(kwh_m2: float, house_size_m2: float, energy_price):
    kw_year = kwh_m2 * house_size_m2
    return kw_year * energy_price


def compute(house_size_m2: float = None) -> pd.DataFrame:

    if house_size_m2 is None:
        house_size_m2 = config.get("basic").get("average_house_size_m2")

    df = pd.DataFrame(index=growth_rates, columns=make_column_index())

    for house_type, kwh_m2 in config.get("energy_use").items():

        for energy_price in energy_prices:

            annual_energy_cost = compute_annual_energy_cost(
                kwh_m2, house_size_m2, energy_price
            )
            total_costs = [
                round(
                    npf.fv(
                        growth_rate,
                        years_until_death,
                        -annual_energy_cost,
                        -annual_energy_cost,
                    )
                )
                for growth_rate in growth_rates
            ]

            df[house_type, energy_price] = total_costs

    return df


if __name__ == "__main__":
    result_df = compute()
    print(result_df)
