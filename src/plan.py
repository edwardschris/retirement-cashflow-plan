import streamlit as st
from classes.settingsclass import SettingsState

def plan_content():
    settings = SettingsState.from_session()
    settings.enforce()

    st.subheader("Cashflow Plan")

    df = settings.cashflow()
    st.dataframe(df)

    return None

  