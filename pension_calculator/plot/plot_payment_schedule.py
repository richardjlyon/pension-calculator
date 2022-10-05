"""Illustrate the difference over time in mortgage, energy, and pension payments between ordinary and passive houses.

This is a four panel figure with mortgage, heating, and pension time series for "average", "passive", and "difference".
The fourth panel computes the difference and displays it as a waterfall chart. Scenarios are specified in
`plot/scenarios.py`.
"""

import matplotlib.pyplot as plt

from pension_calculator import PLOT_DIR
from pension_calculator.compute.compute_payment_schedule import compute_payment_schedule
from pension_calculator.plot.scenario import (
    HOUSE_PURCHASE_YEAR,
    YOB,
    YOD,
    YOR,
    average_params,
    passive_params,
)
from pension_calculator.plot.helpers import currency, waterfall_chart

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

    # Top left: plot 'average' house.

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

    # Top right: plot 'passive' house.

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

    # Bottom left: plot difference.

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

    # Bottom right: "waterfall" showing cumulative differences.

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

    # Display selected parameters as a subtitle.

    ax1.annotate(
        f"Born: {passive_params.person_year_of_birth}, "
        f"Retire: {YOR}, "
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

    # Copyright footer.

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
