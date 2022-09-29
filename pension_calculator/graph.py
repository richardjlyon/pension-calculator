"""
graphy.py

Generate a graph of the cost of an "average" house relative to a passive house as a function of
energy price and compound annual growth rate/.
"""

import datetime
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import toml
from matplotlib.offsetbox import AnchoredText

from pension_calculator import ROOT

PLOT_DIR = ROOT / "plots"

config = toml.load(f"{ROOT}/app.config.toml")


def compute_years_until_death(year_of_birth: Optional[int] = None) -> int:
    if year_of_birth is None:
        year_of_birth = config.get("basic").get("year_of_birth")

    life_expectancy = config.get("basic").get("life_expectancy")
    current_year = datetime.date.today().year
    return life_expectancy - (current_year - year_of_birth) + 1


def compute_energy_prices():
    price_min = config.get("sensitivities").get("price_min")
    price_max = config.get("sensitivities").get("price_max")
    prices = np.arange(price_min, price_max, 0.05)
    return np.round(prices, 3)


def compute_growth_rates():
    cagr_min = config.get("sensitivities").get("cagr_min")
    cagr_max = config.get("sensitivities").get("cagr_max")
    rates = np.arange(cagr_min, cagr_max + 0.001, 0.005)
    return np.round(rates, 3)


def make_column_index(energy_prices) -> pd.MultiIndex:
    house_types = [house_type for house_type, _ in config.get("energy_use").items()]
    iterables = [house_types, energy_prices]
    return pd.MultiIndex.from_product(iterables, names=["house_type", "energy_price"])


def compute_annual_energy_cost(kwh_m2: float, house_size_m2: float, energy_price):
    kw_year = kwh_m2 * house_size_m2
    return kw_year * energy_price


def compute_total_payments(
    growth_rate: float, years: int, initial_payment: float
) -> float:
    """
    Compute the total payment arising from an annual payment increasing at
    a defined rate for a defined number of years.

    Parameters
    ----------
    growth_rate Compound annual growth rate
    years Number of years payments are made
    initial_payment The payment in the first year

    Returns
    -------
    The total amount paid
    """
    total = initial_payment
    new_payment = total
    for i in range(years - 1):
        new_payment = new_payment * (1 + growth_rate)
        total += new_payment
    return total


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
                compute_total_payments(
                    growth_rate, years_until_death, annual_energy_cost
                )
                for growth_rate in growth_rates
            ]

            df[house_type, energy_price] = total_costs

    return df


def currency(x, pos):
    """Format y axis currency label as £xxK"""
    if x >= 1e6:
        return "£{:1.1f}M".format(x * 1e-6)
    else:
        return "£{:1.0f}K".format(x * 1e-3)


def print_sanity_check(
    result_df, delta_df, year_of_birth, year_of_death, house_size_m2
):

    print("\nSanity check:")
    print("======================")
    print(f"Year of birth      : {year_of_birth}")
    print(
        f"Year of retirement : {year_of_birth + config.get('basic').get('pension_age')}"
    )
    print(f"Year of death      : {year_of_death}")
    print(f"House size         : {house_size_m2}m2\n")

    samples = [
        {"CAGR": 0.05, "price": 0.05},
        {"CAGR": 0.10, "price": 0.05},
        {"CAGR": 0.05, "price": 0.20},
        {"CAGR": 0.10, "price": 0.20},
    ]

    for sample in samples:
        cagr = sample["CAGR"]
        price = sample["price"]
        print(
            f"price: {price:.2f} |  CAGR: {cagr:.2f} | average: {round(result_df['average', price][cagr]):>7} | passive: {round(result_df['passive', price][cagr]):>7} | difference: {round(delta_df[price][cagr]):>7}"
        )

    return


if __name__ == "__main__":

    year_of_birth = 1955
    year_of_death = year_of_birth + config.get("basic").get("life_expectancy")
    current_year = datetime.date.today().year
    house_size_m2 = 100

    result_df = compute_relative_energy_cost(year_of_birth, house_size_m2)
    delta_df = result_df["average"] - result_df["passive"]

    print_sanity_check(result_df, delta_df, year_of_birth, year_of_death, house_size_m2)

    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(currency)

    width_inches = 10
    height_inches = width_inches * 9 / 16
    fig.set_size_inches(width_inches, height_inches)
    fig.suptitle(
        f"Additional heating energy cost of an 'average' house relative to Passive House ({current_year}-{year_of_death})"
    )

    delta_df.plot(ax=ax)

    plt.legend(
        title="Energy variable unit cost (p/kWh)",
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

    outfile = PLOT_DIR / f"heating_cost_comparison_{year_of_birth}_{house_size_m2}.png"
    plt.savefig(outfile)

    plt.show()

    print(f"\nSaved file to {outfile}")
