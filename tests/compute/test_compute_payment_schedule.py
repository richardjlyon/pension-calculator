import pytest
from pytest import approx

from pension_calculator.compute.compute_payment_schedule import (
    ScenarioParams,
    compute_payment_schedule,
)
from pension_calculator.models import Person


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
    actual_total_energy_cost = payment_schedule["heating"].sum()

    # they are as expected
    expected_total_energy_cost = 412470  # from quality-control/energy.numbers
    assert actual_total_energy_cost == approx(expected_total_energy_cost, abs=1)


def test_retirement_heating_costs(payment_schedule):
    # given a house with a given heat load and area, and cost tariff and growth
    # when I calculate the retirement energy payments
    actual_retirement_total_energy_cost = (
        payment_schedule["heating"].loc[2032:2052].sum()
    )

    # they are as expected
    expected_retirement_total_energy_cost = 58183  # from quality-control/energy.numbers
    assert actual_retirement_total_energy_cost == approx(
        expected_retirement_total_energy_cost, abs=1
    )


def test_exception_if_retire_before_mortgage_paid():
    # given a scenario in which the person retires before the mortgage is paid
    params = ScenarioParams(
        Person(1974),  # retires 2041
        house_purchase_year=2022,
        house_purchase_cost=350000 / 1.1,
        house_passive_house_premium=0.1,
        house_area_m2=100,
        house_annual_heating_kwh_m2a=100,
        mortgage_deposit_percent=0.1,
        mortgage_interest_rate=0.0425,
        mortgage_length_years=20,  # mortgage paid 2041
        pension_growth_rate=0.01,
        energy_tariff=0.1,
        energy_cagr=0.05,
    )
    # when I compute the payment schedule
    # then an exception is raised
    with pytest.raises(AttributeError):
        df = compute_payment_schedule(params)


def test_exception_if_die_before_mortgage_paid():
    # given a scenario in which the person dies before the mortgage is paid
    params = ScenarioParams(
        Person(1954),  # dies 2041
        house_purchase_year=2022,
        house_purchase_cost=350000 / 1.1,
        house_passive_house_premium=0.1,
        house_area_m2=100,
        house_annual_heating_kwh_m2a=100,
        mortgage_deposit_percent=0.1,
        mortgage_interest_rate=0.0425,
        mortgage_length_years=20,  # mortgage paid 2041
        pension_growth_rate=0.01,
        energy_tariff=0.1,
        energy_cagr=0.05,
    )

    # when I compute the payment schedule
    # then an exception is raised
    with pytest.raises(AttributeError):
        df = compute_payment_schedule(params)
