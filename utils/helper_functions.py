from datetime import datetime, timedelta, timezone
import pandas as pd
import streamlit as st


# Function to get the current timestamp
def get_current_timestamp():
  # utc_now = datetime.utcnow()  # Get current UTC time
    utc_now = datetime.now(timezone.utc)  # Get current UTC time as a timezone-aware object
    ist_now = utc_now + timedelta(hours=5, minutes=30)  # Convert to IST
    return ist_now.strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS

# Function to create feedback dataframe
def create_feedback_dataframe(timestamp, College, Name, Subject_area, Email_creation, Reasons, Email_id, Confirm_Email_id):
    data = {
        'timestamp': timestamp,  # Add the timestamp
        'college': College,
        'name': Name,
        'subject_area': Subject_area if Subject_area else "NA",
        'email_creation': Email_creation,
        'reasons': ', '.join(Reasons) if Reasons else "NA",  # Use "NA" if no reasons provided
        'email_id': Email_id or "NA",  # Use "NA" if no email provided
        'confirm_email_id': Confirm_Email_id or "NA"  # Use "NA" if no confirm email provided
    }
    feedback_df = pd.DataFrame([data])
    return feedback_df
