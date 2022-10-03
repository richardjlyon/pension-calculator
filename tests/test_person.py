import toml

from pension_calculator import ROOT
from pension_calculator.models.person import Person

config = toml.load(f"{ROOT}/app.config.toml")
PENSION_AGE = 67
LIFE_EXPECTANCY = 87


def test_init():
    yob = 1965
    p = Person(yob=yob)
    assert p.yor == yob + PENSION_AGE
    assert p.yod == yob + LIFE_EXPECTANCY
    assert p.years_until_death() == 31
