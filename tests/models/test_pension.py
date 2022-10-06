import numpy_financial as npf
from pytest import approx


def test_annual_payment(pension):
    # given a pension with a compound interest rate, duration, and target amount
    # when I calculate the annual saving payment
    # then it produces the target amount
    nper = pension.end_year - pension.start_year
    actual_fv = npf.fv(pension.growth_rate_pcnt, nper, -pension.annual_payment, 0)
    assert actual_fv == approx(pension.target)


def test_annual_payments(pension):
    payments = pension.annual_payments()
    assert len(payments) == 10
    assert payments["value"].iloc[-1] == approx(10000)
