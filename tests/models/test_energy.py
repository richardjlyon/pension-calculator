from pytest import approx


def test_annual_energy_cost(energy):
    assert energy.annual_energy_cost(house_kwh_m2a=100, house_area_m2=100) == 1000


def test_annual_payments(energy):
    annual_payments = energy.annual_payments(
        house_kwh_m2a=100, house_area_m2=100, first_year=2022, last_year=2052
    )
    expected_total = 70761  # see Numbers document

    assert annual_payments.sum() == approx(expected_total, abs=1)


def test_retirement_cost(energy):
    retirement_cost = energy.retirement_cost(
        house_kwh_m2a=100,
        house_area_m2=100,
        first_year=2022,
        year_of_retirement=2032,
        year_of_death=2052,
    )

    expected_total = 58183  # see Numbers document

    assert retirement_cost == approx(expected_total, abs=1)


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
#     house_area_m2 = 100
#     result_df = compute_relative_energy_cost(life_expectancy, house_area_m2)
#     delta_df = result_df["average"] - result_df["passive"]
#
#     assert round(result_df["average", price][cagr]) == average
#     assert round(result_df["passive", price][cagr]) == passive
#     assert round(delta_df[price][cagr]) == difference
