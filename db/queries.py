import streamlit as st
import pandas as pd
from db.connection import get_db_engine

# Fetch college names from database
@st.cache_data
def fetch_college_names():
    query = """
        SELECT DISTINCT  college_name FROM old.telangana_inc_10_0_gi_20260604110952 WHERE   college_name IS NOT NULL
        ORDER BY   college_name;
    """
    df = pd.read_sql(query, get_db_engine())
    return df["college_name"].tolist()

@st.cache_data
def fetch_students_by_college(college_name):
    query = """
        SELECT DISTINCT full_name
        FROM old.telangana_inc_10_0_gi_20260604110952
        WHERE college_name = %(college_name)s
          AND full_name IS NOT NULL
        ORDER BY full_name
    """

    df = pd.read_sql(
        query,
        get_db_engine(),
        params={"college_name": college_name}
    )

    return df["full_name"].tolist()

# Fetch subject area as per the college name and student name
@st.cache_data
def fetch_subject_areas(college_name, full_name):
    query = """
        SELECT DISTINCT subject_area_abbreviation
        FROM old.telangana_inc_10_0_gi_20260604110952
        WHERE college_name = %(college_name)s
          AND full_name = %(full_name)s
          AND subject_area_abbreviation IS NOT NULL
        ORDER BY subject_area_abbreviation
    """

    df = pd.read_sql(
        query,
        get_db_engine(),
        params={
            "college_name": college_name,
            "full_name": full_name
        }
    )

    return df["subject_area_abbreviation"].tolist()
