import os
import streamlit as st
from cashflow_chart import cashflow_chart
from classes.settingsclass import SettingsState
from investments import investments_content
from plan import plan_content
from settings import settings_form

def is_debug_mode():
    return "DEBUGPY_LAUNCHER_PORT" in os.environ

# Disable file watching if debugging, otherwise leave default
if is_debug_mode():
    os.environ["STREAMLIT_SERVER_FILEWATCHERTYPE"] = "none"
else:
    os.environ.setdefault("STREAMLIT_SERVER_FILEWATCHERTYPE", "auto")

settings = SettingsState.from_session()
settings.enforce()

st.set_page_config(
    layout="wide",
    page_title="Cashflow planner",
)

st.title("Retirement Cashflow")

if settings.dob_changed_event:
    settings.dob_changed(st.session_state["dob"])


if settings.plan_dates_changed_event:
    settings.plan_dates_changed(st.session_state["dob"], st.session_state["plan_start"], st.session_state["plan_end"])

if settings.start_age_changed_event:
    settings.plan_start_changed(st.session_state["start_age"])


if settings.end_age_changed_event:
    settings.plan_end_changed(st.session_state["end_age"])

if settings.pension_changed_event:
    settings.pension_changed(st.session_state["pension_age"], st.session_state["pension_amount"], st.session_state["pension_increase"])

if settings.monthly_changed_event:
    settings.monthly_changed(st.session_state["monthly_income"])
    st.session_state["annual_income"] = float(settings.annual_income)

if settings.annual_changed_event:
    settings.annual_changed(st.session_state["annual_income"])
    st.session_state["monthly_income"] = float(settings.monthly_income)

if settings.inflation_rate_changed_event:
    settings.inflation_rate_changed(st.session_state["inflation_rate"])

settings.enforce()

cashflow_chart()

settings_tab, investment_tab, cashflow_tab = st.tabs(["Settings", "Investments", "Cashflow Plan"])

with settings_tab:
    settings_form()

with investment_tab:
    investments_content()
    
with cashflow_tab:
    plan_content()
    
