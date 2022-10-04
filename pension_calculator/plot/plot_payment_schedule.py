"""
plot_payment_schedule.py

A script to generate plot that illustrate the difference in mortgage, energy, and pension payments between ordinary
and passive houses. 
"""

import matplotlib.pyplot as plt

from pension_calculator.compute.compute_payment_schedule import (
    ScenarioParams,
    compute_data,
)

if __name__ == "__main__":
    params = ScenarioParams(
        person_year_of_birth=1965,
        house_purchase_year=2022,
        house_purchase_cost=100000,
        house_passive_house_premium=0.1,
        house_area_m2=100,
        house_annual_heating_kwh_m2a=100,
        mortgage_deposit=0,
        mortgage_interest_rate=0.06,
        mortgage_length_years=20,
        pension_growth_rate=0.01,
        energy_tariff=0.1,
        energy_cagr=0.05,
    )
    data_df = compute_data(params)

    print(data_df)

    data_df.plot()
    plt.show()
