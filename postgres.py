import pandas as pd
import psycopg
import os
from glob import glob

# Database connection details
DB_HOST = "localhost"
DB_NAME = "lottery_db"
DB_USER = "yourusername"
DB_PASSWORD = "yourpassword"
DB_PORT = 5432

# Folder containing the Excel files
INPUT_FOLDER = "input_docs"

def import_to_postgres(file_name):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_name, engine='openpyxl')

    # Connect to PostgreSQL using psycopg3
    with psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    ) as conn:
        with conn.cursor() as cursor:
            # Create a table (if it doesn't exist)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lottery_results (
                    date DATE,
                    number VARCHAR(4),
                    "1st machine" VARCHAR(1),
                    "2nd machine" VARCHAR(1),
                    "3rd machine" VARCHAR(1),
                    "4th machine" VARCHAR(1),
                    "COMPANY_NAME" VARCHAR(255)
                );
            """)
            conn.commit()

            # Insert data into the table
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO lottery_results (date, number, "1st machine", "2nd machine", "3rd machine", "4th machine", "COMPANY_NAME")
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (row['Date'], row['Number'], row['1st machine'], row['2nd machine'], row['3rd machine'], row['4th machine'], row['COMPANY_NAME']))
            conn.commit()

    print(f"Data from '{file_name}' imported successfully!")

if __name__ == "__main__":
    # Get all .xlsx files from the input_docs folder
    excel_files = glob(os.path.join(INPUT_FOLDER, "*.xlsx"))

    if not excel_files:
        print(f"[INFO] No .xlsx files found in the folder '{INPUT_FOLDER}'.")
    else:
        for file_name in excel_files:
            print(f"[INFO] Processing file: {file_name}")
            import_to_postgres(file_name)