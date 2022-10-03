"""
energy.py

Richard Lyon
3 October 2022
"""

from typing import Optional


import numpy as np
import pandas as pd
import toml

from pension_calculator import ROOT
from pension_calculator.utils import compute_total_payments

config = toml.load(f"{ROOT}/app.config.toml")


def compute_annual_energy_cost(kwh_m2: float, house_size_m2: float, energy_price):
    """
    Compute the annual energy cost of a house with the given area and heating energy demand.

    Parameters
    ----------
    kwh_m2 House area
    house_size_m2 House size (m2)
    energy_price Energy price (p/kWh)

    Returns
    -------
    The annual energy cost in pounds.

    """
    kw_year = kwh_m2 * house_size_m2
    return kw_year * energy_price


def compute_energy_prices():
    """
    Generate an array of energy prices from minimum and maximum prices specified in a config file.
    Returns
    -------
    An array of energy prices
    """
    price_min = config.get("sensitivities").get("price_min")
    price_max = config.get("sensitivities").get("price_max")
    prices = np.arange(price_min, price_max, 0.05)
    return np.round(prices, 3)[::-1]


def compute_energy_growth_rates():
    """
    Generate an array of energy growth rates from minimum and maximum rates specified in a config file.
    Returns
    -------
    An array of growth rates
    """
    cagr_min = config.get("sensitivities").get("cagr_min")
    cagr_max = config.get("sensitivities").get("cagr_max")
    rates = np.arange(cagr_min, cagr_max + 0.001, 0.005)
    return np.round(rates, 3)


def make_column_index(energy_prices) -> pd.MultiIndex:
    """
    Create the multi-index for a dataframe of energy prices

    Parameters
    ----------
    energy_prices An array of energy prices

    Returns
    -------
    A multi-index ["house type", energy_price]

    """
    house_types = [house_type for house_type, _ in config.get("energy_use").items()]
    iterables = [house_types, energy_prices]
    return pd.MultiIndex.from_product(iterables, names=["house_type", "energy_price"])


def compute_relative_energy_cost(
    years_until_death: int, house_size_m2: Optional[float] = None
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

    energy_prices = compute_energy_prices()
    growth_rates = compute_energy_growth_rates()

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
