"""
compute_payment_schedule.py

A python script to compute the mortgage, energy, and pension payments for a specified house cost and energy demand.

Richard Lyon
3 October 2022

"""
from dataclasses import dataclass

import pandas as pd

from pension_calculator.models import Energy, House, Mortgage, Pension, Person


@dataclass
class ScenarioParams:
    person_year_of_birth: int
    house_purchase_year: int
    house_purchase_cost: int
    house_passive_house_premium: float
    house_area_m2: float
    house_annual_heating_kwh_m2a: float
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
        house_kwh_m2a=p.house_annual_heating_kwh_m2a,
        house_area_m2=p.house_area_m2,
        first_year=p.house_purchase_year,
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
        first_year=p.house_purchase_year,
        last_year=person.yod,
    )
    annual_mortgage_payments = mortgage.annual_payments()["total"]
    annual_pension_payments = pension.annual_payments()

    df = pd.DataFrame(
        data={
            "energy": annual_energy_payments,
            "mortgage": annual_mortgage_payments,
            "pension": annual_pension_payments,
        },
        index=range(p.house_purchase_year, person.yod),
    )

    df = df.fillna(0).astype({"energy": "int", "mortgage": "int", "pension": "int"})

    return df
