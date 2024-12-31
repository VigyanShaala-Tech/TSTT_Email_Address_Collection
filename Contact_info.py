#Import necessary libraries
import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import requests
from io import StringIO  # Import StringIO directly from the io module
from io import BytesIO
from google.oauth2 import service_account
import json
import numpy as np
from sqlalchemy import create_engine


# Display the PNG image in the top centre of the Streamlit sidebar with custom dimensions
image_path = 'https://twetkfnfqdtsozephdse.supabase.co/storage/v1/object/sign/stemcheck/VS-logo.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdGVtY2hlY2svVlMtbG9nby5wbmciLCJpYXQiOjE3MjE5NzA3ODUsImV4cCI6MTc1MzUwNjc4NX0.purLZOGk272W80A4OlvnavqVB9u-yExhzpmI3dZrjdM&t=2024-07-26T05%3A13%3A02.704Z'
st.markdown(
    f'<div style="text-align:center"><img src="{image_path}" width="150"></div>',
    unsafe_allow_html=True
)

#Display the title of the Google form
st.markdown(
    "<h1 style='color: black; font-weight: bold;'>Email Address Collection</h1>", 
    unsafe_allow_html=True
)


#Google form Questions
Name=st.text_input("Enter your full name*")
College_names = ["TSWRD Pharmacy College, Mahbubabad","TSWRDC & PGC, Budvel","TSWRDC Khammam","TSWRDC Mahendrahills","TSWRDC Nirmal","TSWRDC Nizamabad","TSWRDC Siddipet","TSWRDCW Adilabad","TSWRDCW Armoor",
"TSWRDCW Bhupalpally","TSWRDCW Jagathgirigutta","TSWRDCW Jagtial","TSWRDCW Kamareddy","TSWRDCW Karimnagar","TSWRDCW Kothagudem","TSWRDCW Mahbubnagar","TSWRDCW Mancherial","TSWRDCW Nagarkurnool","TSWRDCW Nalgonda",
"TSWRDCW Sirsilla","TSWRDCW Suryapet","TSWRDCW Vikarabad","TSWRDCW Wanaparthy","TSWRDCW Warangal east","TSWRDCW Warangal West","TTWRDC Asifabad(Women)","TTWRDC Dammapeta(women)","TTWRDC Devarakonda(women)","TTWRDC Janagaon(women)","TTWRDC Khammam(Women)"
,"TTWRDC Kothagudem(women)","TTWRDC Mahabubabad(women)","TTWRDC Mahabubnagar(Women)","TTWRDC Medak(Women)","TTWRDC Mulugu(Women)","TTWRDC Nizamabad(Women)","TTWRDC Shadnagar(Women)","TTWRDC Siricilla(Women)","TTWRDC Suryapeta(Women)",
"TTWRDC Utnoor(Women)"]
College=st.selectbox('Select your College Name*',College_names)
Email_id=st.text_input("Enter your correct Email address*")
Confirm_Email_id=st.text_input("Rewrite to confirm your correct Email Address*")

if not Name or not College:
    st.error("Please fill in all the compulsory fields marked with * before proceeding.")
    st.stop()


def create_feedback_dataframe(Name,College,Email_id,Confirm_Email_id):
    data = {
        'Name': Name,
        'College':College,
        'Email_id':Email_id,
        "Confirm_Email_id":Confirm_Email_id
    }

    feedback_df = pd.DataFrame([data])
    return feedback_df
    
feedback_df=create_feedback_dataframe(Name,College,Email_id,Confirm_Email_id)


# Create a button in Streamlit
combined_button_text = "Submit"
if st.button(combined_button_text):
    if Email_id and Confirm_Email_id:  # Ensure both fields are filled
        if Email_id == Confirm_Email_id:  # Check if both email addresses match
            if "@gmail.com" in Email_id:  # Check if the email contains '@gmail.com'
                st.success("Thank you for your response.")
            else:
                st.error("The email address must contain '@gmail.com'.")
        else:
            st.error("The email addresses do not match.")
    else:
        st.error("Please fill in both fields.")


    # AWS RDS database connection info
    username = st.secrets['DB_USERNAME']
    password = st.secrets['DB_PASSWORD']
    host = st.secrets['DB_ENDPOINT']
    port = st.secrets['DB_PORT']  # Replace with your MySQL port if different
    database_name = st.secrets['DB_NAME']
    
    #db_username = 'vigyan'
    #db_password = '321#Dev'
    #db_name = 'vigyan'
    #db_port = '3306'
    #db_endpoint = '35.154.220.255'


    # Create the connection string
    engine_str = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}"

    # Create the SQLAlchemy engine
    engine = create_engine(engine_str)
    


    # Store the DataFrame in the database table
    table_name = 'tstt_email_collection'  # Replace with your table name
    data_to_insert = feedback_df.values.tolist()
    data_to_insert = pd.DataFrame(data_to_insert,columns=feedback_df.columns)
    data_to_insert.to_sql(name=table_name, con=engine, if_exists='append', index=False)


