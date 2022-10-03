import numpy as np
from pytest import approx

from pension_calculator.energy import Energy

KWH_M2 = 100
HOUSE_SIZE_M2 = 100
TARIFF = 0.1
CAGR = 0.1
YEARS = 10
EXPECTED_TOTAL = 15937.42  # see Numbers document


def test_annual_energy_cost():
    energy = Energy(energy_type="electricity", tariff=TARIFF, cagr=CAGR)
    assert energy.annual_energy_cost(kwh_m2=KWH_M2, house_size_m2=HOUSE_SIZE_M2) == 1000


def test_annual_payments():

    energy = Energy(energy_type="electricity", tariff=TARIFF, cagr=CAGR)

    yearly_payments = energy.annual_payments(
        years=YEARS, kwh_m2=KWH_M2, house_size_m2=HOUSE_SIZE_M2
    )

    assert yearly_payments["payment"].sum() == approx(EXPECTED_TOTAL)


# @pytest.mark.parametrize(
#     "cagr, price, average, passive, difference",
#     [
#         (0.05, 0.05, 17860, 2679, 15181),
#         (0.1, 0.05, 32001, 4800, 27201),
#         (0.05, 0.2, 71439, 10716, 60723),
#         (0.1, 0.2, 128005, 19201, 108804),
#     ],
# )
# def test_compute_relative_energy_cost(cagr, price, average, passive, difference):
#     life_expectancy = 21
#     house_size_m2 = 100
#     result_df = compute_relative_energy_cost(life_expectancy, house_size_m2)
#     delta_df = result_df["average"] - result_df["passive"]
#
#     assert round(result_df["average", price][cagr]) == average
#     assert round(result_df["passive", price][cagr]) == passive
#     assert round(delta_df[price][cagr]) == difference
