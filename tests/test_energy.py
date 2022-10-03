import numpy as np
import pytest

from pension_calculator.energy import (
    compute_annual_energy_cost,
    compute_relative_energy_cost,
)

energy_prices = np.linspace(0.05, 0.2, 16)


def test_compute_annual_energy_cost():
    kwh_m2 = 133
    house_size_m2 = 67.8
    energy_prices = np.linspace(0.044, 0.2, 16)

    costs = compute_annual_energy_cost(kwh_m2, house_size_m2, energy_prices)

    assert costs[0] == pytest.approx(397, abs=1)


@pytest.mark.parametrize(
    "cagr, price, average, passive, difference",
    [
        (0.05, 0.05, 17860, 2679, 15181),
        (0.1, 0.05, 32001, 4800, 27201),
        (0.05, 0.2, 71439, 10716, 60723),
        (0.1, 0.2, 128005, 19201, 108804),
    ],
)
def test_compute_relative_energy_cost(cagr, price, average, passive, difference):
    year_of_birth = 1955
    house_size_m2 = 100
    result_df = compute_relative_energy_cost(year_of_birth, house_size_m2)
    delta_df = result_df["average"] - result_df["passive"]

    assert round(result_df["average", price][cagr]) == average
    assert round(result_df["passive", price][cagr]) == passive
    assert round(delta_df[price][cagr]) == difference
