from pension_calculator.plot.plot_payment_schedule import plot as plot_payment_schedule
from pension_calculator.plot.plot_payment_schedule_explainer import (
    plot as plot_payment_schedule_explainer,
)


def main():
    plot_payment_schedule()
    plot_payment_schedule_explainer()


if __name__ == "__main__":
    main()
