"""Generate a graph of heating cost as a function of tariff and tariff growth rate."""

import matplotlib.ticker as mtick
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText

from pension_calculator import CURRENT_YEAR, PLOT_DIR
from pension_calculator.compute.compute_heating_cost_sensitivities import (
    compute_heating_cost_sensitivities,
)
from pension_calculator.models import Person
from pension_calculator.plot.helpers import currency


def plot_single(df: pd.DataFrame, person: Person, house_area_m2: float):
    """Plot a single figure of lifetime heating energy cost.

    This is a single graph illustrating the additional lifetime heating energy cost of an "average" house relative to
    a passive house.

    The data to plot is provided as a dataframe. The columns are selected energy tariffs. The rows are selected
    tariff growth rates. Each value is the difference in lifetime heating energy cost between house types for that
    tariff and growth rate.

    Parameters:
        df: A dataframe of data to plot
        person: A person (to supply the year of death)
        house_area_m2: The area of the house (m2)
    """

    fig, ax = plt.subplots()
    width_inches = 10
    height_inches = width_inches * 9 / 16
    fig.set_size_inches(width_inches, height_inches)
    fig.suptitle(
        f"Additional heating energy cost of an 'average' house relative to Passive House ({CURRENT_YEAR}-{person.yod})"
    )
    ax.yaxis.set_major_formatter(currency)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0, 0))
    ax.set_xlabel("Energy price Compound Annual Growth Rate")
    text = f"Year of birth: {person.yob}\nHouse size: {house_area_m2}m2"
    at = AnchoredText(text, prop=dict(size=15), frameon=True, loc="upper center")
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)

    df.plot(ax=ax)
    plt.legend(
        title="Energy variable unit cost (p/kWh)",
        labels=[round(col, 2) * 100 for col in df.columns],
    )
    plt.grid(
        visible=True,
        which="major",
        axis="y",
        color="grey",
        linestyle="-",
        linewidth=0.5,
    )
    outfile = PLOT_DIR / f"relative_energy_cost_single_{person.yob}_{house_area_m2}.png"
    plt.savefig(outfile)
    plt.show()
    print(f"\nSaved file to {outfile}")


if __name__ == "__main__":

    person = Person(1997)
    house_area_m2 = 100

    result_df = compute_heating_cost_sensitivities(
        person=person, house_area_m2=house_area_m2
    )
    delta_df = result_df["average"] - result_df["passive"]

    plot_single(df=delta_df, person=person, house_area_m2=house_area_m2)
