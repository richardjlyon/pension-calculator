from pension_calculator.plot.plot_payment_schedule import plot as plot_payment_schedule
from pension_calculator.plot.plot_payment_schedule_explainer import (
    plot as plot_payment_schedule_explainer,
)
from pension_calculator.plot.plot_relative_energy_cost_4_panel import (
    plot as relative_energy_cost_4_panel,
)
from pension_calculator.plot.plot_relative_energy_cost_single import (
    plot as relative_energy_cost_single,
)


def main():
    plot_payment_schedule()
    plot_payment_schedule_explainer()
    relative_energy_cost_4_panel()
    relative_energy_cost_single()


if __name__ == "__main__":
    main()
