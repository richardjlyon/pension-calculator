import numpy as np
import pandas as pd

from pension_calculator import ROOT, CONFIG
from pension_calculator.models import Person

PLOT_DIR = ROOT / "plot" / "figures"


def compute_energy_prices():
    """
    Generate an array of energy prices from minimum and maximum prices specified in a CONFIG file.
    Returns
    -------
    An array of energy prices
    """
    price_min = CONFIG.get("sensitivities").get("price_min")
    price_max = CONFIG.get("sensitivities").get("price_max")
    prices = np.arange(price_min, price_max, 0.05)
    return np.round(prices, 3)[::-1]


def compute_energy_growth_rates():
    """
    Generate an array of energy growth rates from minimum and maximum rates specified in a CONFIG file.
    Returns
    -------
    An array of growth rates
    """
    cagr_min = CONFIG.get("sensitivities").get("cagr_min")
    cagr_max = CONFIG.get("sensitivities").get("cagr_max")
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
    house_types = [house_type for house_type, _ in CONFIG.get("energy_use").items()]
    iterables = [house_types, energy_prices]
    return pd.MultiIndex.from_product(iterables, names=["house_type", "energy_price"])


def print_sanity_check(result_df, delta_df, house_size_m2, person: Person):

    print("\nSanity check:")
    print("======================")
    print(f"Year of birth      : {person.yob}")
    print(f"Year of retirement : {person.yob + CONFIG.get('basic').get('pension_age')}")
    print(f"Year of death      : {person.yod}")
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
