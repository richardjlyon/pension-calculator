import pytest

from pension_calculator.compute.compute_payment_schedule import (
    ScenarioParams,
    compute_payment_schedule,
)
from pension_calculator.models import House, Mortgage, Pension, Person, Energy


@pytest.fixture
def energy():
    return Energy(tariff=0.1, cagr_pcnt=0.05)


@pytest.fixture(scope="module")
def pension():
    return Pension(target=10000, growth_rate_pcnt=0.1, start_year=2022, end_year=2032)


@pytest.fixture(scope="module")
def mortgage():
    return Mortgage(
        purchase_year=2022,
        purchase_price=350000,
        deposit_pcnt=0.1,
        interest_rate_pcnt=0.0425,
        length_years=20,
    )


@pytest.fixture(scope="module")
def payment_schedule():
    params = ScenarioParams(
        Person(1997),
        House(
            purchase_year=2022,
            purchase_cost=350000 / 1.1,
            passive_house_premium_pcnt=0.1,
            area_m2=100,
            annual_heating_kwh_m2a=100,
        ),
        Mortgage(
            purchase_year=2022,
            purchase_price=350000,
            deposit_pcnt=0.1,
            interest_rate_pcnt=0.0425,
            length_years=20,
        ),
        Pension(target=None, growth_rate_pcnt=0.01, start_year=1997, end_year=2030),
        Energy(tariff=0.1, cagr_pcnt=0.05),
    )
    return compute_payment_schedule(params)
