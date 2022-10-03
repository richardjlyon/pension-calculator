"""
mortgage.py

29 September 2022
"""
from dataclasses import dataclass

import pandas as pd
import numpy_financial as npf
import numpy as np
from math import isclose


@dataclass
class Mortgage:
    """Represents a mortgage."""

    purchase_price: float
    deposit: float
    interest_rate: float
    length_years: int

    def monthly_payment(self) -> float:
        """Compute the monthly payment."""
        loan_amount = self.purchase_price * (1 - self.deposit)
        return npf.pmt(
            rate=self.interest_rate / 12, nper=self.length_years * 12, pv=loan_amount
        )

    def annual_payments(self) -> pd.DataFrame:
        """Compute a time series of annual mortgage payments."""
        loan_amount = self.purchase_price * (1 - self.deposit)
        periods = np.arange(self.length_years * 12 + 1)

        principal_payment = npf.ppmt(
            rate=self.interest_rate / 12,
            per=periods,
            nper=self.length_years * 12,
            pv=loan_amount,
        )[
            1:
        ]  # don't understand why we need [1:], but element [0], and sum() is wrong

        interest_payment = npf.ipmt(
            rate=self.interest_rate / 12,
            per=periods,
            nper=self.length_years * 12,
            pv=loan_amount,
        )[1:]

        # downsample from monthly to annual and sense check
        interest_payment = interest_payment.reshape(-1, 12).sum(axis=1)
        principal_payment = principal_payment.reshape(-1, 12).sum(axis=1)
        assert isclose(principal_payment.sum(), -loan_amount, rel_tol=0.01)

        return pd.DataFrame(
            data={
                "principal": principal_payment,
                "interest": interest_payment,
                "total": principal_payment + interest_payment,
            },
            index=np.arange(self.length_years),
        )