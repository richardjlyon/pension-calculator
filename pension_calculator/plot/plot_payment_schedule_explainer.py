"""Generates a plot that explains how the mortgage, heating and pension costs are built up."""
import matplotlib
import matplotlib.pyplot as plt

from pension_calculator import PLOT_DIR
from pension_calculator.compute.compute_payment_schedule import compute_payment_schedule
from pension_calculator.plot.helpers import (
    annotate_title,
    compute_lowest_decade,
    currency,
    retirement_rectangle,
)
from pension_calculator.plot.scenario import (
    HOUSE_PURCHASE_YEAR,
    YOB,
    YOD,
    YOR,
    average_params,
    passive_params,
)


def main():

    average_df = compute_payment_schedule(average_params)
    passive_df = compute_payment_schedule(passive_params)

    # Compute pension draw down from retirement to death.

    pension_final_value_average = average_df["pension_value"].loc[YOR]
    pension_final_value_passive = passive_df["pension_value"].loc[YOR]

    average_df["pension_value"].loc[YOR + 1 : YOD] = (
        pension_final_value_average - average_df["heating"].loc[YOR + 1 : YOD].cumsum()
    )
    passive_df["pension_value"].loc[YOR + 1 : YOD] = (
        pension_final_value_passive - passive_df["heating"].loc[YOR + 1 : YOD].cumsum()
    )

    # Initialise a four panel figure.

    fig = plt.figure()
    width_inches = 10
    height_inches = width_inches * 9 / 16
    fig.set_size_inches(width_inches, height_inches)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        f"Pension, mortgage, and heating annual payments for a Passive house relative to average ({HOUSE_PURCHASE_YEAR}-{YOD})",
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

    for ax in axes:
        ax.yaxis.set_major_formatter(currency)
        ax.set_ylim([0, max_cost])
        ax.set_xlim([min_year, max_year])

    # Top left: mortgage.

    annotate_title(ax1, "Mortgage payments")
    annotate_title(ax1, "RETIREMENT", x=250, y=10, color="tab:red")
    ax1.add_patch(retirement_rectangle(YOR, YOD, max_cost))

    passive_df["mortgage"].plot(ax=ax1, color="tab:orange", label="passive")
    average_df["mortgage"].plot(
        ax=ax1, color="tab:orange", linestyle="dashed", label="average"
    )
    ax1.fill_between(
        average_df.index,
        average_df["mortgage"],
        passive_df["mortgage"],
        color="tab:orange",
        alpha=0.25,
    )

    # Top right: heating cost.

    annotate_title(ax2, "Heating cost")
    ax2.add_patch(retirement_rectangle(YOR, YOD, max_cost))

    passive_df["heating"].plot(ax=ax2, color="tab:blue", label="passive")
    average_df["heating"].plot(
        ax=ax2, color="tab:blue", linestyle="dashed", label="average"
    )
    ax2.fill_between(
        average_df.index,
        average_df["heating"],
        passive_df["heating"],
        color="tab:blue",
        alpha=0.25,
    )

    # Bottom left: pension cost.

    annotate_title(ax3, "Heating pension - payments")
    ax3.add_patch(retirement_rectangle(YOR, YOD, max_cost))

    passive_df["pension"].plot(ax=ax3, color="tab:green", label="passive")
    average_df["pension"].plot(
        ax=ax3, color="tab:green", linestyle="dashed", label="average"
    )
    ax3.fill_between(
        average_df.index,
        average_df["pension"],
        passive_df["pension"],
        color="tab:green",
        alpha=0.25,
    )

    # Bottom right: pension explainer.

    annotate_title(ax4, "Heating pension - value")
    max_cost = average_df[["heating", "pension_value"]].max(axis=1).max() * 1.2
    ax4.set_ylim([0, max_cost])
    ax4.add_patch(retirement_rectangle(YOR, YOD, max_cost))

    passive_df["pension_value"].plot(ax=ax4, color="tab:green", label="passive")
    average_df["pension_value"].plot(
        ax=ax4, color="tab:green", linestyle="dashed", label="average"
    )
    ax4.fill_between(
        average_df.index,
        average_df["pension_value"],
        passive_df["pension_value"],
        color="tab:green",
        alpha=0.25,
    )

    # Annotate "house pension"

    rect = matplotlib.patches.Rectangle(
        (min_year, pension_final_value_passive),
        max_year - min_year,
        pension_final_value_average - pension_final_value_passive,
        linewidth=1,
        edgecolor="purple",
        facecolor="tab:purple",
        alpha=0.1,
    )
    ax4.add_patch(rect)
    annotate_title(ax4, "'House pension'", y=130, color="tab:purple")

    for ax in axes:
        ax.legend(loc="upper right")

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
        (20, 525),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
        fontsize="small",
    )

    # Copyright footer.

    ax3.annotate(
        "© Lyon Energy Futures Ltd. (2022)",
        (0, 0),
        (20, 25),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )

    outfile = (
        PLOT_DIR
        / f"payment_shedule_explainer_{YOB}_tarrif_{passive_params.energy_tariff}_cagr_{passive_params.energy_cagr}.png"
    )
    plt.savefig(outfile)
    print(f"\nSaved file to {outfile}")

    plt.show()


if __name__ == "__main__":
    main()
