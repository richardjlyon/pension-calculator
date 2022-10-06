"""Helpers for plotting charts."""
import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pension_calculator import PLOT_DIR
from pension_calculator.plot.scenario import passive


def currency(x, pos):
    """Format y axis currency label as £xxK."""
    if x >= 1e6:
        return "£{:1.1f}M".format(x * 1e-6)
    else:
        return "£{:1.0f}K".format(x * 1e-3)


def waterfall_chart(
    index,
    data,
    Title="",
    x_lab="",
    y_lab="",
    ax=None,
    formatting="{:,.1f}",
    green_color="#29EA38",
    red_color="#FB3C62",
    blue_color="#24CAFF",
    sorted_value=False,
    threshold=None,
    other_label="other",
    net_label="net",
    rotation_value=30,
    blank_color=(0, 0, 0, 0),
    figsize=(10, 10),
):
    """
    Given two sequences ordered appropriately, generate a standard waterfall chart.
    Optionally modify the title, axis labels, number formatting, bar colors,
    increment sorting, and thresholding. Thresholding groups lower magnitude changes
    into a combined group to display as a single entity on the chart.

    https://github.com/chrispaulca/waterfall
    """

    # convert data and index to np.array
    index = np.array(index)
    data = np.array(data)

    # sorted by absolute value
    if sorted_value:
        abs_data = abs(data)
        data_order = np.argsort(abs_data)[::-1]
        data = data[data_order]
        index = index[data_order]

    # group contributors less than the threshold into 'other'
    if threshold:

        abs_data = abs(data)
        threshold_v = abs_data.max() * threshold

        if threshold_v > abs_data.min():
            index = np.append(index[abs_data >= threshold_v], other_label)
            data = np.append(
                data[abs_data >= threshold_v], sum(data[abs_data < threshold_v])
            )

    changes = {"amount": data}

    ax.yaxis.set_major_formatter(currency)

    # Store data and create a blank series to use for the waterfall
    trans = pd.DataFrame(data=changes, index=index)
    blank = trans.amount.cumsum().shift(1).fillna(0)

    trans["positive"] = trans["amount"] > 0

    # Get the net total number for the final element in the waterfall
    total = trans.sum().amount
    trans.loc[net_label] = total
    blank.loc[net_label] = total

    # The steps graphically show the levels as well as used for label placement
    step = blank.reset_index(drop=True).repeat(3).shift(-1)
    step[1::3] = np.nan

    # When plotting the last element, we want to show the full bar,
    # Set the blank to 0
    blank.loc[net_label] = 0

    # define bar colors for net bar
    trans.loc[trans["positive"] > 1, "positive"] = 99
    trans.loc[trans["positive"] < 0, "positive"] = 99
    trans.loc[(trans["positive"] > 0) & (trans["positive"] < 1), "positive"] = 99

    trans["color"] = trans["positive"]

    trans.loc[trans["positive"] == 1, "color"] = green_color
    trans.loc[trans["positive"] == 0, "color"] = red_color
    trans.loc[trans["positive"] == 99, "color"] = blue_color

    my_colors = list(trans.color)

    # Plot and label
    my_plot = plt.bar(range(0, len(trans.index)), blank, width=0.5, color=blank_color)
    plt.bar(
        range(0, len(trans.index)),
        trans.amount,
        width=0.6,
        bottom=blank,
        color=my_colors,
    )

    # connecting lines - figure out later
    # my_plot = lines.Line2D(step.index, step.values, color = "gray")
    # my_plot = lines.Line2D((3,3), (4,4))

    # axis labels
    plt.xlabel("\n" + x_lab)
    plt.ylabel(y_lab + "\n")

    # Get the y-axis position for the labels
    y_height = trans.amount.cumsum().shift(1).fillna(0)

    temp = list(trans.amount)

    # create dynamic chart range
    for i in range(len(temp)):
        if (i > 0) & (i < (len(temp) - 1)):
            temp[i] = temp[i] + temp[i - 1]

    trans["temp"] = temp

    plot_max = trans["temp"].max()
    plot_min = trans["temp"].min()

    # Make sure the plot doesn't accidentally focus only on the changes in the data
    if all(i >= 0 for i in temp):
        plot_min = 0
    if all(i < 0 for i in temp):
        plot_max = 0

    if abs(plot_max) >= abs(plot_min):
        maxmax = abs(plot_max)
    else:
        maxmax = abs(plot_min)

    pos_offset = maxmax / 40

    plot_offset = maxmax / 15  ## needs to me cumulative sum dynamic

    # Start label loop
    loop = 0
    for index, row in trans.iterrows():
        # For the last item in the list, we don't want to double count
        if row["amount"] == total:
            y = y_height[loop]
        else:
            y = y_height[loop] + row["amount"]
        # Determine if we want a neg or pos offset
        if row["amount"] > 0:
            y += pos_offset * 2
            plt.annotate(
                formatting.format(row["amount"]),
                (loop, y),
                ha="center",
                color="g",
                fontsize=9,
            )
        else:
            y -= pos_offset * 4
            plt.annotate(
                formatting.format(row["amount"]),
                (loop, y),
                ha="center",
                color="r",
                fontsize=9,
            )
        loop += 1

    # Scale up the y axis so there is room for the labels
    plt.ylim(0, plot_max + round(3.6 * plot_offset, 7))
    # Rotate the labels
    plt.xticks(range(0, len(trans)), trans.index, rotation=rotation_value)


def retirement_rectangle(
    yor: int, yod: int, max_cost: float, min_cost: float = 0
) -> matplotlib.patches.Rectangle:
    """Return a rectangle representing the retirement period.
    Args:
        yor: Year of retirement
        yod: Year of death
        max_cost: Maximum cost
        min_cost: Minimum cost

    Returns:
        A Rectangle patch representing the retirement period.

    """
    return matplotlib.patches.Rectangle(
        (yor - 1, min_cost),
        yod - yor + 1,
        max_cost,
        linewidth=1,
        edgecolor="r",
        facecolor="r",
        alpha=0.1,
    )


def compute_lowest_decade(year: int) -> int:
    """Return the lowest decade of the given year i.e. 2022 -> 2020."""
    return math.floor(year / 10) * 10


def annotate_title(ax: matplotlib.axis, title: str, x=10, y=180, color="black") -> None:
    """Return a"""
    ax.annotate(
        title,
        (0, 0),
        (x, y),
        color=color,
        xycoords="axes points",
        textcoords="offset pixels",
    )


def annotate_subtitle(ax):
    ax.annotate(
        f"Born: {passive.person.yob}, "
        f"Retire: {passive.person.yor}, "
        f"House cost: £{passive.house.purchase_cost / 1000:1.0f}K, "
        f"{passive.mortgage.interest_rate * 100}%/{passive.mortgage.length_years}y Mortgage, "
        f"Area: {passive.house.area_m2}m2, "
        f"Energy Tariff: {passive.energy.tariff * 100}p/kWh, "
        f"Energy CAGR: {passive.energy.cagr * 100:1.0f}%, "
        f"Pension CAGR: {passive.pension.growth_rate * 100:1.0f}%",
        (0, 0),
        (20, 525),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
        fontsize="small",
    )


def annotate_copyright(ax):
    ax.annotate(
        "© Lyon Energy Futures Ltd. (2022)",
        (0, 0),
        (20, 25),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )


def make_outfile_name(root: str, yob: int) -> str:
    outfile = (
        PLOT_DIR
        / f"{root}_{yob}_tariff_{passive.energy.tariff}_cagr_{passive.energy.cagr}.png"
    )
    return outfile
