"""
energy.py

Richard Lyon
3 October 2022
"""

import pandas as pd
import toml

from pension_calculator import ROOT

config = toml.load(f"{ROOT}/app.config.toml")


class Energy:
    """Represents an energy type. Computes cost time series."""

    def __init__(self, tariff: float, cagr: float = 0, energy_type: str = None):
        """
        Initialise an Energy object

        Parameters
        ----------
        energy_type The type of energy e.g. "electricity"
        tariff Energy price (£/kWh)
        cagr Compound Annual Growth Rate percentage e.g. 0.1
        """
        self.tariff: float = tariff
        self.cagr: float = cagr
        self.energy_type: str = energy_type  #

    def annual_energy_cost(self, kwh_m2: float, house_size_m2: float):
        """
        Compute the annual energy cost of a house with the given area and heating energy demand.

        Parameters
        ----------
        kwh_m2 House area
        house_size_m2 House size (m2)

        Returns
        -------
        The annual energy cost in pounds.

        """
        kw_year = kwh_m2 * house_size_m2
        return kw_year * self.tariff

    def annual_payments(
        self, years: int, kwh_m2: float, house_size_m2: float
    ) -> pd.Series:
        """
        Compute a time series of annual energy payments for a given house size and number of years.

        Parameters
        ----------
        years The number of years to compute
        house_size_m2 The size of the house in square meters

        Returns
        -------
        A dataframe containing the annual payments time series.

        """

        initial_payment = self.annual_energy_cost(
            kwh_m2=kwh_m2, house_size_m2=house_size_m2
        )
        payments = [
            initial_payment * pow(1 + self.cagr, period) for period in range(years)
        ]

        return pd.Series(data=payments, index=range(years))
