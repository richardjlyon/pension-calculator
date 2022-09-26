"""
calculate.py

Calculate a pension profile.
"""

import toml
import numpy as np
import numpy_financial as npf
import pandas as pd
import datetime
from matplotlib import pyplot as plt

config = toml.load("app.config.toml")

year_of_birth = config.get("basic").get("year_of_birth")
current_year = datetime.date.today().year
life_expectancy = config.get("basic").get("life_expectancy")
years_until_death = life_expectancy - (current_year - year_of_birth)
years = np.arange(year_of_birth, year_of_birth + life_expectancy + 1)

average_house_size_m2 = config.get("basic").get("average_house_size_m2")
variable_unit_cost_gas = config.get("basic").get("variable_unit_cost_gas")
variable_unit_cost_elec = config.get("basic").get("variable_unit_cost_electricity")
cagr_gas = config.get("CAGR").get("gas")
cagr_elec = config.get("CAGR").get("electricity")


def label_from_house_and_power(type: str, kwh_m2: int) -> str:
    """Make a label from the type and power"""
    return f"{type} ({kwh_m2} kwh/m2)"


def make_column_index() -> pd.MultiIndex:
    """Make a multi-index for the results dataframe from house and energy type."""

    house_types = [
        label_from_house_and_power(house_type, kwh_m2)
        for house_type, kwh_m2 in config.get("energy_use").items()
    ]
    energy_types = ["gas", "electricity", "total"]
    iterables = [house_types, energy_types]
    return pd.MultiIndex.from_product(iterables, names=["house_type", "energy_type"])


def compute_costs() -> pd.DataFrame:
    """Compute energy costs from house and energy type."""

    # construct result dataframe
    year_index = np.arange(current_year, current_year + years_until_death)
    column_index = make_column_index()
    result_df = pd.DataFrame(index=year_index, columns=column_index)

    # compute annual energy costs for each house type and populate dataframe
    for house_type, kwh_m2 in config.get("energy_use").items():
        kw_year = kwh_m2 * average_house_size_m2
        cost_gas_year = kw_year * variable_unit_cost_gas
        cost_elec_year = kw_year * variable_unit_cost_elec

        gas_annual = npf.fv(
            cagr_gas, np.arange(years_until_death), -cost_gas_year, -cost_gas_year
        )
        electricity_annual = npf.fv(
            cagr_elec, np.arange(years_until_death), -cost_elec_year, -cost_elec_year,
        )

        label = label_from_house_and_power(house_type, kwh_m2)
        result_df[label, "gas"] = gas_annual
        result_df[label, "electricity"] = electricity_annual
        result_df[label, "total"] = gas_annual + electricity_annual

    return result_df


if __name__ == "__main__":
    df = compute_costs()
    print(df)
    df["leaky (300 kwh/m2)", "gas"].plot()
    plt.show()
