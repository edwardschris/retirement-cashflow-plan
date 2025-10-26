import streamlit as st
from classes.settingsclass import SettingsState

def init_event_handlers(settings: SettingsState):
    if settings.dob_changed_event:
        settings.dob_changed(st.session_state["dob"])

    if settings.plan_dates_changed_event:
        settings.plan_dates_changed(st.session_state["dob"], st.session_state["plan_start"], st.session_state["plan_end"])

    if settings.start_age_changed_event:
        settings.start_age_changed(st.session_state["start_age"])

    if settings.end_age_changed_event:
        settings.end_age_changed(st.session_state["end_age"])

    if settings.pension_changed_event:
        settings.pension_changed(st.session_state["pension_age"], st.session_state["pension_amount"], st.session_state["pension_increase"])

    if settings.monthly_changed_event:
        settings.monthly_changed(st.session_state["monthly_income"])

    if settings.annual_changed_event:
        settings.annual_changed(st.session_state["annual_income"])

    if settings.inflation_rate_changed_event:
        settings.inflation_rate_changed(st.session_state["inflation_rate"])

    if settings.rental_changed_event:
        settings.rental_changed(
            st.session_state["rental1_value"], st.session_state["rental1_start"], st.session_state["rental1_end"],
            st.session_state["rental2_value"], st.session_state["rental2_start"], st.session_state["rental2_end"],
            st.session_state["rent_increase"]
        )

    if settings.cash_changed_event:
        settings.cash_changed(st.session_state["cash_value"], st.session_state["cash_interest"])

    if settings.isa_changed_event:
        settings.isa_changed(st.session_state["isa_value"], st.session_state["isa_growth"])

    if settings.gia_changed_event:
        settings.gia_changed(st.session_state["gia_value"], st.session_state["gia_growth"])

    if settings.sipp_changed_event:
        settings.sipp_changed(st.session_state["sipp_value"], st.session_state["sipp_growth"])
    
    return None