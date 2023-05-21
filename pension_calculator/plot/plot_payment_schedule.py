"""Illustrate the difference over time in mortgage, energy, and pension payments between ordinary and passive houses.

This is a four panel figure with mortgage, heating, and pension time series for "average", "passive", and "difference".
The fourth panel computes the difference and displays it as a waterfall chart. Scenarios are specified in
`plot/scenarios.py`.
"""

import matplotlib.pyplot as plt

from pension_calculator.compute.compute_payment_schedule import compute_payment_schedule
from pension_calculator.plot.helpers import (
    annotate_copyright,
    annotate_subtitle,
    annotate_title,
    compute_lowest_decade,
    currency,
    make_outfile_name,
    retirement_rectangle,
    waterfall_chart,
)
from pension_calculator.plot.scenario import (
    average,
    passive,
)


def plot():

    average_df = compute_payment_schedule(average)
    passive_df = compute_payment_schedule(passive)
    delta_df = passive_df - average_df

    # Initialise a four panel figure.

    fig = plt.figure()
    width_inches = 10
    height_inches = width_inches * 700 / 1280
    fig.set_size_inches(width_inches, height_inches)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        f"Pension, mortgage, and heating annual payments for a Passive house relative to average ({average.house.purchase_year}-{average.person.yod})",
        x=0.5,
        fontsize=12,
        fontweight="bold",
    )
    gs = fig.add_gridspec(2, 2, hspace=0.2, wspace=0.2)
    (ax1, ax2), (ax3, ax4) = gs.subplots()
    axes = [ax1, ax2, ax3, ax4]

    # Set axis limits.

    max_cost = average_df[["mortgage", "heating", "pension"]].max(axis=1).max() * 1.2
    min_year = compute_lowest_decade(average_df.index.min())
    max_year = average_df.index.max()

    for ax in [ax1, ax2, ax3]:
        ax.yaxis.set_major_formatter(currency)
        ax.set_xlim([min_year, max_year])

    # Top left: Average house.

    title = f"Average - {average.house.annual_heating_kwh_m2a} kWh/m2(a)"
    annotate_title(ax1, title)
    annotate_title(ax1, "RETIREMENT", x=250, y=10, color="tab:red")
    ax1.add_patch(
        retirement_rectangle(average.person.yor, average.person.yod, max_cost)
    )
    ax1.set_ylim([0, max_cost])

    average_df["mortgage"].plot(ax=ax1, legend=None, color="tab:blue")
    average_df["heating"].plot(ax=ax1, legend=None, color="tab:orange")
    average_df["pension"].plot(ax=ax1, legend=None, color="tab:green")

    ax1.fill_between(
        average_df.index, average_df["heating"], color="tab:orange", alpha=0.25
    )
    ax1.fill_between(
        average_df.index, average_df["mortgage"], color="tab:blue", alpha=0.25
    )
    ax1.fill_between(
        average_df.index, average_df["pension"], color="tab:green", alpha=0.25
    )

    # Top right: Passive house.

    title = f"Passive - {average.house.annual_heating_kwh_m2a} kWh/m2(a)"
    annotate_title(ax2, title)
    ax2.add_patch(
        retirement_rectangle(average.person.yor, average.person.yod, max_cost)
    )
    ax2.set_ylim([0, max_cost])

    passive_df["mortgage"].plot(ax=ax2, legend="mortgage", color="tab:blue")
    passive_df["heating"].plot(ax=ax2, legend="heating", color="tab:orange")
    passive_df["pension"].plot(ax=ax2, legend="pension", color="tab:green")

    ax2.fill_between(
        passive_df.index, passive_df["heating"], color="tab:orange", alpha=0.25
    )
    ax2.fill_between(
        passive_df.index, passive_df["mortgage"], color="tab:blue", alpha=0.25
    )
    ax2.fill_between(
        passive_df.index, passive_df["pension"], color="tab:green", alpha=0.25
    )
    ax2.legend(loc="upper right")

    # Bottom left: difference.

    annotate_title(ax3, "Difference", y=10)

    min_cost = delta_df[["mortgage", "heating", "pension"]].min(axis=1).min()
    max_cost = delta_df[["mortgage", "heating", "pension"]].max(axis=1).max() * 1.5
    ax3.set_ylim([min_cost, max_cost])

    ax3.add_patch(
        retirement_rectangle(
            average.person.yor, average.person.yod, min_cost * 1.5, max_cost,
        )
    )

    delta_df["mortgage"].plot(ax=ax3, legend=None, color="tab:blue")
    delta_df["heating"].plot(ax=ax3, legend=None, color="tab:orange")
    delta_df["pension"].plot(ax=ax3, legend=None, color="tab:green")

    ax3.fill_between(
        delta_df.index, delta_df["heating"], color="tab:orange", alpha=0.25
    )
    ax3.fill_between(delta_df.index, delta_df["mortgage"], color="tab:blue", alpha=0.25)
    ax3.fill_between(delta_df.index, delta_df["pension"], color="tab:green", alpha=0.25)

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

    subtitle_text = (
        f"Born: {passive.person.yob}, "
        f"Retire: {passive.person.yor}, "
        f"House cost: £{passive.house.purchase_cost / 1000:1.0f}K, "
        f"{passive.mortgage.interest_rate_pcnt * 100}%/{passive.mortgage.length_years}y "
        f"Mortgage, Area: {passive.house.area_m2}m2, "
        f"Energy Tariff: {passive.energy.tariff * 100}p/kWh, "
        f"Energy CAGR: {passive.energy.cagr_pcnt * 100:1.0f}%, "
        f"Pension CAGR: {passive.pension.growth_rate_pcnt * 100:1.0f}%"
    )
    annotate_subtitle(ax1, subtitle_text)
    annotate_copyright(ax3)

    outfile = make_outfile_name("payment_schedule", average.person.yob)
    plt.savefig(outfile)
    print(f"\nSaved file to {outfile}")

    plt.show()


if __name__ == "__main__":
    plot()
