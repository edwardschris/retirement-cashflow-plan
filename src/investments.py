from decimal import Decimal
import streamlit as st
from classes.settingsclass import SettingsState
from decimal_input import decimal_input

def investments_content():
    settings = SettingsState.from_session()
    settings.enforce()
    st.session_state.setdefault("rental1_value",  settings.rental1_value)
    st.session_state.setdefault("rental1_start",  settings.rental1_start)
    st.session_state.setdefault("rental1_end",  settings.rental1_end)
    st.session_state.setdefault("rental2_value",  settings.rental2_value)
    st.session_state.setdefault("rental2_start",  settings.rental2_start)
    st.session_state.setdefault("rental2_end",  settings.rental2_end)
    st.session_state.setdefault("rent_increase",  settings.rent_increase)

    st.session_state.setdefault("cash_value",  settings.cash_value)
    st.session_state.setdefault("cash_interest",  settings.cash_interest)
    st.session_state.setdefault("isa_value",  settings.isa_value)
    st.session_state.setdefault("isa_growth",  settings.isa_growth)
    st.session_state.setdefault("gia_value",  settings.gia_value)
    st.session_state.setdefault("gia_growth",  settings.gia_growth)
    st.session_state.setdefault("sipp_value",  settings.sipp_value)
    st.session_state.setdefault("sipp_growth",  settings.sipp_growth)

    st.subheader("Investments")

    rental_col, isa_col, other_col, col4 = st.columns([1,1,1,1],border=True)

    with rental_col:
        value1, start1, end1 = st.columns([2,1,1])

        with value1:
            decimal_input(
                "Rental per month",
                min_value=Decimal("0.0"),
                key="rental1_value",
                step= 1,
                on_change=settings.rental_on_change
            )

        with start1:
             st.number_input(
                "Rent Start",
                min_value=settings.start_min,
                max_value=settings.end_age,
                key="rental1_start",
                on_change=settings.rental_on_change
            )
        with end1:
             st.number_input(
                "Rent End",
                min_value=settings.start_min,
                max_value=settings.end_age,
                key="rental1_end",
                on_change=settings.rental_on_change
            )



        value2, start2, end2 = st.columns([2,1,1])

        with value2:
            decimal_input(
                "Rental per month",
                min_value=Decimal("0.0"),
                key="rental2_value",
                step= 1,
                on_change=settings.rental_on_change
            )


        with start2:
            st.number_input(
                "Rent Start",
                min_value=settings.start_min,
                max_value=settings.end_age,
                key="rental2_start",
                on_change=settings.rental_on_change
            )
        with end2:
            st.number_input(
                "Rent End",
                min_value=settings.start_min,
                max_value=settings.end_age,
                key="rental2_end",
                on_change=settings.rental_on_change
            )

        decimal_input(
            "Annual Rent Increase (%)",
            key="rent_increase",
            step= 0.05,
            on_change=settings.rental_on_change
        )

    with isa_col:

        decimal_input(
                "Cash Value",
                min_value=0.0,
                key="cash_value",
                step= 1_000,
                on_change=settings.cash_on_change
            )

        decimal_input(
            "Cash Investment Growth (%)",
            key="cash_interest",
            step= 0.05,
            on_change=settings.cash_on_change
        )

        decimal_input(
                "ISA Value",
                min_value=0.0,
                key="isa_value",
                step= 1_000,
                on_change=settings.isa_on_change
            )

        decimal_input(
            "ISA Investment Growth (%)",
            key="isa_growth",
            step= 0.05,
            on_change=settings.isa_on_change
        )

    with other_col:

        decimal_input(
            "GIA Value",
            min_value=0.0,
            key="gia_value",
            step= 1_000,
            on_change=settings.gia_on_change
        )

        decimal_input(
            "GIA Investment Growth (%)",
            key="gia_growth",
            step= 0.05,
            on_change=settings.gia_on_change
        )

        decimal_input(
            "SIPP Value",
            min_value=0.0,
            key="sipp_value",
            step= 1_000,
            on_change=settings.sipp_on_change
        )

        decimal_input(
            "SIPP Investment Growth (%)",
            key="sipp_growth",
            step= 0.05,
            on_change=settings.sipp_on_change
        )


    return None


