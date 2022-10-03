"""
pension.py

Richard Lyon
3 October 2022
"""
from dataclasses import dataclass


@dataclass
class Pension:
    """Represents a Pension."""

    target: float
    growth_rate: float
    saving_length_years: int

    def annual_payments(self) -> float:
        """Compute the annual payment required to achieve the target given a growth rate and saving period."""
        return (
            self.target
            * self.growth_rate
            / (pow(1 + self.growth_rate, self.saving_length_years) - 1)
        )
