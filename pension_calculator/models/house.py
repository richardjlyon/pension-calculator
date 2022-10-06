"""A class that represents a house."""

from dataclasses import dataclass


@dataclass
class House:
    """Represents a house with a purchase cost and annual heating requirements.

    Attributes:
        purchase_year: The year of purchase.
        purchase_cost: The purchase cost.
        passive_house_premium: The additional cost to meet Passive House standard, as a percent e.g. '0.1'.
        area_m2: float The area of the house for heating purposes, expressed in square meters.
        annual_heating_kwh_m2a: The annual heating requirement of the house in kilowatt-hours per square meter per year.
    """

    purchase_year: int
    purchase_cost: float
    passive_house_premium_pcnt: float
    area_m2: float
    annual_heating_kwh_m2a: float

    def total_cost(self) -> float:
        """Compute the total cost of the house including additional passive house costs."""
        return self.purchase_cost * (1 + self.passive_house_premium_pcnt)
