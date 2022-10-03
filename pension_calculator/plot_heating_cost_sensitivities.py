"""
graphy.py

Generate a graph of the cost of an "average" house relative to a passive house as a function of
energy price and compound annual growth rate/.
"""

import datetime

import matplotlib.pyplot as plt
import toml
from matplotlib.offsetbox import AnchoredText
import matplotlib.ticker as mtick

from pension_calculator import ROOT
from pension_calculator.energy import compute_relative_energy_cost

PLOT_DIR = ROOT / "plots"

config = toml.load(f"{ROOT}/app.config.toml")


def currency(x, pos):
    """Format y axis currency label as £xxK"""
    if x >= 1e6:
        return "£{:1.1f}M".format(x * 1e-6)
    else:
        return "£{:1.0f}K".format(x * 1e-3)


def print_sanity_check(
    result_df, delta_df, year_of_birth, year_of_death, house_size_m2
):

    print("\nSanity check:")
    print("======================")
    print(f"Year of birth      : {year_of_birth}")
    print(
        f"Year of retirement : {year_of_birth + config.get('basic').get('pension_age')}"
    )
    print(f"Year of death      : {year_of_death}")
    print(f"House size         : {house_size_m2}m2\n")

    samples = [
        {"CAGR": 0.05, "price": 0.05},
        {"CAGR": 0.10, "price": 0.05},
        {"CAGR": 0.05, "price": 0.20},
        {"CAGR": 0.10, "price": 0.20},
    ]

    for sample in samples:
        cagr = sample["CAGR"]
        price = sample["price"]
        print(
            f"price: {price:.2f} |  CAGR: {cagr:.2f} | average: {round(result_df['average', price][cagr]):>7} | passive: {round(result_df['passive', price][cagr]):>7} | difference: {round(delta_df[price][cagr]):>7}"
        )

    return


def plot_single(delta_df):
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(currency)
    width_inches = 10
    height_inches = width_inches * 9 / 16
    fig.set_size_inches(width_inches, height_inches)
    fig.suptitle(
        f"Additional heating energy cost of an 'average' house relative to Passive House ({current_year}-{year_of_death})"
    )
    delta_df.plot(ax=ax)
    plt.legend(
        title="Energy variable unit cost (p/kWh)",
        labels=[round(col, 2) * 100 for col in delta_df.columns],
    )
    ax.set_xlabel("Energy price Compound Annual Growth Rate")
    text = f"Year of birth: {year_of_birth}\nHouse size: {house_size_m2}m2"
    at = AnchoredText(text, prop=dict(size=15), frameon=True, loc="upper center")
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)
    plt.grid(
        visible=True,
        which="major",
        axis="y",
        color="grey",
        linestyle="-",
        linewidth=0.5,
    )
    outfile = PLOT_DIR / f"heating_cost_comparison_{year_of_birth}_{house_size_m2}.png"
    plt.savefig(outfile)
    plt.show()
    print(f"\nSaved file to {outfile}")


def plot_4_panel(result_df, house_size_m2, year_of_birth, current_year, year_of_death):

    max_cost = result_df["average"].max(axis=1).max()

    fig = plt.figure()
    width_inches = 10
    height_inches = width_inches * 9 / 16
    fig.set_size_inches(width_inches, height_inches)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        f"Additional heating energy cost of an 'average' house relative to Passive House ({current_year}-{year_of_death})",
        fontsize=12,
    )

    gs = fig.add_gridspec(2, 2, hspace=0, wspace=0)
    (ax1, ax2), (ax3, ax4) = gs.subplots(sharex="col", sharey="row")
    axes = [ax1, ax2, ax3, ax4]
    prices = result_df["average"].columns[::-1]

    for ax, price in zip(axes, prices):

        ax.set_ylim([0, max_cost])
        ax.set_xlabel("Energy price annual growth rate ")
        ax.yaxis.set_major_formatter(currency)
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0, 0))

        result_df["average", price].plot(ax=ax, color="tab:red", label="Average")
        ax.fill_between(
            result_df.index,
            result_df["average", price],
            result_df["passive", price,],
            color="tab:red",
            alpha=0.25,
        )
        result_df["passive", price].plot(ax=ax, color="tab:green", label="Passive")
        ax.fill_between(
            result_df.index, result_df["passive", price], color="tab:green", alpha=0.25
        )

        ax.annotate(
            f"Energy price: £{price:.2f}/kWh",
            (0, 0),
            (20, 200),
            xycoords="axes points",
            textcoords="offset pixels",
        )

    ax1.legend(loc="upper right")

    ax1.annotate(
        f"Floor area: {house_size_m2} m2",
        (0, 0),
        (20, 180),
        xycoords="axes points",
        textcoords="offset pixels",
    )

    ax1.annotate(
        f"Year Of Birth: {year_of_birth}",
        (0, 0),
        (20, 160),
        xycoords="axes points",
        textcoords="offset pixels",
    )

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
        / f"heating_cost_comparison_4_panel_{year_of_birth}_{house_size_m2}.png"
    )
    plt.savefig(outfile)
    plt.show()
    print(f"\nSaved file to {outfile}")


if __name__ == "__main__":

    year_of_birth = 1997
    year_of_death = year_of_birth + config.get("basic").get("life_expectancy")
    current_year = datetime.date.today().year
    house_size_m2 = 100

    result_df = compute_relative_energy_cost(year_of_birth, house_size_m2)
    delta_df = result_df["average"] - result_df["passive"]

    print_sanity_check(result_df, delta_df, year_of_birth, year_of_death, house_size_m2)

    plot_single(delta_df)
    plot_4_panel(result_df, house_size_m2, year_of_birth, current_year, year_of_death)
