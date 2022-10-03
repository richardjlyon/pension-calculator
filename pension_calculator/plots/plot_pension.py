"""
plot_pension.py

A script to generate plots that illustrate the difference in mortgage, energy, and pension payments between ordinary
and passive houses. 
"""
import datetime

from pension_calculator.models.energy import Energy
from pension_calculator.models.house import House
from pension_calculator.models.mortgage import Mortgage
from pension_calculator.models.person import Person


def do_pension_plot():
    person = Person(yob=1965)

    house = House(
        purchase_date=datetime.datetime.now(),
        purchase_cost=100000,
        passive_house_premium=0.1,
        area_m2=100,
        annual_heating_kwh_m2a=100,
    )

    mortgage = Mortgage(
        purchase_price=house.total_cost(),
        deposit=0,
        interest_rate=0.06,
        length_years=20,
    )

    energy = Energy(tariff=0.1, cagr=0.05)


if __name__ == "__main__":
    do_pension_plot()
