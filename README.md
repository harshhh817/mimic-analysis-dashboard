# ICU Mortality Analysis Project

## For Group Members: How to Run
If you just cloned or downloaded this project:

1.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Add Data**: Copy the `mimic-iii-clinical-database-demo-1.4/` folder or CSV files into the `data/` directory.
3.  **Run Dashboard**:
    ```bash
    streamlit run src/dashboard_app.py
    ```

## Project Overview
This project analyzes ICU mortality based on diagnoses and lab measurements using the MIMIC-III Clinical Database Demo.

## Dataset
The project uses the following tables from the MIMIC-III demo dataset:
1. `PATIENTS.csv`: Demographic data for patients.
2. `ADMISSIONS.csv`: Hospital admission information.
3. `ICUSTAYS.csv`: ICU stay details.
4. `DIAGNOSES_ICD.csv`: ICD-9 diagnosis codes for patients.
5. `LABEVENTS.csv`: Laboratory measurements.
6. `processed_admissions.csv`: The cleaned analytical dataset (created by `src/data_cleaning.py`), which includes calculated age, LOS, and **first lab measurements** for Glucose and Creatinine.

## Project Structure
- `data/`: Contains the dataset files (should be linked or placed here).
- `notebooks/`: Jupyter notebooks for exploratory data analysis.
- `src/`: Python source code for data cleaning and processing.
- `sql/`: SQL scripts for data extraction and joining.
- `tableau/`: Tableau dashboard design documentation.
- `report/`: Final project report and documentation.

## Running the Analysis
1. Ensure the MIMIC-III CSV files are available in the `../mimic-iii-clinical-database-demo-1.4/` folder or copied to `data/`.
2. Run `pip install streamlit plotly pandas`
2. Run `src/data_cleaning.py` to process the raw data.
3. Run or view `notebooks/Analysis.ipynb` for EDA and insights.
4. SQL queries are available in `sql/queries.sql`.
5. Run `src/run_sql_analysis.py` to execute SQL queries on the CSVs and generate output in `sql_output/`.

## Generated Artifacts
- **Interactive Notebook**: `notebooks/Analysis.ipynb`
- **SQL Results**: `sql_output/*.csv` (e.g., `Analytical_Dataset_View.csv`)
- **EDA Plots**: `report/images/*.png` (Age, LOS, Diagnoses, etc.)
- **Final Report**: `report/final_report.md`

## 6. Interactive Dashboard
To view the interactive dashboard, run the following command in your terminal:
```bash
streamlit run src/dashboard_app.py
```
This will launch a web-based dashboard where you can filter by age, gender, and explore the data visually.

