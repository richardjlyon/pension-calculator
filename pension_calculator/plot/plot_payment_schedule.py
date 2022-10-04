"""
plot_payment_schedule.py

A script to generate plot that illustrate the difference in mortgage, energy, and pension payments between ordinary
and passive houses. 
"""

import matplotlib.pyplot as plt

from pension_calculator.compute.compute_payment_schedule import (
    ScenarioParams,
    compute_payment_schedule,
)

YOB = 1997
HOUSE_PURCHASE_YEAR = 2022
HOUSE_PURCHASE_COST = 160000
HOUSE_AREA_M2 = 100
MORTGAGE_DEPOSIT_PERCENT = 0.1
MORTGAGE_INTEREST_RATE = 0.0425
MORTGAGE_LENGTH_YEARS = 40
PENSION_GROWTH_RATE = 0.01
ENERGY_TARIFF = 0.05
ENERGY_CAGR = 0.05

average_params = ScenarioParams(
    person_year_of_birth=YOB,
    house_purchase_year=HOUSE_PURCHASE_YEAR,
    house_purchase_cost=HOUSE_PURCHASE_COST,
    house_passive_house_premium=0.0,
    house_area_m2=HOUSE_AREA_M2,
    house_annual_heating_kwh_m2a=100,
    mortgage_deposit_percent=MORTGAGE_DEPOSIT_PERCENT,
    mortgage_interest_rate=MORTGAGE_INTEREST_RATE,
    mortgage_length_years=MORTGAGE_LENGTH_YEARS,
    pension_growth_rate=PENSION_GROWTH_RATE,
    energy_tariff=ENERGY_TARIFF,
    energy_cagr=ENERGY_CAGR,
)

passive_params = ScenarioParams(
    person_year_of_birth=YOB,
    house_purchase_year=HOUSE_PURCHASE_YEAR,
    house_purchase_cost=HOUSE_PURCHASE_COST,
    house_passive_house_premium=0.15,
    house_area_m2=HOUSE_AREA_M2,
    house_annual_heating_kwh_m2a=15,
    mortgage_deposit_percent=MORTGAGE_DEPOSIT_PERCENT,
    mortgage_interest_rate=MORTGAGE_INTEREST_RATE,
    mortgage_length_years=MORTGAGE_LENGTH_YEARS,
    pension_growth_rate=PENSION_GROWTH_RATE,
    energy_tariff=ENERGY_TARIFF,
    energy_cagr=ENERGY_CAGR,
)

if __name__ == "__main__":

    average_df = compute_payment_schedule(average_params)
    passive_df = compute_payment_schedule(passive_params, do_summary=True)
    delta_df = passive_df - average_df

    average_df.plot()
    passive_df.plot()
    delta_df.plot()

    plt.show()
