from pension_calculator.models.mortgage import Mortgage
from pytest import approx


def test_monthly_payment(mortgage):
    # given a mortgage
    # when I check the computed monthly payment
    # it corresponds to the number calculated in quality-control/mortgage.numbers
    assert mortgage.monthly_payment() == approx(1950.59, abs=0.01)


def test_annual_payments(mortgage):
    annual_payments = mortgage.annual_payments()
    expected_annual_payment = 12 * mortgage.monthly_payment()

    assert annual_payments["principal"].iloc[0] == approx(10217.06)
    assert annual_payments["interest"].iloc[0] == approx(13190.0)
    assert annual_payments["total"].iloc[0] == approx(expected_annual_payment)


def test_final_year(mortgage):
    # given a mortgage
    # when I get the final payment year
    # then it's correct
    assert mortgage.final_year == 2041
