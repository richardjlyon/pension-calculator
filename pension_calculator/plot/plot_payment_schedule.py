"""
plot_payment_schedule.py

A script to generate plot that illustrate the difference in mortgage, energy, and pension payments between ordinary
and passive houses. 
"""

import matplotlib.pyplot as plt
from pension_calculator.plot.utils import waterfall_chart

from pension_calculator import CONFIG, PLOT_DIR
from pension_calculator.compute.compute_payment_schedule import (
    ScenarioParams,
    compute_payment_schedule,
)
from pension_calculator.plot.utils import currency

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

if __name__ == "__main__":

    average_df = compute_payment_schedule(average_params)
    passive_df = compute_payment_schedule(passive_params, do_summary=True)
    delta_df = passive_df - average_df

    # initialise figure
    fig = plt.figure()
    width_inches = 10
    height_inches = width_inches * 9 / 16
    fig.set_size_inches(width_inches, height_inches)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        f"Pension, mortgage, and heating cost of a Passive house relative to average ({HOUSE_PURCHASE_YEAR}-{YOD})",
        x=0.45,
        fontsize=12,
        fontweight="bold",
    )

    # make four subplots and get axes

    max_cost = average_df.max(axis=1).max() * 1.2

    gs = fig.add_gridspec(2, 2, hspace=0.2, wspace=0.2)
    (ax1, ax2), (ax3, ax4) = gs.subplots()
    axes = [ax1, ax2, ax3, ax4]

    # top left: plot 'average' house
    ax1.yaxis.set_major_formatter(currency)
    ax1.set_ylim([0, max_cost])
    ax1.annotate(
        f"Average - {average_params.house_annual_heating_kwh_m2a} kWh/m2(a)",
        (0, 0),
        (20, 180),
        xycoords="axes points",
        textcoords="offset pixels",
    )
    average_df.plot(ax=ax1, legend=None)
    ax1.fill_between(
        average_df.index, average_df["heating"], color="tab:blue", alpha=0.25
    )
    ax1.fill_between(
        average_df.index, average_df["mortgage"], color="tab:orange", alpha=0.25
    )
    ax1.fill_between(
        average_df.index, average_df["pension"], color="tab:green", alpha=0.25
    )
    ax1.axvline(x=YOR, ymin=0, ymax=max_cost, color="tab:red", alpha=0.25)

    # top right: plot 'passive' house
    ax2.yaxis.set_major_formatter(currency)
    ax2.set_ylim([0, max_cost])
    ax2.annotate(
        f"Passive - {passive_params.house_annual_heating_kwh_m2a} kWh/m2(a)",
        (0, 0),
        (20, 180),
        xycoords="axes points",
        textcoords="offset pixels",
    )
    passive_df.plot(ax=ax2).legend(loc="upper right")
    ax2.fill_between(
        passive_df.index, passive_df["heating"], color="tab:blue", alpha=0.25
    )
    ax2.fill_between(
        passive_df.index, passive_df["mortgage"], color="tab:orange", alpha=0.25
    )
    ax2.fill_between(
        passive_df.index, passive_df["pension"], color="tab:green", alpha=0.25
    )
    ax2.axvline(x=YOR, ymin=0, ymax=max_cost, color="tab:red", alpha=0.25)

    # bottom left: plot difference
    ax3.yaxis.set_major_formatter(currency)
    ax3.annotate(
        f"Difference",
        (0, 0),
        (20, 10),
        xycoords="axes points",
        textcoords="offset pixels",
    )
    delta_df.plot(ax=ax3, legend=None)
    ax3.fill_between(delta_df.index, delta_df["heating"], color="tab:blue", alpha=0.25)
    ax3.fill_between(
        delta_df.index, delta_df["mortgage"], color="tab:orange", alpha=0.25
    )
    ax3.fill_between(delta_df.index, delta_df["pension"], color="tab:green", alpha=0.25)
    ax3.axvline(x=YOR, ymin=0, ymax=max_cost, color="tab:red", alpha=0.25)

    # bottom right: "waterfall"
    labels = ["mortgage", "heating", "pension"]
    data = [
        -delta_df["mortgage"].sum(),
        -delta_df["heating"].sum(),
        -delta_df["pension"].sum(),
    ]

    waterfall_chart(
        labels,
        data,
        ax=ax4,
        sorted_value=True,
        green_color="tab:green",
        red_color="tab:red",
        blue_color="tab:blue",
        Title="Savings",
        rotation_value=0,
        formatting="£ {:,.0f}",
        net_label="saving",
    )

    # parameters
    ax1.annotate(
        f"Born: {passive_params.person_year_of_birth}, "
        f"Retired: {YOR}, "
        f"House cost: £{passive_params.house_purchase_cost/1000:1.0f}K, "
        f"{passive_params.mortgage_interest_rate*100}%/{passive_params.mortgage_length_years}y Mortgage, "
        f"Area: {passive_params.house_area_m2}m2, "
        f"Energy Tariff: {passive_params.energy_tariff*100}p/kWh, "
        f"Energy CAGR: {passive_params.energy_cagr*100:1.0f}%, "
        f"Pension CAGR: {passive_params.pension_growth_rate*100:1.0f}%",
        (0, 0),
        (33, 525),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
        fontsize="small",
    )

    # footer
    ax3.annotate(
        "Lyon Energy Futures Ltd.",
        (0, 0),
        (30, 25),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )

    outfile = (
        PLOT_DIR
        / f"payment_shedule_{YOB}_tarrif_{passive_params.energy_tariff}_cagr_{passive_params.energy_cagr}.png"
    )
    plt.savefig(outfile)
    print(f"\nSaved file to {outfile}")

    plt.show()
