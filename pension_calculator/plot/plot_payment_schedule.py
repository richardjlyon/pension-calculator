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
    data_df = compute_payment_schedule(params)

    data_df.plot()
    plt.show()
