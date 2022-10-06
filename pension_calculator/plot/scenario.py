"""Describes scenarios for computing mortgage, pension, and heating costs."""

from dataclasses import dataclass

from pension_calculator.models import Energy, House, Mortgage, Pension, Person

YOB = 1997
HOUSE_PURCHASE_YEAR = 2022
HOUSE_PURCHASE_COST = 160000
HOUSE_AREA_M2 = 100
MORTGAGE_DEPOSIT_PCNT = 0.1
MORTGAGE_INTEREST_RATE_PCNT = 0.0425
MORTGAGE_LENGTH_YEARS = 40
PENSION_GROWTH_RATE_PCNT = 0.01
ENERGY_TARIFF_PCNT = 0.05
ENERGY_CAGR_PCNT = 0.05


@dataclass
class ScenarioParams:
    """Stores parameters for passing to functions.

    Attributes:
        person: A person.
        house: A house.
        mortgage: A mortgage.
        pension: A pension.
        energy: Energy.

    """

    person: Person
    house: House
    mortgage: Mortgage
    pension: Pension
    energy: Energy


person = Person(YOB)

average_house = House(
    purchase_year=HOUSE_PURCHASE_YEAR,
    purchase_cost=HOUSE_PURCHASE_COST,
    passive_house_premium_pcnt=0.0,
    area_m2=HOUSE_AREA_M2,
    annual_heating_kwh_m2a=100,
)

average_mortgage = Mortgage(
    purchase_year=HOUSE_PURCHASE_YEAR,
    purchase_price=average_house.total_cost(),
    deposit_pcnt=MORTGAGE_DEPOSIT_PCNT,
    interest_rate_pcnt=MORTGAGE_INTEREST_RATE_PCNT,
    length_years=MORTGAGE_LENGTH_YEARS,
)

passive_house = House(
    purchase_year=HOUSE_PURCHASE_YEAR,
    purchase_cost=HOUSE_PURCHASE_COST,
    passive_house_premium_pcnt=0.15,
    area_m2=HOUSE_AREA_M2,
    annual_heating_kwh_m2a=15,
)

passive_mortgage = Mortgage(
    purchase_year=HOUSE_PURCHASE_YEAR,
    purchase_price=passive_house.total_cost(),
    deposit_pcnt=MORTGAGE_DEPOSIT_PCNT,
    interest_rate_pcnt=MORTGAGE_INTEREST_RATE_PCNT,
    length_years=MORTGAGE_LENGTH_YEARS,
)


pension = Pension(
    target=None,
    growth_rate_pcnt=PENSION_GROWTH_RATE_PCNT,
    start_year=HOUSE_PURCHASE_YEAR,
    end_year=person.yor,
)

energy = Energy(tariff=ENERGY_TARIFF_PCNT, cagr_pcnt=ENERGY_CAGR_PCNT)

average = ScenarioParams(
    person=person,
    house=average_house,
    mortgage=average_mortgage,
    pension=pension,
    energy=energy,
)

passive = ScenarioParams(
    person=person,
    house=passive_house,
    mortgage=passive_mortgage,
    pension=pension,
    energy=energy,
)
