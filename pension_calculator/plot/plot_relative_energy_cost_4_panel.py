"""
graphy.py

Generate a graph of the cost of an "average" house relative to a passive house as a function of
energy price and compound annual growth rate/.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

from pension_calculator import CURRENT_YEAR, PLOT_DIR
from pension_calculator.compute.compute_heating_cost_sensitivities import (
    compute_heating_cost_sensitivities,
)
from pension_calculator.compute.utils import print_sanity_check
from pension_calculator.models.person import Person
from pension_calculator.plot.utils import currency


def plot_4_panel(df: pd.DataFrame, person: Person, house_area_m2: float):
    """
    Plot a four panel figure illustrating the additional heating energy cost of an 'average' house relative to a passive
    house for a range of energy tariff and compound annual growth rates.

    Parameters
    ----------
    df A dataframe of data to plot
    person A person (to supply the year of death)
    house_area_m2 The area of the house (m2)

    Returns
    -------
    None

    """

    max_cost = result_df["average"].max(axis=1).max()

    fig = plt.figure()
    width_inches = 10
    height_inches = width_inches * 9 / 16
    fig.set_size_inches(width_inches, height_inches)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        f"Additional heating energy cost of an 'average' house relative to Passive House ({CURRENT_YEAR}-{person.yod})",
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
        f"Floor area: {house_area_m2} m2",
        (0, 0),
        (20, 180),
        xycoords="axes points",
        textcoords="offset pixels",
    )

    ax1.annotate(
        f"Year Of Birth: {person.yob}",
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
        PLOT_DIR / f"relative_energy_cost_4_panel_{person.yob}_{house_area_m2}.png"
    )
    plt.savefig(outfile)
    print(f"\nSaved file to {outfile}")

    plt.show()


if __name__ == "__main__":

    person = Person(1997)
    house_area_m2 = 100

    result_df = compute_heating_cost_sensitivities(
        person=person, house_area_m2=house_area_m2
    )
    delta_df = result_df["average"] - result_df["passive"]
    plot_4_panel(df=result_df, house_area_m2=house_area_m2, person=person)

    print_sanity_check(result_df, delta_df, house_area_m2, person)
