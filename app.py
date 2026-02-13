import streamlit as st
from db.queries import fetch_college_names, fetch_students_by_college, fetch_subject_areas
from utils.helper_functions import create_feedback_dataframe, get_current_timestamp
from storage.store_to_database import store_feedback_postgres
from ui.style import apply_global_styles
from ui.header import header

apply_global_styles()
header()

# Add college name dropdown on UI
College_names = fetch_college_names()
College=st.selectbox(
                    'Select your College Name*',
                    College_names,
                    index=None,
                    placeholder="Select your College Name")

# Add student name dropdown on UI

student_names = fetch_students_by_college(College)

Name = st.selectbox(
    "Enter your Full Name*",
    student_names,
    index=None,
    placeholder="Select your Full Name"
)

# Fetch subject areas
if College and Name:
    subject_areas = fetch_subject_areas(College, Name)

    if len(subject_areas) == 1:
        Subject_area = subject_areas[0]
        st.info(f"Subject Area: **{Subject_area}**")

    elif len(subject_areas) > 1:
        Subject_area = st.selectbox(
            "Select your subject area*",
            subject_areas,
            index=None,
            placeholder="Choose your subject area"
        )

    else:
        st.warning("No subject area found for this student.")


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

if st.button("Submit"):

    # Basic Validation 
    if not Name or not College or not Subject_area:
        st.error("Please fill in all the compulsory fields marked with *.")
        st.stop()

    # Case where email is created
    if Email_creation == "Yes":

        # Test Cases for email created
        if not Email_id or not Confirm_Email_id:
            st.error("Please enter and confirm your email address.")
            st.stop()

        valid_emails = ["@gmail.com", "@proton.me", "@protonmail.com"]

        if not any(Email_id.lower().endswith(domain) for domain in valid_emails):
            st.error(
                "Please enter a valid email address "
                "(@gmail.com, @proton.me, or @protonmail.com)."
            )
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
            Subject_area,
            Email_creation,
            Reasons,
            Email_id,
            Confirm_Email_id
        )

        # Store data to our database
        try:
            st.markdown("---")

            st.success(
                "🎉 **Submission Successful!**\n\n"
            )

            st.balloons()


        except Exception as e:
            st.error(f"Failed to store data: {e}")

    # Case where no email was created
    elif Email_creation == "No":

        timestamp = get_current_timestamp()
        feedback_df = create_feedback_dataframe(
            timestamp,
            College,
            Name,
            Subject_area,
            Email_creation,
            Reasons,
            "",   # Email_id
            ""    # Confirm_Email_id
        )

        # Store data to our database
        try:
            st.markdown("---")

            st.success(
                "🎉 **Submission Successful!**\n\n"
            )

            st.balloons()

        except Exception as e:
            st.error(f"Failed to store data: {e}")

    else:
        st.error("Invalid selection. Please try again.")