from pytest import approx

from pension_calculator.models.pension import Pension


def test_annual_payments():

    pension = Pension(target=10000, growth_rate=0.1, saving_length_years=10)
    assert pension.annual_payments() == approx(627.45, abs=0.01)
