"""
mortgage.py

29 September 2022
"""
from dataclasses import dataclass

import pandas as pd
import numpy_financial as npf
import numpy as np
from math import isclose


def compute_loan_amount(purchase_price: float, deposit_percent: float) -> float:
    """
    Compute the loan amount, given a purchase price and deposit.

    Parameters
    ----------
    purchase_price Purchase price
    deposit_percent Deposit (%)

    Returns
    -------
    Loan amount.

    """
    return purchase_price * (1 - deposit_percent)


@dataclass
class Mortgage:
    """Represents a mortgage."""

    purchase_year: int
    purchase_price: float
    deposit_percent: float
    interest_rate: float
    length_years: int

    def monthly_payment(self) -> float:
        """
        Compute the monthly payment.

        Returns
        -------
        The monthly payment in pounds.
        """
        loan_amount = compute_loan_amount(self.purchase_price, self.deposit_percent)
        return -npf.pmt(
            rate=self.interest_rate / 12, nper=self.length_years * 12, pv=loan_amount
        )

    def annual_payments(self) -> pd.DataFrame:
        """
        Compute a time series of annual mortgage payments.

        Returns
        -------
        A dataframe of principal, interest, and total payments with year as the index.
        """
        loan_amount = compute_loan_amount(self.purchase_price, self.deposit_percent)
        periods = np.arange(self.length_years * 12 + 1)

        principal_payment = -npf.ppmt(
            rate=self.interest_rate / 12,
            per=periods,
            nper=self.length_years * 12,
            pv=loan_amount,
        )[
            1:
        ]  # don't understand why we need [1:], but element [0], and therefore sum(), is wrong

        interest_payment = -npf.ipmt(
            rate=self.interest_rate / 12,
            per=periods,
            nper=self.length_years * 12,
            pv=loan_amount,
        )[
            1:
        ]  # don't understand why we need [1:], but element [0], and therefore sum(), is wrong

        # down sample from monthly to annual and sense check
        interest_payment = interest_payment.reshape(-1, 12).sum(axis=1)
        principal_payment = principal_payment.reshape(-1, 12).sum(axis=1)
        assert isclose(principal_payment.sum(), loan_amount, rel_tol=0.01)

        df = pd.DataFrame(
            data={
                "principal": principal_payment,
                "interest": interest_payment,
                "total": principal_payment + interest_payment,
            },
            index=range(self.purchase_year, self.purchase_year + self.length_years),
        )

        return df

    @property
    def final_year(self) -> int:
        """Return the final payment year."""
        return self.purchase_year + self.length_years - 1
