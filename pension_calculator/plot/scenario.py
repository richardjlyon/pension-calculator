"""Describes scenarios for computing mortgage, pension, and heating costs."""

from dataclasses import dataclass

from pension_calculator import CONFIG


@dataclass
class ScenarioParams:
    """Stores parameters for passing to functions.

    Attributes:
        person_year_of_birth: Year of birth.
        house_purchase_year: House purchase year.
        house_purchase_cost: House purchase cost.
        house_passive_house_premium: Additional cost for meeting PH specification. Expressed as percent e.g. '0.1'.
        house_area_m2: Area of the house in square meters.
        house_annual_heating_kwh_m2a: Annual heating energy demand in kilowatt-hours per square meter per year.
        mortgage_deposit_percent: Mortgage deposit as a percentage of purchase cost e.g. '0.1'.
        mortgage_interest_rate: Mortgage interest rate as a percent e.g. '0.05'.
        mortgage_length_years: Mortgage length in years.
        pension_growth_rate: Pension annual growth rate in percent e.g. '0.05'.
        energy_tariff: Energy tariff in pounds per killowatt-hours e.g. '0.05'.
        energy_cagr: Energy compound annual growth rate in percent e.g. '0.05'.
    """

    person_year_of_birth: int
    house_purchase_year: int
    house_purchase_cost: int
    house_passive_house_premium: float
    house_area_m2: float
    house_annual_heating_kwh_m2a: float
    mortgage_deposit_percent: float
    mortgage_interest_rate: float
    mortgage_length_years: int
    pension_growth_rate: float
    energy_tariff: float
    energy_cagr: float


YOB = 1997
YOD = YOB + CONFIG.get("basic").get("life_expectancy")
YOR = YOB + CONFIG.get("basic").get("pension_age") - 1
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
