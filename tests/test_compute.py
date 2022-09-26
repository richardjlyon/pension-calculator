from pension_calculator.graph import compute_annual_energy_cost, compute
import numpy as np
from pytest import approx

energy_prices = np.linspace(0.05, 0.2, 16)


def test_compute_annual_energy_cost():
    kwh_m2 = 133
    house_size_m2 = 67.8
    energy_prices = np.linspace(0.044, 0.2, 16)

    costs = compute_annual_energy_cost(kwh_m2, house_size_m2, energy_prices)

    assert costs[0] == approx(397, abs=1)
