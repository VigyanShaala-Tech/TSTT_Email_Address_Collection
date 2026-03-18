# **📧 Email Address Collection – Streamlit Application**

## Overview
- This project is a Streamlit based web application designed to collect and log student email creation details into a PostgreSQL database. 

- The application allows students to: 
* Select their college 
* Select their name
* Indicate whether they have created their email address 
* Provide reasons if not created 
* Submit verified Gmail addresses

- All responses are securely stored in a PostgreSQL database for tracking and reporting. 


## Folder Structure
## Folder Structure

```text
TSTT_Email_Address_Collection/
├── app.py                     # Main Streamlit entry point
├── db/
│   ├── __init__.py
│   ├── connection.py          # DB engine / connection
│   └── queries.py             # Fetch college, name, subject
├── storage/
│   ├── __init__.py
│   └── store_to_database.py   # Store data to PostgreSQL
├── utils/
│   ├── __init__.py
│   └── helper_functions.py    # Timestamp, dataframe creation
├── ui/
│   ├── __init__.py
│   ├── style.py               # CSS & styling
│   └── header.py              # Logo + title
├── .streamlit/
│   ├── config.toml
│   ├── secrets.example.toml   # Example file
│   └── secrets.toml           # Ignored by git
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 How to Run the Application 
From your project directory, run: 

*streamlit run app.py*
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
```text
DB_HOST = "your_host" 
DB_PORT = "your_port" 
DB_NAME = "your_database" 
DB_USER = "your_username" 
DB_PASSWORD = "your_password" 
```

## 🧩 Application Workflow 
### 1. Load Dropdown Data 
- Fetches college names from database 
- Fetches student names from database
- Displays the subject area associated with the student from database
    
### 2. User Input Collection 
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
    
### 3. Validations 
The app enforces: 
- Required fields must be filled 
- Email must contain @gmail.com 
- Confirm email must match original email 
- Graceful error messages on failure 
    
### 4. Data Storage 
On successful submission: 
- A timestamp (converted to IST) is generated 
- Data is structured into a Pandas DataFrame 
- Stored in PostgreSQL table:
```text
old.tstt_email_collection_log
```

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
| subject_area     | Subject Areas of student|
