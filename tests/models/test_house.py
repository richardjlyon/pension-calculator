from pension_calculator.models.house import House


def test_init():
    house = House(
        purchase_year=2022,
        purchase_cost=10000,
        passive_house_premium_pcnt=0.1,
        area_m2=100,
        annual_heating_kwh_m2a=100,
    )

    assert house.total_cost() == 11000
