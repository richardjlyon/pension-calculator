"""
graphy.py

Generate a graph of the cost of an "average" house relative to a passive house as a function of
energy price and compound annual growth rate/.
"""

import datetime
from typing import Optional

import toml

import numpy as np
import pandas as pd
import numpy_financial as npf
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
from pension_calculator import ROOT

PLOT_DIR = ROOT / "plots"

config = toml.load(f"{ROOT}/app.config.toml")


def compute_years_until_death(year_of_birth: Optional[int] = None) -> int:
    if year_of_birth is None:
        year_of_birth = config.get("basic").get("year_of_birth")

    life_expectancy = config.get("basic").get("life_expectancy")
    current_year = datetime.date.today().year
    return life_expectancy - (current_year - year_of_birth)


def compute_energy_prices():
    price_min = config.get("sensitivities").get("price_min")
    price_max = config.get("sensitivities").get("price_max")
    return np.arange(price_min, price_max, 0.05)


def compute_growth_rates():
    cagr_min = config.get("sensitivities").get("cagr_min")
    cagr_max = config.get("sensitivities").get("cagr_max")
    return np.arange(cagr_min, cagr_max + 0.01, 0.005)


def make_column_index(energy_prices) -> pd.MultiIndex:
    house_types = [house_type for house_type, _ in config.get("energy_use").items()]
    iterables = [house_types, energy_prices]
    return pd.MultiIndex.from_product(iterables, names=["house_type", "energy_price"])


def compute_annual_energy_cost(kwh_m2: float, house_size_m2: float, energy_price):
    kw_year = kwh_m2 * house_size_m2
    return kw_year * energy_price


def compute_relative_energy_cost(
    year_of_birth: Optional[int] = None, house_size_m2: Optional[float] = None
) -> pd.DataFrame:
    """
    Compute the heating energy cost of an "average" house relative to a passive house for a range of
    energy prices and compound annual growth rates.

    The energy cost is computed from the energy intensity of the house and the area. Energy cost is inflated from the
    year the script is run until the year of death computed from the year of birth.

    Parameters
    ----------
    year_of_birth The year of birth to compute year of death from (default set from config file)
    house_size_m2 The size of the house in square metres (default set from config file)

    Returns
    -------
    A dataframe of energy costs
    """

    if house_size_m2 is None:
        house_size_m2 = config.get("basic").get("average_house_size_m2")

    years_until_death = compute_years_until_death(year_of_birth)
    energy_prices = compute_energy_prices()
    growth_rates = compute_growth_rates()

    df = pd.DataFrame(index=growth_rates, columns=make_column_index(energy_prices))

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


def currency(x, pos):
    """Format y axis currency label as £xxK"""
    return "£{:1.0f}K".format(x * 1e-3)


if __name__ == "__main__":
    year_of_birth = 1965
    house_size_m2 = 67.8
    result_df = compute_relative_energy_cost(year_of_birth, house_size_m2)
    delta_df = result_df["average"] - result_df["passive"]

    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(currency)

    fig.set_size_inches(10, 6)
    fig.suptitle("Heating cost of an 'average' house relative to Passive House")

    delta_df.plot(ax=ax)

    plt.legend(
        title="Energy price (p/kWh)",
        labels=[round(col, 2) * 100 for col in delta_df.columns],
    )
    ax.set_xlabel("Energy price Compound Annual Growth Rate")

    text = f"Year of birth: {year_of_birth}\nHouse size: {house_size_m2}m2"
    at = AnchoredText(text, prop=dict(size=15), frameon=True, loc="upper center")
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)

    plt.grid(
        visible=True,
        which="major",
        axis="y",
        color="grey",
        linestyle="-",
        linewidth=0.5,
    )

    outfile = PLOT_DIR / "heating_cost_comparison.png"
    plt.savefig(outfile)

    plt.show()
