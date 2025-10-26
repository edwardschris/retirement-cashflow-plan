from decimal import Decimal
import streamlit as st
from classes.settingsclass import SettingsState
import numpy as np
import pandas as pd

def plan_content():
    settings = SettingsState.from_session()
    settings.enforce()

    st.subheader("Cashflow Plan")
    st.dataframe(settings.cashflow())

    return None

  