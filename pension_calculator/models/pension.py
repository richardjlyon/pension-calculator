"""
pension.py

Richard Lyon
3 October 2022
"""
from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class Pension:
    """Represents a Pension."""

    target: float
    growth_rate: float
    start_year: int
    saving_length_years: int

    def annual_payments(self) -> pd.Series:
        """
        Compute the annual payments required to achieve the target given a growth rate and saving period.

        Returns
        -------
        A series of payments with year as the index.
        """

        amount = (
            self.target
            * self.growth_rate
            / (pow(1 + self.growth_rate, self.saving_length_years) - 1)
        )

        return pd.Series(
            data=np.full(self.saving_length_years, amount),
            index=range(self.start_year, self.start_year + self.saving_length_years),
        )
