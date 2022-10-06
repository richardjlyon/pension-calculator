"""
compute_payment_schedule.py

A python script to compute the mortgage, energy, and pension payments for a specified house cost and energy demand.

Richard Lyon
3 October 2022

"""

import pandas as pd

from pension_calculator.models import Energy, House, Mortgage, Pension, Person
from pension_calculator.plot.scenario import ScenarioParams, passive


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

    if p.mortgage.final_year >= p.person.yod:
        raise AttributeError(
            f"Person dies before mortgage paid ({p.person.yod} vs. {p.mortgage.final_year})"
        )

    if p.mortgage.final_year >= p.person.yor:
        raise AttributeError(
            f"Person retires before mortgage paid ({p.person.yor} vs. {p.mortgage.final_year})"
        )

    retirement_heating_cost = p.energy.retirement_cost(
        house_kwh_m2a=p.house.annual_heating_kwh_m2a,
        house_area_m2=p.house.area_m2,
        first_year=p.house.purchase_year,
        year_of_retirement=p.person.yor,
        year_of_death=p.person.yod,
    )

    p.pension.target = retirement_heating_cost

    annual_heating_payments = p.energy.annual_payments(
        house_kwh_m2a=p.house.annual_heating_kwh_m2a,
        house_area_m2=p.house.area_m2,
        first_year=p.house.purchase_year,
        last_year=p.person.yod,
    )
    annual_mortgage_payments = p.mortgage.annual_payments()["total"]
    annual_pension_payments = p.pension.annual_payments()["payment"]
    annual_pension_value = p.pension.annual_payments()["value"]

    # print()
    # print(annual_mortgage_payments)

    df = pd.DataFrame(
        data={
            "heating": annual_heating_payments,
            "mortgage": annual_mortgage_payments,
            "pension": annual_pension_payments,
            "pension_value": annual_pension_value,
        },
        index=range(p.house.purchase_year, p.person.yod + 1),
    )
    if do_summary:
        events = {
            "YOB": p.person.yob,
            "Retire": p.person.yor,
            "Die": p.person.yod,
            "Purchase": p.house.purchase_year,
            "Mortgage paid": p.mortgage.final_year,
        }
        events = sorted(events.items(), key=lambda x: x[1])

        print()
        print("Summary\n============================================")
        for event in events:
            print(f"{event[0]}: {event[1]}")
        print(f"Total house purchase cost: £{p.house.total_cost():.0f}")
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

    data_df = compute_payment_schedule(passive, do_summary=True)
