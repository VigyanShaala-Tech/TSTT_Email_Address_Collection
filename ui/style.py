import streamlit as st

def apply_global_styles():
    st.markdown(
        """
        <style>
        /* ===============================
        Selectbox (Dropdown)
        =============================== */
        div[data-baseweb="select"] > div {
            background-color: #cccccc !important;
            border-radius: 8px;
        }

        div[data-baseweb="select"] span {
            color: #555555;
        }

        /* ===============================
        Text Input (Email, Name, etc.)
        =============================== */
        div[data-baseweb="input"] > div {
            background-color: #cccccc !important;
            border-radius: 8px;
        }

        div[data-baseweb="input"] input {
            background-color: #cccccc !important;
            color: #000000;
        }

        /* Placeholder text */
        div[data-baseweb="input"] input::placeholder {
            color: #6c6c6c;
        }
        </style>
        """,
        unsafe_allow_html=True
    )