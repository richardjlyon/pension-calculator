from pytest import approx

from pension_calculator.utils import compute_total_payments


def test_compute_total_payments():
    growth_rate = 0.05
    periods = 31
    payment = 500

    assert compute_total_payments(growth_rate, periods, payment) == approx(35380, abs=1)
