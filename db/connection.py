import streamlit as st
from sqlalchemy import create_engine

# Connect to database
@st.cache_resource
def get_db_engine():
    db_host = st.secrets["DB_HOST"]
    db_port = st.secrets["DB_PORT"]
    db_name = st.secrets["DB_NAME"]
    db_user = st.secrets["DB_USER"]
    db_password = st.secrets["DB_PASSWORD"]

    database_url = (
        f"postgresql+psycopg2://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

    return create_engine(database_url)