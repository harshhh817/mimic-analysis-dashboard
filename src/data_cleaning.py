import pandas as pd
import numpy as np
import os
from datetime import datetime

# Define paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../mimic-iii-clinical-database-demo-1.4')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../data')

def load_data():
    """Load the required CSV files."""
    print("Loading data...")
    patients = pd.read_csv(os.path.join(DATA_DIR, 'PATIENTS.csv'))
    admissions = pd.read_csv(os.path.join(DATA_DIR, 'ADMISSIONS.csv'))
    # Use only relevant columns for initial load to avoid memory issues if any (demo is small though)
    icustays = pd.read_csv(os.path.join(DATA_DIR, 'ICUSTAYS.csv'))
    diagnoses = pd.read_csv(os.path.join(DATA_DIR, 'DIAGNOSES_ICD.csv'))
    labevents = pd.read_csv(os.path.join(DATA_DIR, 'LABEVENTS.csv'))
    return patients, admissions, icustays, diagnoses, labevents

def clean_data(patients, admissions, icustays, diagnoses, labevents):
    """Clean and preprocess the data."""
    print("Cleaning data...")

    # Convert date columns to datetime with coercion
    date_cols_patients = ['dob', 'dod', 'dod_hosp', 'dod_ssn']
    for col in date_cols_patients:
        patients[col] = pd.to_datetime(patients[col], errors='coerce')

    date_cols_admissions = ['admittime', 'dischtime', 'deathtime', 'edregtime', 'edouttime']
    for col in date_cols_admissions:
        admissions[col] = pd.to_datetime(admissions[col], errors='coerce')

    date_cols_icustays = ['intime', 'outtime'] 
    for col in date_cols_icustays:
        icustays[col] = pd.to_datetime(icustays[col], errors='coerce')

    # Merge patients and admissions
    adm_pat = pd.merge(admissions, patients[['subject_id', 'dob', 'gender']], on='subject_id', how='inner')
    
    # Check for Out of Bounds dates
    # Pandas timestamp min/max: 1677-09-21 to 2262-04-11
    # Check if DOB is valid
    print(f"DOB range: {adm_pat['dob'].min()} to {adm_pat['dob'].max()}")
    print(f"AdmitTime range: {adm_pat['admittime'].min()} to {adm_pat['admittime'].max()}")

    # Calculate age safely
    # If DOB is missing or out of bounds, age will be NaN
    # We use (admittime - dob) / 365.25 days
    
    # Calculate difference in days directly if subtraction fails
    try:
        age_timedelta = adm_pat['admittime'] - adm_pat['dob']
        adm_pat['age'] = age_timedelta.dt.total_seconds() / (3600 * 24 * 365.25)
    except Exception as e:
        print(f"Error calculating age directly: {e}")
        # Alternative: use year difference
        adm_pat['age'] = (adm_pat['admittime'].dt.year - adm_pat['dob'].dt.year)

    # Handle ages > 89 (MIMIC shifts these ages to 300 for de-identification, resulting in negative or huge ages if not handled)
    # Actually, if DOB is shifted to 300 years *before* admission...
    # Wait, if admission is 2150, DOB is 1850 -> Age 300.
    # If age > 89, it should be treated as >89.
    # In MIMIC, age > 89 are shifted to be 300+ years old.
    # We will cap at 90.
    adm_pat.loc[adm_pat['age'] > 120, 'age'] = 90
    adm_pat.loc[adm_pat['age'] < 0, 'age'] = np.nan 

    print("Age calculated.")

    # Calculate ICU Length of Stay (LOS)
    # Aggregating at Admission level
    icustay_agg = icustays.groupby('hadm_id')['los'].sum().reset_index()
    icustay_agg.rename(columns={'los': 'total_icu_los'}, inplace=True)
    
    final_df = pd.merge(adm_pat, icustay_agg, on='hadm_id', how='left')
    final_df['total_icu_los'] = final_df['total_icu_los'].fillna(0)

    # Categorize LOS
    def categorize_los(los):
        if los < 2:
            return 'Short'
        elif los <= 7:
            return 'Medium'
        else:
            return 'Long'
    
    final_df['los_category'] = final_df['total_icu_los'].apply(categorize_los)

    # Add diagnosis info (First listed diagnosis)
    # We can use the 'diagnosis' column in ADMISSIONS or join with DIAGNOSES_ICD
    primary_diag = diagnoses[diagnoses['seq_num'] == 1][['hadm_id', 'icd9_code']]
    final_df = pd.merge(final_df, primary_diag, on='hadm_id', how='left')

    # Feature Engineering: First Lab Measurement per Admission
    # Glucose (50931, 50809) and Creatinine (50912)
    print("Extracting first lab measurements...")
    
    # Filter LABEVENTS for relevant items
    # 50931: Glucose (Blood), 50809: Glucose, 50912: Creatinine
    relevant_items = [50931, 50809, 50912]
    labs_filtered = labevents[labevents['itemid'].isin(relevant_items)].copy()
    
    # Ensure charttime is datetime
    labs_filtered['charttime'] = pd.to_datetime(labs_filtered['charttime'], errors='coerce')
    
    # Sort by admission and time
    labs_filtered.sort_values(by=['hadm_id', 'charttime'], inplace=True)
    
    # Extract Glucose
    glucose_labs = labs_filtered[labs_filtered['itemid'].isin([50931, 50809])]
    first_glucose = glucose_labs.groupby('hadm_id').first().reset_index()[['hadm_id', 'valuenum']]
    first_glucose.rename(columns={'valuenum': 'first_glucose'}, inplace=True)
    
    # Extract Creatinine
    creat_labs = labs_filtered[labs_filtered['itemid'] == 50912]
    first_creat = creat_labs.groupby('hadm_id').first().reset_index()[['hadm_id', 'valuenum']]
    first_creat.rename(columns={'valuenum': 'first_creatinine'}, inplace=True)
    
    # Merge into final_df
    final_df = pd.merge(final_df, first_glucose, on='hadm_id', how='left')
    final_df = pd.merge(final_df, first_creat, on='hadm_id', how='left')
    
    return final_df

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    try:
        patients, admissions, icustays, diagnoses, labevents = load_data()
        final_df = clean_data(patients, admissions, icustays, diagnoses, labevents)
        
        output_path = os.path.join(OUTPUT_DIR, 'processed_admissions.csv')
        final_df.to_csv(output_path, index=False)
        print(f"Data processed and saved to {output_path}")
        print(final_df.head())
        print(final_df.info())
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
