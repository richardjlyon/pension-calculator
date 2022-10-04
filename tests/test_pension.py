from pytest import approx

from pension_calculator.models.pension import Pension


def test_annual_payments():

    pension = Pension(
        target=10000, growth_rate=0.1, start_year=2022, saving_length_years=10
    )
    assert pension.annual_payments().loc[2022] == approx(627.45, abs=0.01)
