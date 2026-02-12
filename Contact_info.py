#  Import necessary libraries
import pandas as pd
import streamlit as st
import json
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta, timezone

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


# Function to get the current timestamp
def get_current_timestamp():
  # utc_now = datetime.utcnow()  # Get current UTC time
    utc_now = datetime.now(timezone.utc)  # Get current UTC time as a timezone-aware object
    ist_now = utc_now + timedelta(hours=5, minutes=30)  # Convert to IST
    return ist_now.strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS
    


# Display the PNG image in the top centre of the Streamlit sidebar with custom dimensions
image_path = 'https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/VS-logo.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svVlMtbG9nby5wbmciLCJpYXQiOjE3MjE5NzA3ODUsImV4cCI6MTc1MzUwNjc4NX0.purLZOGk272W80A4OlvnavqVB9u-yExhzpmI3dZrjdM&t=2024-07-26T05%3A13%3A02.704Z'
st.markdown(
    f'<div style="text-align:center"><img src="{image_path}" width="150"></div>',
    unsafe_allow_html=True
)


# Display the title of the Google form
st.markdown(
    "<h1 style='color: black; font-weight: bold;'>Email Address Collection</h1>", 
    unsafe_allow_html=True
)


# Google form Questions

# College Name
# Fetch college names from database
@st.cache_data
def fetch_college_names():
    query = """
        SELECT DISTINCT  college_name FROM old.uploadstelangana_feb_10_0_gi_f_20260207052038 WHERE   college_name IS NOT NULL
        ORDER BY   college_name;
    """
    df = pd.read_sql(query, get_db_engine())
    return df["college_name"].tolist()

# Add college name dropdown on UI
College_names = fetch_college_names()
College=st.selectbox('Select your College Name*',College_names)


# Student Name
# Fetch student names from database
@st.cache_data
def fetch_student_names():
    query = """
        SELECT DISTINCT  full_name FROM old.uploadstelangana_feb_10_0_gi_f_20260207052038 WHERE  full_name IS NOT NULL
        ORDER BY  full_name;
    """
    df = pd.read_sql(query, get_db_engine())
    return df["full_name"].tolist()

# Add student name dropdown on UI
student_names = fetch_student_names()
Name=st.selectbox('Enter your name',student_names)


Email_creation =st.radio('Did you create your email address?*',('Yes','No'))


# Initialize fields with default values
Reasons = []
Email_id = ""
Confirm_Email_id = ""

if Email_creation == "No":
     Reasons=st.multiselect('Please explain the select your reason here',('Network issues','Gmail was asking phone number for verification','PC/Laptop was not available','I did not find time yet, but will do now','Other:'))
     if 'Other:' in Reasons:
        # Display a text box for custom reason if 'Other' is selected
        other_reason = st.text_area("Reason: ")
        if other_reason:
            Reasons.append(other_reason)

if Email_creation == "Yes":
    Email_id=st.text_input("Enter your correct Email address*")
    Confirm_Email_id=st.text_input("Rewrite to confirm your correct Email Address*")

if not Name or not College:
    st.error("Please fill in all the compulsory fields marked with * before proceeding.")
    st.stop()


# Function to store data to database
def store_feedback_postgres(feedback_df):
    engine = get_db_engine()
    feedback_df.to_sql(
        "tstt_email_collection_log",
        engine,
        schema = "old",
        if_exists="append",
        index=False,
        method="multi"
    )


# Function to create feedback dataframe
def create_feedback_dataframe(timestamp,College, Name, Email_creation, Reasons, Email_id, Confirm_Email_id):
    data = {
        'timestamp': timestamp,  # Add the timestamp
        'college': College,
        'name': Name,
        'email_creation': Email_creation,
        'reasons': ', '.join(Reasons) if Reasons else "NA",  # Use "NA" if no reasons provided
        'email_id': Email_id or "NA",  # Use "NA" if no email provided
        'confirm_email_id': Confirm_Email_id or "NA"  # Use "NA" if no confirm email provided
    }
    feedback_df = pd.DataFrame([data])
    return feedback_df


if st.button("Submit"):

    # Basic Validation 
    if not Name or not College:
        st.error("Please fill in all the compulsory fields marked with *.")
        st.stop()

    # Case where email is created
    if Email_creation == "Yes":

        # Test Cases for email created
        if not Email_id or not Confirm_Email_id:
            st.error("Please enter and confirm your email address.")
            st.stop()

        if "@gmail.com" not in Email_id:
            st.error("The email address must contain '@gmail.com'.")
            st.stop()

        if Email_id != Confirm_Email_id:
            st.error("The email addresses do not match.")
            st.stop()


        # All validations passed
        timestamp = get_current_timestamp()
        feedback_df = create_feedback_dataframe(
            timestamp,
            College,
            Name,
            Email_creation,
            Reasons,
            Email_id,
            Confirm_Email_id
        )

        # Store data to our database
        try:
            store_feedback_postgres(feedback_df)
            st.success("Thank you! Your response has been successfully recorded.")
        except Exception as e:
            st.error(f"Failed to store data: {e}")

    # Case where no email was created
    elif Email_creation == "No":

        timestamp = get_current_timestamp()
        feedback_df = create_feedback_dataframe(
            timestamp,
            College,
            Name,
            Email_creation,
            Reasons,
            "",   # Email_id
            ""    # Confirm_Email_id
        )

        # Store data to our database
        try:
            store_feedback_postgres(feedback_df)
            st.success("Thank you! Your response has been successfully recorded.")
        except Exception as e:
            st.error(f"Failed to store data: {e}")

    else:
        st.error("Invalid selection. Please try again.")