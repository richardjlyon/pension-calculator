from toml_config.core import Config

my_config = Config('app.config.toml')

if __name__ == "__main__":
    my_config = Config('app.config.toml')
    my_config.add_section('basic').set(
        pension_age=67,
        life_expectancy=87,
        average_house_size_m2=67.8,
        variable_unit_cost_electricity=0.143,
        variable_unit_cost_gas=0.044,
    )
    my_config.add_section('energy_use').set(
        leaky=300,
        old=200,
        modern=150,
        new=100,
        low=50,
        passive=15
    )
    my_config.add_section('CAGR').set(
        gas=0.05,
        electricity=0.08,
    )