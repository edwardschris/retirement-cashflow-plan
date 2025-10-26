import streamlit as st

def style():
    st.markdown("""
    <style>
    /* --- Reduce overall vertical space between elements --- */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    div.row-widget.stRadio, div.row-widget.stCheckbox, div.row-widget.stSelectbox {
        margin-bottom: 0.3rem;
    }

    /* --- Reduce spacing after titles/subheaders --- */
    h1, h2, h3, h4, h5, h6 {
        margin-bottom: 0.25em;
        margin-top: 0.25em;
    }

    /* --- Custom title & subheader font sizes --- */
    h1 {
        font-size: 1.8rem !important;   /* Default ~2.5rem */
    }
    h2 {
        font-size: 1.3rem !important;   /* Default ~1.6rem */
    }
    h3 {
        font-size: 1.1rem !important;
    }
                
    </style>
    """, unsafe_allow_html=True)

