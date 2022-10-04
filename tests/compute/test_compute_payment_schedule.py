from pytest import approx

from pension_calculator.compute.compute_payment_schedule import (
    ScenarioParams,
    compute_payment_schedule,
)


def test_mortgage_payments(payment_schedule):
    # given a house with a given purchase cost, premium, and year
    # when I calculate the mortgage payments
    actual_total_mortgage_payment = payment_schedule["mortgage"].sum()

    # they are as expected
    expected_total_mortgage_payment = 468141  # from quality-control/mortgage.numbers

    assert actual_total_mortgage_payment == approx(
        expected_total_mortgage_payment, abs=1
    )


def test_total_heating_costs(payment_schedule):
    # given a house with a given heat load and area, and cost tariff and growth
    # when I calculate the energy payments
    actual_total_energy_cost = payment_schedule["energy"].sum()

    # they are as expected
    expected_total_energy_cost = 70761  # from quality-control/energy.numbers
    assert actual_total_energy_cost == approx(expected_total_energy_cost, abs=1)


def test_retirement_heating_costs(payment_schedule):
    # given a house with a given heat load and area, and cost tariff and growth
    # when I calculate the retirement energy payments
    actual_retirement_total_energy_cost = (
        payment_schedule["energy"].loc[2032:2052].sum()
    )

    # they are as expected
    expected_retirement_total_energy_cost = 58183  # from quality-control/energy.numbers
    assert actual_retirement_total_energy_cost == approx(
        expected_retirement_total_energy_cost, abs=1
    )
