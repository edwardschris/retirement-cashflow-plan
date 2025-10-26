import streamlit as st
from classes.settingsclass import SettingsState
from decimal_input import decimal_input

def investments_content():
    settings = SettingsState.from_session()

    st.subheader("Investments")

    rental_col, isa_col, other_col, col4 = st.columns([1,1,1,1],border=True)

    with rental_col:
        value1, start1, end1 = st.columns([2,1,1])

        with value1:
            rental1_value = decimal_input(
                "Rental per month",
                min_value=0.0,
                value= float(settings.rental1_value),
                key="rental1_value",
                step= 1,
            )

        with start1:
            rental1_start = st.number_input(
                "Rent Start",
                min_value=settings.start_min,
                max_value=settings.end_age,
                value=settings.rental1_start,
                key="rental1_start",
            )
        with end1:
            rental1_end = st.number_input(
                "Rent End",
                min_value=settings.start_min,
                max_value=settings.end_age,
                value=settings.rental1_end,
                key="rental1_end",
            )



        value2, start2, end2 = st.columns([2,1,1])

        with value2:
            rental2_value = decimal_input(
                "Rental per month",
                min_value=0.0,
                value= float(settings.rental2_value),
                key="rental2_value",
                step= 1,
            )


        with start2:
            rental2_start = st.number_input(
                "Rent Start",
                value=settings.rental2_start,
                key="rental2_start",
            )
        with end2:
            rental2_end = st.number_input(
                "Rent End",
                value=settings.rental2_end,
                key="rental2_end",
            )

        rent_increase = decimal_input(
            "Annual Rent Increase (%)",
            value= float(settings.rent_increase),
            key="rent_increase",
            step= 0.05
        )

        settings.rental1_value = rental1_value
        settings.rental1_start = rental1_start
        settings.rental1_end = rental1_end

        settings.rental2_value = rental2_value
        settings.rental2_start = rental2_start
        settings.rental2_end = rental2_end

        settings.rent_increase = rent_increase


    with isa_col:

        cash_value = decimal_input(
                "Cash Value",
                min_value=0.0,
                value= float(settings.cash_value),
                key="cash_value",
                step= 1_000,
            )

        cash_interest = decimal_input(
            "Cash Investment Growth (%)",
            value= float(settings.cash_interest),
            key="cash_interest",
            step= 0.05
        )

        isa_value = decimal_input(
                "ISA Value",
                min_value=0.0,
                value= float(settings.isa_value),
                key="isa_value",
                step= 1_000,
            )

        isa_growth = decimal_input(
            "ISA Investment Growth (%)",
            value= float(settings.isa_growth),
            key="isa_growth",
            step= 0.05
        )

        settings.cash_value = cash_value
        settings.cash_interest = cash_interest

        settings.isa_value = isa_value
        settings.isa_growth = isa_growth

    with other_col:

        gia_value = decimal_input(
                "GIA Value",
                min_value=0.0,
                value= float(settings.gia_value),
                key="gia_value",
                step= 1_000,
            )

        gia_growth = decimal_input(
            "GIA Investment Growth (%)",
            value= float(settings.gia_growth),
            key="gia_growth",
            step= 0.05
        )

        sipp_value = decimal_input(
                "SIPP Value",
                min_value=0.0,
                value= float(settings.sipp_value),
                key="sipp_value",
                step= 1_000,
            )

        sipp_growth = decimal_input(
            "SIPP Investment Growth (%)",
            value= float(settings.sipp_growth),
            key="sipp_growth",
            step= 0.05
        )

        settings.sipp_value = sipp_value
        settings.sipp_growth = sipp_growth

        settings.gia_value = gia_value
        settings.gia_growth = gia_growth



    return None


