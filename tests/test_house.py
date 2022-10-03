import datetime

from pension_calculator.house import House
from moneyed import Money, GBP


def test_init():
    house = House(
        purchase_date=datetime.datetime.now(),
        purchase_cost=Money(10000, "GBP"),
        passive_house_premium=0.1,
        area_m2=100,
    )

    assert house.total_cost() == Money(11000, "GBP")
