from decimal import Decimal
import pandas as pd
import streamlit as st
from classes.settingsclass import SettingsState
from decimal_input import decimal_input

def settings_form():
    settings = SettingsState.from_session()
    settings.enforce()
    st.session_state.setdefault("dob",  settings.dob)
    st.session_state.setdefault("plan_start",  settings.plan_start)
    st.session_state.setdefault("plan_end",  settings.plan_end)
    st.session_state.setdefault("start_age",  settings.start_age)
    st.session_state.setdefault("end_age",  settings.end_age)
    st.session_state.setdefault("inflation_rate",  settings.inflation_rate)

    st.subheader("Settings")

    plan_col, pension_col, income_tab = st.columns([1,1,1],border=True)

    with plan_col:
        # --- Date of Birth ---
        st.date_input(
            "Date of Birth", 
            format="DD/MM/YYYY",
            key="dob",
            on_change=settings.dob_on_change,
        )

        age1_col, date1_col = st.columns([1,1])

        with age1_col:
            # --- Start Age ---
            start_age = st.number_input(
                "Plan Start Age",
                min_value=settings.start_min,
                max_value=settings.start_max,
                key="start_age",
                on_change=settings.start_age_on_change
            )

        with date1_col:
            st.date_input(
                "Plan Start", 
                format="DD/MM/YYYY",
                key="plan_start",
                on_change=settings.plan_date_on_change,
            )

        age2_col, date2_col = st.columns([1,1])

        with age2_col:
            # --- End Age ---
            st.number_input(
                "Plan End Age",
                min_value=50,
                max_value=100,
                key="end_age",
                on_change=settings.end_age_on_change
            )

        with date2_col:
             st.date_input(
                 "Plan End",
                format="DD/MM/YYYY",
                key="plan_end",
                on_change=settings.plan_date_on_change,
            )

    with pension_col:

        st.number_input(
            "State Pension Age",
            min_value=60,
            max_value=100,
            value= settings.state_pension_age,
            key="pension_age",
            on_change=settings.on_pension_change
        )

        decimal_input(
            "Current Annual State Pension (£)",
            value= float(settings.state_pension_current_amount),
            key="pension_amount",
            step= 500,
            on_change=settings.on_pension_change
        )

        decimal_input(
            "Annual State Pension Increase (%)",
            value= float(settings.state_pension_annual_increase),
            key="pension_increase",
            step= 0.05,
            on_change=settings.on_pension_change
        )


    with income_tab:
        income1_col, _ = st.columns([1,1])

        with income1_col:
            decimal_input(
                "Required Monthly Income (£)",
                min_value=0.0,
                value= float(settings.monthly_income),
                key="monthly_income",
                step= 125,
                on_change=settings.monthly_on_change
            )

        income2_col, inflation_rate_col2= st.columns([1,1])

        annual_value = st.session_state.get("annual_income", float(settings.annual_income))

        with income2_col:
            decimal_input(
                "Required Annual Income (£)",
                min_value=0.0,
                value=float(annual_value),
                key="annual_income",
                step= 500,
                on_change=settings.annual_on_change
            )

        with inflation_rate_col2:
            decimal_input(
                "Inflation Rate (%)",
                min_value=0.0,
                max_value=100.0,
                key="inflation_rate",
                step= 0.05,
                on_change=settings.inflation_rate_on_change
            )

        df = settings.reducedIncome.copy()
        income = float(settings.annual_income)
        df["salary"] = df["percentage"].apply(lambda x: (income * (1 - x / 100)) / 12)
        df["salary_display"] = df["salary"].apply(lambda x: f"£{x:,.0f}")

        settings.reducedIncome = st.data_editor(
            df,
            column_order=["age", "percentage", "salary_display"], 
            column_config= {
                "age": st.column_config.NumberColumn("Age", min_value=settings.start_age, step=1, format="%d"),
                "percentage": st.column_config.NumberColumn("%", min_value=0, max_value=100, step=1, format="%d%%"),
                "salary_display": st.column_config.TextColumn("Income (£)", disabled=True,)
            },
            hide_index=True
        )

        if st.button("🔄 Recalculate Incomes", ):
            st.rerun()

    settings.enforce()

    return None