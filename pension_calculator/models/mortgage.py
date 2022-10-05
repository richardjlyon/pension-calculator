"""Class and functions for handling mortgages.

Classes:
    Mortgage: A mortgage

Functions:
    compute_loan_amount: Compute the loan amount, given a purchase price and deposit.
"""

from dataclasses import dataclass
from math import isclose

import numpy as np
import numpy_financial as npf
import pandas as pd


@dataclass
class Mortgage:
    """A mortgage.

    Attributes:
        purchase_year: The year of purchase
        purchase_price: The purchase price
        deposit_percent: The deposit, expressed as a percentage of purchase price e.g. '0.1'
        interest_rate: The interest rate, expressed as a percentage e.g. '0.05'
        length_years: The length of the mortgage, in years.
    """

    purchase_year: int
    purchase_price: float
    deposit_percent: float
    interest_rate: float
    length_years: int

    def monthly_payment(self) -> float:
        """Compute the monthly payment.

        Returns:
            The monthly payment in pounds.
        """
        loan_amount = compute_loan_amount(self.purchase_price, self.deposit_percent)
        return -npf.pmt(
            rate=self.interest_rate / 12, nper=self.length_years * 12, pv=loan_amount
        )

    def annual_payments(self) -> pd.DataFrame:
        """Compute a time series of annual mortgage payments.

        Payments are compounded monthly and then resampled to compute the annual payment.

        Returns:
            A dataframe of principal, interest, and total payments.
            Each row represents the total payment for a year.
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
        ]  # FIXME: I don't understand why we need [1:], but element [0], and therefore sum(), is wrong.

        interest_payment = -npf.ipmt(
            rate=self.interest_rate / 12,
            per=periods,
            nper=self.length_years * 12,
            pv=loan_amount,
        )[
            1:
        ]  # FIXME: I don't understand why we need [1:], but element [0], and therefore sum(), is wrong.

        # Down sample from monthly to annual and sense check.

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


def compute_loan_amount(purchase_price: float, deposit_percent: float) -> float:
    """Compute the loan amount, given a purchase price and deposit.

    Args:
        purchase_price: Purchase price, in pounds.
        deposit_percent: Deposit (%) e.g. '0.01'

    Returns:
        The loan amount.
    """

    return purchase_price * (1 - deposit_percent)
