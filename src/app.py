import os
import streamlit as st
from classes.settingsclass import SettingsState
from dashboard_charts import cashflow_chart, income_need_chart, pots_chart
from investments import investments_content
from plan import plan_content
from settings import settings_form
import event_handler
from styling import style

def is_debug_mode():
    return "DEBUGPY_LAUNCHER_PORT" in os.environ

# Disable file watching if debugging, otherwise leave default
if is_debug_mode():
    os.environ["STREAMLIT_SERVER_FILEWATCHERTYPE"] = "none"
else:
    os.environ.setdefault("STREAMLIT_SERVER_FILEWATCHERTYPE", "auto")

settings = SettingsState.from_session()
settings.enforce()

style()

st.set_page_config(
    layout="wide",
    page_title="Retirement Cashflow planner",
)

st.title("Retirement Cashflow Planner")

settings.enforce()

event_handler.init_event_handlers(settings)

cashflow_chart_tab, income_chart_tab, pots_chart_tab = st.tabs(["Cashflow", "Income Needed", "Pots"])

with cashflow_chart_tab:
    cashflow_chart()

with income_chart_tab:
    income_need_chart()

with pots_chart_tab:
    pots_chart()

settings_tab, investment_tab, cashflow_tab = st.tabs(["Settings", "Investments", "Cashflow Plan"])

with settings_tab:
    settings_form()

with investment_tab:
    investments_content()
    
with cashflow_tab:
    plan_content()
    
