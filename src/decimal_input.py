import streamlit as st
from decimal import Decimal
from typing import Callable

def decimal_input(
    label: str,
    key: str,
    value: float | None = 0.00,           # allow None
    min_value: float = 0.00,
    max_value: float = 9_999_999_999.99,
    step: float = 0.01,
    use_decimal: bool = True,
    on_change: Callable | None = None,
):
    """
    Streamlit number input that supports Decimal output and avoids
    'default + session' warnings by only passing value= on first creation.
    """
    kwargs = dict(
        key=key,
        min_value=float(min_value),
        max_value=float(max_value),
        step=float(step),
        format="%.2f",
        on_change=on_change,
    )

    # Only pass a default value if this key is not already in session
    # and the provided value is not None
    if key not in st.session_state and value is not None:
        kwargs["value"] = float(value)

    amount = st.number_input(label, **kwargs)

    return Decimal(str(amount)) if use_decimal else amount