"""A class that represents a pension."""

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class Pension:
    """Represents a pension.

    Attributes:
        target: The target amount the pension must reach, in pounds.
        growth_rate: The assumed average annual growth rate over the duration of the pension e.g. '0.01'.
        start_year: The year that saving commences.
        end_year: The year that saving ends (exclusive).
    """

    target: float
    growth_rate: float
    start_year: int
    end_year: int

    def annual_payments(self) -> pd.Series:
        """Compute the annual payments required to achieve the target, given a growth rate and saving period.

        Returns:
            A Series of payments. Each row is the total payment for that year. The returned series is inclusive of the
            first year and exclusive of the last i.e. 2010-2020 produces [2010, 2011, .... , 2019]
        """

        # TODO: Convert to DataFrame and return compounded annual value.

        years = self.end_year - self.start_year
        amount = self.target * self.growth_rate / (pow(1 + self.growth_rate, years) - 1)
        return pd.Series(
            data=np.full(years, amount), index=range(self.start_year, self.end_year),
        )

    @property
    def annual_payment(self) -> float:
        """Compute the annual payment amount."""
        return self.annual_payments().iloc[0]
