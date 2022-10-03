"""
mortgage.py

29 September 2022
"""
from dataclasses import dataclass


@dataclass
def MortgageDetails():
    amount: int
    interest_rate: float
    length_years: int


def calculate():
    pass


if __name__ == "__main__":
    details = MortgageDetails(amount)
    calculate()
