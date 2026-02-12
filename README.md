# **📧 Email Address Collection – Streamlit Application**

## Overview
- This project is a Streamlit\-based web application designed to collect and log student email creation details into a PostgreSQL database. 

- The application allows students to: 
* Select their college 
* Select their name 
* Indicate whether they have created their email address 
* Provide reasons if not created 
* Submit verified Gmail addresses

- All responses are securely stored in a PostgreSQL database for tracking and reporting. 

## 🚀 How to Run the Application 

From your project directory, run: 

*streamlit run Contact_info.py*
The app will open automatically in your browser. 

## 🧱 Tech Stack 

| Component           | Technology |
| --------------------| -----------|
| Frontend UI         | Streamlit  |
| Backend             | Python     |
| Database            | PostgreSQL |
| ORM / DB Connection | SQLAlchemy |
| Data Handling       | Pandas     |

## 🔐 Database Configuration 

- The app reads database credentials from st.secrets. 
- You must configure the following in your .streamlit/secrets.toml file: 

DB\_HOST = "your\_host" 
DB\_PORT = "your\_port" 
DB\_NAME = "your\_database" 
DB\_USER = "your\_username" 
DB\_PASSWORD = "your\_password" 
 

## 🧩 Application Workflow 

### 1️⃣ Load Dropdown Data 

- Fetches college names from database 
- Fetches student names from database 
- Uses caching for performance optimization 
    

### 2️⃣ User Input Collection 

The form collects: 
- College Name (Required) 
- Student Name (Required) 
- Email Creation Status (Yes / No) 
- If Yes: 
    - Enter Gmail address 
    - Confirm Gmail address 
    - Email validation enforced 
- If No: 
    - Select reasons (multi-select) 
    - Optional custom reason 
    

## ✅ Validations 

The app enforces: 
- Required fields must be filled 
- Email must contain @gmail.com 
- Confirm email must match original email 
- Graceful error messages on failure 
    

## 🗄️ Data Storage 

On successful submission: 
- A timestamp (converted to IST) is generated 
- Data is structured into a Pandas DataFrame 
- Stored in PostgreSQL table: 
        *old.tstt_email_collection_log*  


## 📊 Database Table Fields 

- The following columns are inserted: 

| Column           | Description             |
| ---------------- | ----------------------- |
| timestamp        | Submission time (IST)   |
| college          | Selected college        |
| name             | Student name            |
| email_creation   | Yes / No                |
| reasons          | Comma-separated reasons |
| email_id         | Entered email (or NA)   |
| confirm_email_id | Confirmed email (or NA) |