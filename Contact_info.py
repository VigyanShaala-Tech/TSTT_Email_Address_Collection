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
"TSWRDCW Bhupalpally","TSWRDCW Jagathgirigutta","TSWRDCW Jagtial","TSWRDCW Kamareddy","TSWRDCW Karimnagar","TSWRDCW Kothagudem","TSWRDCW Mahbubnagar","TSWRDCW Mancherial","TSWRDCW Medak","TSWRDCW Nagarkurnool","TSWRDCW Nalgonda",
"TSWRDCW Sirsilla","TSWRDCW Suryapet","TSWRDCW Vikarabad","TSWRDCW Wanaparthy","TSWRDCW Warangal east","TSWRDCW Warangal West","TTWRDC Asifabad(Women)","TTWRDC Dammapeta(women)","TTWRDC Devarakonda(women)","TTWRDC Janagaon(women)","TTWRDC Khammam(Women)"
,"TTWRDC Kothagudem(women)","TTWRDC Mahabubabad(women)","TTWRDC Mahabubnagar(Women)","TTWRDC Medak(Women)","TTWRDC Mulugu(Women)","TTWRDC Nizamabad(Women)","TTWRDC Shadnagar(Women)","TTWRDC Siricilla(Women)","TTWRDC Suryapeta(Women)",
"TTWRDC Utnoor(Women)","MJBTBC Keesara","MJBTBC Wargal","MJBTBC Nizamabad","MJBTBC Khamam","MJBTBC Ghanpur"]
College=st.selectbox('Select your College Name*',College_names)
Email_id=st.text_input("Enter your correct Email address*")
Confirm_Email_id=st.text_input("Rewrite to confirm your correct Email Address*")

if not Name or not College:
    st.error("Please fill in all the compulsory fields marked with * before proceeding.")
    st.stop()


#Creates a feedback DataFrame.
def create_feedback_dataframe(Name, College, Email_id, Confirm_Email_id):
    data = {
        'Name': Name,
        'College': College,
        'Email_id': Email_id,
        "Confirm_Email_id": Confirm_Email_id
    }
    feedback_df = pd.DataFrame([data])
    return feedback_df
    


# Button to submit feedback
if st.button("Submit"):
    if Email_id and Confirm_Email_id:  # Ensure both fields are filled
        if Email_id == Confirm_Email_id:  # Check if email addresses match
            if "@gmail.com" in Email_id:  # Check for '@gmail.com'
                # Create feedback DataFrame
                feedback_df = create_feedback_dataframe(Name, College, Email_id, Confirm_Email_id)

                # Fetch service account credentials from Supabase or other storage
                supabase_credentials_url = st.secrets['SUPABASE_CREDENTIALS'] 
                response = requests.get(supabase_credentials_url)

                if response.status_code == 200:
                    try:
                        # Parse the service account credentials
                        service_account_info = response.json()

                        # Authenticate with Google Sheets
                        creds = service_account.Credentials.from_service_account_info(
                            service_account_info,
                            scopes=['https://www.googleapis.com/auth/spreadsheets']
                        )
                        client = gspread.authorize(creds)

                        # Open the Google Sheet
                        sheet_key = st.secrets['SH_Contact_info'] 
                        sheet = client.open_by_key(sheet_key).sheet1

                        # Get existing records from the sheet
                        existing_records = sheet.get_all_values()

                        if existing_records:
                            # Extract headers
                            headers = existing_records[0]

                            # Ensure the headers match the DataFrame
                            if headers == feedback_df.columns.tolist():
                                # Convert DataFrame to list of lists and append to the sheet
                                feedback_records = feedback_df.values.tolist()
                                sheet.append_rows(feedback_records, value_input_option='RAW')
                                st.success("Thank you! Your response has been successfully recorded.")
                            else:
                                st.error("Sheet headers do not match the expected format.")
                        else:
                            st.error("No headers found in the sheet. Please ensure the sheet has headers.")
                    except Exception as e:
                        st.error(f"An error occurred while appending data: {e}")
                else:
                    st.error("Failed to fetch service account credentials. Please check your setup.")
            else:
                st.error("The email address must contain '@gmail.com'.")
        else:
            st.error("The email addresses do not match.")
    else:
        st.error("Please fill in all the fields.")


