from db.connection import get_db_engine

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
