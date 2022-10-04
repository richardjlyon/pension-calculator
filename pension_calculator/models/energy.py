"""
energy.py

Richard Lyon
3 October 2022
"""
from dataclasses import dataclass

import pandas as pd
import toml

from pension_calculator import ROOT

config = toml.load(f"{ROOT}/app.config.toml")


@dataclass
class Energy:
    """Represents an energy type. Computes cost time series."""

    tariff: float
    cagr: float

    def annual_energy_cost(self, house_kwh_m2a: float, house_area_m2: float):
        """
        Compute the annual energy cost of a house with the given area and heating energy demand.

        Parameters
        ----------
        house_kwh_m2a House area (kwh_m2a)
        house_area_m2 House size (m2)

        Returns
        -------
        The annual energy cost in pounds.

        """
        kw_year = house_kwh_m2a * house_area_m2
        return kw_year * self.tariff

    def annual_payments(
        self,
        house_kwh_m2a: float,
        house_area_m2: float,
        first_year: int,
        last_year: int,
    ) -> pd.Series:
        """
        Compute a time series of annual energy payments for a given house size and number of years.

        Parameters
        ----------
        house_kwh_m2a House heating energy demand (kwh_m2a)
        house_area_m2 House area (m2)
        first_year First year of energy payments
        last_year Last year of energy payments

        Returns
        -------
        A pandas Series of payments with year number as the index.

        """

        years = last_year - first_year + 1

        initial_payment = self.annual_energy_cost(
            house_kwh_m2a=house_kwh_m2a, house_area_m2=house_area_m2
        )
        payments = [
            initial_payment * pow(1 + self.cagr, period) for period in range(years)
        ]

        return pd.Series(data=payments, index=range(first_year, last_year + 1))

    def retirement_cost(
        self,
        house_kwh_m2a: float,
        house_area_m2: float,
        first_year: int,
        year_of_retirement: int,
        year_of_death: int,
    ) -> float:
        """
        Compute the total cost of house heating energy from retirement to death.

        Parameters
        ----------
        house_kwh_m2a House heating energy demand (kwh_m2a)
        house_area_m2 House area (m2)
        first_year First year of energy payments
        year_of_retirement Year of retirement
        year_of_death Year of death

        Returns
        -------
        The total cost of house heating energy from retirement to death.

        """
        annual_payments = self.annual_payments(
            house_kwh_m2a=house_kwh_m2a,
            house_area_m2=house_area_m2,
            first_year=first_year,
            last_year=year_of_death,
        )
        retirement_annual_payments = annual_payments.loc[
            year_of_retirement:year_of_death
        ]

        return retirement_annual_payments.sum()
