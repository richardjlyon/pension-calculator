"""
house.py

Richard Lyon
3 October 2022
"""
import datetime
from dataclasses import dataclass


@dataclass
class House:
    """Represents a house with a mortgage and energy bills."""

    purchase_date: datetime.datetime
    purchase_cost: float
    passive_house_premium: float
    area_m2: float

    def total_cost(self) -> float:
        """Compute the total cost of the house."""
        return self.purchase_cost * (1 + self.passive_house_premium)