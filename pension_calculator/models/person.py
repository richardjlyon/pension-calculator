"""A class that represents a person."""

from dataclasses import dataclass

from pension_calculator import CONFIG

pension_age = CONFIG.get("basic").get("pension_age")
life_expectancy = CONFIG.get("basic").get("life_expectancy")


@dataclass
class Person:
    """Represents a person and dates of birth, retirement, and death.

    Attributes:
        yob: Year of birth.
    """

    yob: int

    @property
    def yor(self):
        """Year of retirement."""
        return self.yob + pension_age

    @property
    def yod(self):
        """Year of death."""
        return self.yob + life_expectancy
