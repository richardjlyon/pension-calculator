import pytest

from pension_calculator.models.energy import Energy


@pytest.fixture
def energy():
    return Energy(tariff=0.05, cagr=0.05)
