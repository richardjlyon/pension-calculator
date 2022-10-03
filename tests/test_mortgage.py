from pension_calculator.mortgage import Mortgage
from pytest import approx


def test_monthly_payment():
    mortgage = Mortgage(
        purchase_price=350000, deposit=0.1, interest_rate=0.0425, length_years=20
    )
    assert mortgage.monthly_payment() == approx(-1950.59, abs=0.01)


def test_annual_payments():
    mortgage = Mortgage(
        purchase_price=350000, deposit=0.1, interest_rate=0.0425, length_years=20
    )
    annual_payments = mortgage.annual_payments()
    expected_annual_payment = 12 * mortgage.monthly_payment()

    assert annual_payments["principal"].iloc[0] == approx(-10217.06)
    assert annual_payments["interest"].iloc[0] == approx(-13190.0)
    assert annual_payments["total"].iloc[0] == approx(expected_annual_payment)
