import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seaborn
import os

# Define paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), '../../mimic-iii-clinical-database-demo-1.4')
REPORT_DIR = os.path.join(os.path.dirname(__file__), '../report')
IMAGES_DIR = os.path.join(REPORT_DIR, 'images')

if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

def load_processed_data():
    df = pd.read_csv(os.path.join(DATA_DIR, 'processed_admissions.csv'))
    return df

def generate_eda_plots(df):
    print("Generating EDA plots...")
    
    # 1. Age Distribution Histogram
    plt.figure(figsize=(10, 6))
    seaborn.histplot(df['age'].dropna(), bins=20, kde=True, color='skyblue')
    plt.title('Age Distribution of Patients')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(IMAGES_DIR, 'age_distribution.png'))
    plt.close()

    # 2. ICU Stay Duration Distribution
    plt.figure(figsize=(10, 6))
    seaborn.histplot(df['total_icu_los'].dropna(), bins=20, kde=True, color='green')
    plt.title('ICU Stay Duration Distribution')
    plt.xlabel('Length of Stay (Days)')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(IMAGES_DIR, 'icu_los_distribution.png'))
    plt.close()

    # 3. Top 10 Most Common Diagnoses (using ICD9 Code from processed file)
    # The 'diagnosis' column (text) is also available. Let's use 'diagnosis' for readability if available, else icd9_code
    # processed_admissions has 'diagnosis' (text) and 'icd9_code'.
    # Text is more readable.
    top_diag = df['diagnosis'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    seaborn.barplot(x=top_diag.values, y=top_diag.index, palette='viridis')
    plt.title('Top 10 Most Common Admitting Diagnoses')
    plt.xlabel('Count')
    plt.ylabel('Diagnosis')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'top_10_diagnoses.png'))
    plt.close()

    # 4. Diagnosis vs Average ICU Stay
    # Group by diagnosis and calculate mean LOS
    diag_los = df.groupby('diagnosis')['total_icu_los'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    seaborn.barplot(x=diag_los.values, y=diag_los.index, palette='magma')
    plt.title('Average ICU Stay by Diagnosis (Top 10 Longest)')
    plt.xlabel('Average LOS (Days)')
    plt.ylabel('Diagnosis')
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'diagnosis_vs_los.png'))
    plt.close()

    # 5. Correlation Heatmap
    # Select numeric columns
    numeric_df = df[['age', 'total_icu_los', 'hospital_expire_flag']]
    plt.figure(figsize=(8, 6))
    seaborn.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    plt.savefig(os.path.join(IMAGES_DIR, 'correlation_heatmap.png'))
    plt.close()

    print("Main plots saved.")

def generate_lab_plots():
    print("Generating Lab plots...")
    # Load LABEVENTS for specific item IDs
    # Glucose: 50931, Creatinine: 50912
    # Check if file exists
    lab_path = os.path.join(RAW_DATA_DIR, 'LABEVENTS.csv')
    if not os.path.exists(lab_path):
        print("LABEVENTS.csv not found, skipping lab plots.")
        return

    # Read only necessary columns to save memory if large
    # For demo it's small, read all
    labs = pd.read_csv(lab_path)
    
    # Filter for Glucose and Creatinine
    glucose_df = labs[labs['itemid'].isin([50931, 50809])] # 50931: Glucose (Blood), 50809: Glucose
    creatinine_df = labs[labs['itemid'].isin([50912])] # 50912: Creatinine

    # Plot Glucose Distribution
    plt.figure(figsize=(10, 6))
    seaborn.histplot(glucose_df['valuenum'].dropna(), bins=30, kde=True, color='orange')
    plt.title('Glucose Level Distribution')
    plt.xlabel('Glucose (mg/dL)')
    plt.xlim(0, 400) # Limit x-axis to avoid outliers skewing plot
    plt.savefig(os.path.join(IMAGES_DIR, 'glucose_distribution.png'))
    plt.close()

    # Plot Creatinine Distribution
    plt.figure(figsize=(10, 6))
    seaborn.histplot(creatinine_df['valuenum'].dropna(), bins=30, kde=True, color='purple')
    plt.title('Creatinine Level Distribution')
    plt.xlabel('Creatinine (mg/dL)')
    plt.xlim(0, 10) # Limit
    plt.savefig(os.path.join(IMAGES_DIR, 'creatinine_distribution.png'))
    plt.close()
    
    print("Lab plots saved.")

if __name__ == "__main__":
    try:
        df = load_processed_data()
        generate_eda_plots(df)
        generate_lab_plots()
        print("Analysis complete. Images saved to report/images/")
    except Exception as e:
        print(f"Error in EDA: {e}")
