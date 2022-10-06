"""
payment_schedule.py

Python script to visualise payment schedules.

streamlit run /Users/richardlyon/Documents/Version\ Controlled/pension-calculator/pension_calculator/web/payment_schedule.py


"""
import pandas as pd
import streamlit as st
import altair as alt

from pension_calculator import CONFIG
from pension_calculator.compute.compute_payment_schedule import (
    ScenarioParams,
    compute_payment_schedule,
)

from pension_calculator.plot.scenario import (
    average_params,
    passive_params,
)

YOB = 1997
YOD = YOB + CONFIG.get("basic").get("life_expectancy")
YOR = YOB + CONFIG.get("basic").get("pension_age") - 1
HOUSE_PURCHASE_YEAR = 2022
HOUSE_PURCHASE_COST = 160000
HOUSE_AREA_M2 = 100
MORTGAGE_DEPOSIT_PERCENT = 0.1
MORTGAGE_INTEREST_RATE = 0.0425
MORTGAGE_LENGTH_YEARS = 40
PENSION_GROWTH_RATE = 0.01
ENERGY_TARIFF = st.slider(
    "Energy Tariff (£/kWh)", value=0.05, min_value=0.01, max_value=0.5, step=0.01
)
ENERGY_CAGR = st.slider(
    "Energy CAGR (%)", value=0.05, min_value=0.0, max_value=1.0, step=0.01
)


average_df = compute_payment_schedule(average_params)
passive_df = compute_payment_schedule(passive_params)
delta_df = passive_df - average_df

mortgage_total = -delta_df["mortgage"].sum()
heating_total = -delta_df["heating"].sum()
pension_total = -delta_df["pension"].sum()
saving = mortgage_total + heating_total + pension_total


source = pd.DataFrame(
    {
        "£": [mortgage_total, heating_total, pension_total, saving],
        "category": ["mortgage", "heating", "pension", "net saving"],
    },
)
bar_chart = alt.Chart(source).mark_bar().encode(y="£:Q", x="category")

st.altair_chart(bar_chart, use_container_width=True)

st.write("Difference")
st.line_chart(delta_df)

st.write("Passive")
st.line_chart(passive_df)

st.write("Average")
st.line_chart(average_df)
