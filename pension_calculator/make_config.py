"""
make_config.py

Creates a configuration file for a given experiment.

Usage:
"""
from toml_config.core import Config

if __name__ == "__main__":
    my_config = Config("app.config.toml")
    my_config.add_section("basic").set(
        year_of_birth=1965,
        pension_age=67,
        life_expectancy=87,
        average_house_size_m2=67.8,
        variable_unit_cost_electricity=0.143,
        variable_unit_cost_gas=0.044,
    )
    my_config.add_section("energy_use").set(average=133, passive=15)
    my_config.add_section("sensitivities").set(
        price_min=0.05, price_max=0.2, cagr_min=0.05, cagr_max=0.15
    )
    my_config.add_section("CAGR").set(
        gas=0.05, electricity=0.08,
    )
