from pension_calculator.graph import compute_total_payments
from pytest import approx


def test_compute_fv():
    growth_rate = 0.05
    periods = 31
    payment = 500

    assert compute_total_payments(growth_rate, periods, payment) == approx(35380, abs=1)
