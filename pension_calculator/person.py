"""
person.py

Richard Lyon
3 Oct 2022
"""

import datetime
from typing import Optional

import toml

from pension_calculator import ROOT

config = toml.load(f"{ROOT}/app.config.toml")


def compute_years_until_death(year_of_birth: Optional[int] = None) -> int:
    """
    Compute the number of years until death from the current year for a person's year of birth.

    Parameters
    ----------
    year_of_birth The year of birth

    Returns
    -------
    The number of years until death

    """
    if year_of_birth is None:
        year_of_birth = config.get("basic").get("year_of_birth")

    life_expectancy = config.get("basic").get("life_expectancy")
    current_year = datetime.date.today().year
    return life_expectancy - (current_year - year_of_birth) + 1
