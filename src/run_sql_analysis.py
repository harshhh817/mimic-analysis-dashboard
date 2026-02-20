import sqlite3
import pandas as pd
import os

# Define paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../mimic-iii-clinical-database-demo-1.4')
SQL_DIR = os.path.join(os.path.dirname(__file__), '../sql')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../sql_output')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_data_to_sqlite():
    conn = sqlite3.connect(':memory:')  # Create in-memory DB
    print("Loading CSV files into SQLite...")
    
    # Load required tables
    tables = ['PATIENTS', 'ADMISSIONS', 'ICUSTAYS', 'DIAGNOSES_ICD', 'LABEVENTS']
    
    for table_name in tables:
        file_path = os.path.join(DATA_DIR, f'{table_name}.csv')
        if os.path.exists(file_path):
            print(f"Loading {table_name}...")
            # Read CSV
            df = pd.read_csv(file_path)
            # Write to SQL
            df.to_sql(table_name, conn, index=False, if_exists='replace')
        else:
            print(f"Warning: {table_name}.csv not found.")
            
    return conn

def execute_queries(conn):
    print("Executing queries...")
    
    queries = [
        ("Join_Patients_Admissions", """
        SELECT 
            p.subject_id,
            p.gender,
            p.dob,
            a.hadm_id,
            a.admittime,
            a.dischtime,
            a.diagnosis,
            a.hospital_expire_flag
        FROM PATIENTS p
        JOIN ADMISSIONS a ON p.subject_id = a.subject_id
        LIMIT 50;
        """),
        ("Join_Admissions_ICUStays", """
        SELECT 
            a.subject_id,
            a.hadm_id,
            a.admittime,
            i.icustay_id,
            i.intime,
            i.outtime,
            i.los AS icu_length_of_stay
        FROM ADMISSIONS a
        JOIN ICUSTAYS i ON a.hadm_id = i.hadm_id
        LIMIT 50;
        """),
        ("Join_Diagnoses", """
        SELECT 
            a.subject_id,
            a.hadm_id,
            d.seq_num,
            d.icd9_code
        FROM ADMISSIONS a
        JOIN DIAGNOSES_ICD d ON a.hadm_id = d.hadm_id
        ORDER BY a.hadm_id, d.seq_num
        LIMIT 50;
        """),
        ("Analytical_Dataset_View", """
        SELECT
            p.subject_id,
            p.gender,
            (julianday(a.admittime) - julianday(p.dob)) / 365.25 AS age_years,
            a.hadm_id,
            a.admittime,
            i.icustay_id,
            i.los
        FROM PATIENTS p
        JOIN ADMISSIONS a ON p.subject_id = a.subject_id
        LEFT JOIN ICUSTAYS i ON a.hadm_id = i.hadm_id
        LIMIT 50;
        """)
    ]
    
    for name, query in queries:
        print(f"Running Query: {name}...")
        try:
            df_result = pd.read_sql_query(query, conn)
            output_file = os.path.join(OUTPUT_DIR, f'{name}.csv')
            df_result.to_csv(output_file, index=False)
            print(f"Saved result to {output_file}")
            print(df_result.head(2))
        except Exception as e:
            print(f"Error executing {name}: {e}")

def main():
    try:
        conn = load_data_to_sqlite()
        execute_queries(conn)
        conn.close()
        print("SQL Analysis execution complete.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
