from pytest import approx

from pension_calculator.models.energy import Energy


def test_annual_energy_cost(energy):
    assert energy.annual_energy_cost(kwh_m2=100, house_size_m2=100) == 1000


def test_annual_payments(energy):
    yearly_payments = energy.annual_payments(years=10, kwh_m2=100, house_size_m2=100)
    expected_total = 15937.42  # see Numbers document

    assert yearly_payments.sum() == approx(expected_total)


def test_retirement_cost(energy):
    retirement_cost = energy.retirement_cost()
    expected_total = 0

    # assert retirement_cost == approx(expected_total)


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
