"""A class that represents a pension."""

from dataclasses import dataclass
from typing import Optional

import numpy as np
import numpy_financial as npf
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

    target: Optional[float]
    growth_rate_pcnt: float
    start_year: int
    end_year: int

    def annual_payments(self) -> pd.DataFrame:
        """Compute the annual payments required to achieve the target, given a growth rate and saving period.

        Returns:
            A dataframe of annual payments and value. Each row is the total payment and current value for that year.
            The returned dataframe is inclusive of the first year and exclusive of the last i.e. 2010-2020 produces
            [2010, 2011, .... , 2019].
        """

        duration_years = self.end_year - self.start_year
        amount = (
            self.target
            * self.growth_rate_pcnt
            / (pow(1 + self.growth_rate_pcnt, duration_years) - 1)
        )

        value = npf.fv(
            self.growth_rate_pcnt, range(duration_years), 0, -amount
        ).cumsum()

        return pd.DataFrame(
            data={"payment": np.full(duration_years, amount), "value": value},
            index=range(self.start_year, self.end_year),
        )

    @property
    def annual_payment(self) -> float:
        """Compute the annual payment amount."""
        return self.annual_payments().iloc[0]
