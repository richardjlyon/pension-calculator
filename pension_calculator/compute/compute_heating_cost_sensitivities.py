"""
compute_heating_cost_sensitivities.py

Compute difference and variation of heating energy cost to tariff and tariff growth rate for normal and passive house.
"""
from typing import Optional

import pandas as pd

from pension_calculator import CONFIG, CURRENT_YEAR
from pension_calculator.compute.utils import (
    compute_energy_growth_rates,
    compute_energy_prices,
    make_column_index,
)
from pension_calculator.models import Energy, Person


def compute_heating_cost_sensitivities(
    person: Person, house_area_m2: Optional[float] = None
) -> pd.DataFrame:
    """
    Compute the heating energy cost of an "average" house relative to a passive house for a range of
    energy prices and compound annual growth rates.

    The energy cost is computed from the energy intensity of the house and the area. Energy cost is inflated from the
    year the script is run until the year of death computed from the year of birth.

    Parameters
    ----------
    year_of_birth The year of birth to compute year of death from (default set from CONFIG file)
    house_area_m2 The size of the house in square metres (default set from CONFIG file)

    Returns
    -------
    A dataframe of energy costs
    """

    if house_area_m2 is None:
        house_area_m2 = CONFIG.get("basic").get("average_house_size_m2")

    energy_prices = compute_energy_prices()
    growth_rates = compute_energy_growth_rates()

    df = pd.DataFrame(index=growth_rates, columns=make_column_index(energy_prices))

    for house_type, kwh_m2 in CONFIG.get("energy_use").items():
        for energy_price in energy_prices:
            total_payments = []
            for growth_rate in growth_rates:

                energy = Energy(tariff=energy_price, cagr_pcnt=growth_rate)
                annual_payments = energy.annual_payments(
                    house_kwh_m2a=kwh_m2,
                    house_area_m2=house_area_m2,
                    first_year=CURRENT_YEAR,
                    last_year=person.yod,
                )
                total_payments.append(annual_payments.sum())

            df[house_type, energy_price] = total_payments

    return df
