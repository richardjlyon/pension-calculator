"""
compute_payment_schedule.py

A python script to compute the mortgage, energy, and pension payments for a specified house cost and energy demand.

Richard Lyon
3 October 2022

"""
from dataclasses import dataclass

import pandas as pd

from pension_calculator.models import Energy, House, Mortgage, Pension, Person
from pension_calculator.plot.scenario import ScenarioParams


def compute_payment_schedule(
    p: ScenarioParams, do_summary: bool = False
) -> pd.DataFrame:
    """
    Compute the energy, mortgage, and pension costs associated with a scenario described by the supplied scenario
    description.

    Parameters
    ----------
    p The scenario parameters

    Returns
    -------
    A dataframe containing the energy, mortgage, and pension costs with an index of years.

    """

    person = Person(yob=p.person_year_of_birth)

    house = House(
        purchase_year=p.house_purchase_year,
        purchase_cost=p.house_purchase_cost,
        passive_house_premium=p.house_passive_house_premium,
        area_m2=p.house_area_m2,
        annual_heating_kwh_m2a=p.house_annual_heating_kwh_m2a,
    )

    mortgage = Mortgage(
        purchase_year=p.house_purchase_year,
        purchase_price=house.total_cost(),
        deposit_percent=p.mortgage_deposit_percent,
        interest_rate=p.mortgage_interest_rate,
        length_years=p.mortgage_length_years,
    )

    if mortgage.final_year >= person.yod:
        raise AttributeError(
            f"Person dies before mortgage paid ({person.yod} vs. {mortgage.final_year})"
        )

    if mortgage.final_year >= person.yor:
        raise AttributeError(
            f"Person retires before mortgage paid ({person.yor} vs. {mortgage.final_year})"
        )

    energy = Energy(tariff=p.energy_tariff, cagr=p.energy_cagr)

    retirement_heating_cost = energy.retirement_cost(
        house_kwh_m2a=p.house_annual_heating_kwh_m2a,
        house_area_m2=p.house_area_m2,
        first_year=p.house_purchase_year,
        year_of_retirement=person.yor,
        year_of_death=person.yod,
    )

    pension = Pension(
        target=retirement_heating_cost,
        growth_rate=p.pension_growth_rate,
        start_year=p.house_purchase_year,
        end_year=person.yor,
    )

    annual_heating_payments = energy.annual_payments(
        house_kwh_m2a=p.house_annual_heating_kwh_m2a,
        house_area_m2=p.house_area_m2,
        first_year=p.house_purchase_year,
        last_year=person.yod,
    )
    annual_mortgage_payments = mortgage.annual_payments()["total"]
    annual_pension_payments = pension.annual_payments()["payment"]

    # print()
    # print(annual_mortgage_payments)

    df = pd.DataFrame(
        data={
            "heating": annual_heating_payments,
            "mortgage": annual_mortgage_payments,
            "pension": annual_pension_payments,
        },
        index=range(p.house_purchase_year, person.yod + 1),
    )
    if do_summary:
        events = {
            "YOB": person.yob,
            "Retire": person.yor,
            "Die": person.yod,
            "Purchase": house.purchase_year,
            "Mortgage paid": mortgage.final_year,
        }
        events = sorted(events.items(), key=lambda x: x[1])

        print()
        print("Summary\n============================================")
        for event in events:
            print(f"{event[0]}: {event[1]}")
        print(f"Total house purchase cost: £{house.total_cost():.0f}")
        print(f"Retirement heating cost:   £{retirement_heating_cost:.0f}")
        print(
            f"Monthly heating payment:   £{annual_heating_payments.iloc[0]/12:.0f} -> £{annual_heating_payments.iloc[-1]/12:.0f}"
        )
        print(f"Monthly mortgage payment:  £{annual_mortgage_payments.iloc[0]/12:.0f}")
        print(f"Monthly pension payment:   £{annual_pension_payments.iloc[0]/12:.0f}")

        print()
        print(df.head())

    return df


if __name__ == "__main__":
    params = ScenarioParams(
        person_year_of_birth=1997,
        house_purchase_year=2022,
        house_purchase_cost=100000,
        house_passive_house_premium=0.1,
        house_area_m2=100,
        house_annual_heating_kwh_m2a=100,
        mortgage_deposit_percent=0.1,
        mortgage_interest_rate=0.0425,
        mortgage_length_years=40,
        pension_growth_rate=0.01,
        energy_tariff=0.05,
        energy_cagr=0.04,
    )
    data_df = compute_payment_schedule(params, do_summary=True)
