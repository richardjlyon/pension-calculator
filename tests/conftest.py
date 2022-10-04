import pytest

from pension_calculator.compute.compute_payment_schedule import (
    ScenarioParams,
    compute_payment_schedule,
)
from pension_calculator.models import Mortgage, Pension
from pension_calculator.models.energy import Energy


@pytest.fixture
def energy():
    return Energy(tariff=0.1, cagr=0.05)


@pytest.fixture(scope="module")
def pension():
    return Pension(target=10000, growth_rate=0.1, start_year=2022, end_year=2032)


@pytest.fixture(scope="module")
def mortgage():
    return Mortgage(
        purchase_year=2022,
        purchase_price=350000,
        deposit_percent=0.1,
        interest_rate=0.0425,
        length_years=20,
    )


@pytest.fixture(scope="module")
def payment_schedule():
    params = ScenarioParams(
        person_year_of_birth=1965,
        house_purchase_year=2022,
        house_purchase_cost=350000 / 1.1,
        house_passive_house_premium=0.1,
        house_area_m2=100,
        house_annual_heating_kwh_m2a=100,
        mortgage_deposit_percent=0.1,
        mortgage_interest_rate=0.0425,
        mortgage_length_years=20,
        pension_growth_rate=0.01,
        energy_tariff=0.1,
        energy_cagr=0.05,
    )
    return compute_payment_schedule(params)
