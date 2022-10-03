import pytest

from pension_calculator.models.energy import Energy


@pytest.fixture
def energy():
    return Energy(tariff=0.1, cagr=0.1, year_of_retirement=2032, year_of_death=2052)
