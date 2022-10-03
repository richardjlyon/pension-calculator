import datetime

from pension_calculator.models.house import House


def test_init():
    house = House(
        purchase_date=datetime.datetime.now(),
        purchase_cost=10000,
        passive_house_premium=0.1,
        area_m2=100,
    )

    assert house.total_cost() == 11000
