"""Generate a graph of the heating cost over time of an "average" house relative to a passive house.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from pension_calculator import CURRENT_YEAR, PLOT_DIR
from pension_calculator.compute.compute_heating_cost_sensitivities import (
    compute_heating_cost_sensitivities,
)
from pension_calculator.models.person import Person
from pension_calculator.plot.helpers import (
    annotate_copyright,
    annotate_subtitle,
    annotate_title,
    currency,
)


def plot():
    """Plot a 4 panel figure.

    This is a four panel figure with a different average energy tariff in each panel. The graph displays the total cost
    from the current year until the person's year of death as a function of average tariff compound average growth
    rate.

    Data is prepared by the imported `compute_heating_cost_sensitivities` function which returns a dataframe. The
    columns are a multiindex of house type (average, passive) and selected energy tariffs. The rows are selected
    tariff growth rates. Each value is the lifetime heating energy cost for that house type, tariff, and
    growth rate.

    """

    person = Person(1997)
    house_area_m2 = 100

    result_df = compute_heating_cost_sensitivities(
        person=person, house_area_m2=house_area_m2
    )

    # Initialise a four panel figure.

    fig = plt.figure()
    width_inches = 10
    height_inches = width_inches * 700 / 1280
    fig.set_size_inches(width_inches, height_inches)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        f"Additional heating energy cost of an 'average' house relative to Passive House ({CURRENT_YEAR}-{person.yod})",
        x=0.45,
        fontsize=12,
        fontweight="bold",
    )

    gs = fig.add_gridspec(2, 2, hspace=0.05, wspace=0.2)
    (ax1, ax2), (ax3, ax4) = gs.subplots(sharex="col")
    axes = [ax1, ax2, ax3, ax4]

    max_cost = result_df["average"].max(axis=1).max()
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

        title = f"Energy price: £{price:.2f}/kWh"
        annotate_title(ax, title, y=190)

    ax1.legend(loc="upper right")

    subtitle_text = f"Year Of Birth: {person.yob}, Floor area: {house_area_m2} m2"
    annotate_subtitle(ax1, subtitle_text)

    annotate_copyright(ax3)

    outfile = (
        PLOT_DIR / f"relative_energy_cost_4_panel_{person.yob}_{house_area_m2}.png"
    )
    plt.savefig(outfile)
    print(f"\nSaved file to {outfile}")

    plt.show()


if __name__ == "__main__":
    plot()
