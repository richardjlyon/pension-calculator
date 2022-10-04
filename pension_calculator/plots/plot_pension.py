"""
plot_pension.py

A script to generate plots that illustrate the difference in mortgage, energy, and pension payments between ordinary
and passive houses. 
"""
import datetime
from dataclasses import dataclass

import pandas as pd

import matplotlib.pyplot as plt

from pension_calculator.models.energy import Energy
from pension_calculator.models.house import House
from pension_calculator.models.mortgage import Mortgage
from pension_calculator.models.pension import Pension
from pension_calculator.models.person import Person


@dataclass
class ScenarioParams:
    house_annual_heating_kwh_m2a: float
    house_area_m2: float
    house_purchase_cost: int
    house_purchase_year: int
    house_passive_house_premium: float
    person_year_of_birth: int
    mortgage_deposit: int
    mortgage_interest_rate: float
    mortgage_length_years: int
    pension_growth_rate: float
    energy_tariff: float
    energy_cagr: float


def compute_data(p: ScenarioParams):

    person = Person(yob=p.person_year_of_birth)

    house = House(
        purchase_year=p.house_purchase_year,
        purchase_cost=p.house_purchase_cost,
        passive_house_premium=p.house_passive_house_premium,
        area_m2=p.house_area_m2,
        annual_heating_kwh_m2a=p.house_annual_heating_kwh_m2a,
    )

    mortgage = Mortgage(
        purchase_year=p.house_purchase_year,
        purchase_price=house.total_cost(),
        deposit=p.mortgage_deposit,
        interest_rate=p.mortgage_interest_rate,
        length_years=p.mortgage_length_years,
    )

    energy = Energy(tariff=p.energy_tariff, cagr=p.energy_cagr)

    retirement_energy_cost = energy.retirement_cost(
        kwh_m2=p.house_annual_heating_kwh_m2a,
        house_size_m2=p.house_area_m2,
        starting_year=p.house_purchase_year,
        year_of_retirement=person.yor,
        year_of_death=person.yod,
    )

    saving_length_years = person.yor - p.house_purchase_year

    pension = Pension(
        target=retirement_energy_cost,
        growth_rate=p.pension_growth_rate,
        start_year=p.house_purchase_year,
        saving_length_years=saving_length_years,
    )

    annual_energy_payments = energy.annual_payments(
        house_kwh_m2a=p.house_annual_heating_kwh_m2a,
        house_area_m2=p.house_area_m2,
        starting_year=p.house_purchase_year,
        year_of_death=person.yod,
    )
    annual_mortgage_payments = mortgage.annual_payments()["total"]
    annual_pension_payments = pension.annual_payments()

    return pd.DataFrame(
        data={
            "energy_payments": annual_energy_payments,
            "mortgage_payments": annual_mortgage_payments,
            "pension_payments": annual_pension_payments,
        },
        index=range(p.house_purchase_year, person.yod),
    )


if __name__ == "__main__":
    params = ScenarioParams(
        house_annual_heating_kwh_m2a=100,
        house_area_m2=100,
        house_purchase_cost=100000,
        house_purchase_year=2022,
        house_passive_house_premium=0.1,
        person_year_of_birth=1965,
        mortgage_deposit=0,
        mortgage_interest_rate=0.06,
        mortgage_length_years=20,
        pension_growth_rate=0.01,
        energy_tariff=0.1,
        energy_cagr=0.05,
    )
    data_df = compute_data(params)

    print(data_df)

    data_df.plot()
    plt.show()
