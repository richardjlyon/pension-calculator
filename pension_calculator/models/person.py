"""
person.py

Richard Lyon
3 Oct 2022
"""

import datetime
from dataclasses import dataclass

import toml

from pension_calculator import ROOT

config = toml.load(f"{ROOT}/app.config.toml")
pension_age = config.get("basic").get("pension_age")
life_expectancy = config.get("basic").get("life_expectancy")


@dataclass
class Person:
    """Represents a person who owns a house and a pension."""

    yob: int

    @property
    def yor(self):
        return self.yob + pension_age

    @property
    def yod(self):
        return self.yob + life_expectancy

    def years_until_death(self) -> int:
        """
        Compute the number of years until death from the current year for a person's year of birth.

        Parameters
        ----------
        year_of_birth The year of birth

        Returns
        -------
        The number of years until death

        """
        current_year = datetime.date.today().year
        return life_expectancy - (current_year - self.yob) + 1
