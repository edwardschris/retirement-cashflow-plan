import altair as alt
import pandas as pd
import streamlit as st
from classes.settingsclass import SettingsState

def cashflow_chart():
    settings = SettingsState.from_session()
    settings.enforce()
    df = settings.cashflow()

    numeric_cols = ["Age", "Income", "Pension", "Short", "Rental",  "Cash Take", "ISA Take",]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Age"]).sort_values("Age")

    stacked = True

    df_melted = df.melt(
        id_vars="Age",
        value_vars=["Short", "Pension", "Rental", "Cash Take", "ISA Take", "SIPP Take", "GIA Take"],
        var_name="Category",
        value_name="Amount"
    )

    category_order = [
        "Pension", "Rental", "Cash Take", "ISA Take",
        "Short", "SIPP Take", "GIA Take"
    ]

    color_scale = alt.Scale(
        domain=category_order,
        range=[
            "#1f77b4",  # Pension - blue
            "#9467bd",  # Rental - purple
            "#17becf",  # Cash Take - teal
            "#8c564b",  # ISA Take - brown
            "#d62728",  # Short - bright red (stands out)
            "#ff7f0e",  # SIPP Take - orange
            "#bcbd22"   # GIA Take - olive/yellow-green
        ]
    )

    base = alt.Chart(df_melted).mark_bar()

    if stacked:
        chart = base.encode(
            x=alt.X("Age:O", title="Age"),
            y=alt.Y("Amount:Q", title="Amount (£)", stack="zero"),
            color=alt.Color("Category:N", title="Category", sort=category_order, scale=color_scale,),
            order=alt.Order("Category", sort="ascending"),
            tooltip=["Age", "Category", alt.Tooltip("Amount:Q", format=",.2f")]
        )
    else:
        chart = base.encode(
            x=alt.X("Age:O", title="Age"),
            xOffset=alt.X("Category:N", sort=category_order),
            y=alt.Y("Amount:Q", title="Amount (£)"),
            color=alt.Color("Category:N", title="Category", sort=category_order, scale=color_scale, legend=alt.Legend(orient="bottom")),
            tooltip=["Age", "Category", alt.Tooltip("Amount:Q", format=",.2f")]
        )

    st.altair_chart(chart.properties(height=200), use_container_width=True)

    return None

def income_need_chart():
    settings = SettingsState.from_session()
    settings.enforce()
    df = settings.cashflow()

    numeric_cols = ["Age", "Income"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Age"]).sort_values("Age")

    df_melted = df.melt(
        id_vars="Age",
        value_vars=["Income"],
        var_name="Category",
        value_name="Amount"
    )

    category_order = [
        "Income"
    ]

    color_scale = alt.Scale(
        domain=category_order,
        range=[
            "#1f77b4",
        ]
    )

    base = alt.Chart(df_melted).mark_bar()

    chart = base.encode(
        x=alt.X("Age:O", title="Age"),
        y=alt.Y("Amount:Q", title="Amount (£)", stack="zero"),
        color=alt.Color("Category:N", title="Category", sort=category_order, scale=color_scale,),
        order=alt.Order("Category", sort="ascending"),
        tooltip=["Age", "Category", alt.Tooltip("Amount:Q", format=",.2f")]
    )

    st.altair_chart(chart.properties(height=200), use_container_width=True)

    return None

def pots_chart():
    settings = SettingsState.from_session()
    settings.enforce()
    df = settings.cashflow()

    numeric_cols = ["Age", "Short", "Cash End", "ISA End", "SIPP End", "GIA End",]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Age"]).sort_values("Age")

    stacked = True

    df_melted = df.melt(
        id_vars="Age",
        value_vars=["Deficit", "Cash End", "ISA End", "SIPP End", "GIA End"],
        var_name="Category",
        value_name="Amount"
    )

    category_order = [
        "Cash End", "ISA End",
         "SIPP End", "GIA End", "Deficit"
    ]

    color_scale = alt.Scale(
        domain=category_order,
        range=[
            "#17becf",  # Cash Take - teal
            "#8c564b",  # ISA Take - brown
            "#ff7f0e",  # SIPP Take - orange
            "#bcbd22",  # GIA Take - olive/yellow-green
            "#d62728",  # Short - bright red (stands out)
        ]
    )

    base = alt.Chart(df_melted).mark_bar()

    if stacked:
        chart = base.encode(
            x=alt.X("Age:O", title="Age"),
            y=alt.Y("Amount:Q", title="Amount (£)", stack="zero"),
            color=alt.Color("Category:N", title="Category", sort=category_order, scale=color_scale,),
            order=alt.Order("Category", sort="ascending"),
            tooltip=["Age", "Category", alt.Tooltip("Amount:Q", format=",.2f")]
        )
    else:
        chart = base.encode(
            x=alt.X("Age:O", title="Age"),
            xOffset=alt.X("Category:N", sort=category_order),
            y=alt.Y("Amount:Q", title="Amount (£)"),
            color=alt.Color("Category:N", title="Category", sort=category_order, scale=color_scale, legend=alt.Legend(orient="bottom")),
            tooltip=["Age", "Category", alt.Tooltip("Amount:Q", format=",.2f")]
        )

    st.altair_chart(chart.properties(height=200), use_container_width=True)

    return None