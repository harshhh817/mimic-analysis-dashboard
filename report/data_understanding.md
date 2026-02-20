# Data Understanding

## 1. Dataset Tables

### PATIENTS.csv
Contains de-identified patient demographic data.
- **Key Columns**:
  - `subject_id`: Unique identifier for each patient. (Primary Key)
  - `gender`: Patient gender (M/F).
  - `dob`: Date of birth.
  - `dod`: Date of death (null if alive).
  - `expire_flag`: Flag indicating if the patient died (1) or not (0).

### ADMISSIONS.csv
Contains information regarding a patient's admission to the hospital.
- **Key Columns**:
  - `hadm_id`: Unique identifier for each admission. (Primary Key)
  - `subject_id`: Identify the patient. (Foreign Key to PATIENTS)
  - `admittime`: Date and time of admission.
  - `dischtime`: Date and time of discharge.
  - `deathtime`: Date and time of death (if applicable).
  - `diagnosis`: Preliminary diagnosis upon admission.
  - `hospital_expire_flag`: In-hospital mortality indicator.

### ICUSTAYS.csv
Defines each ICU stay for a patient.
- **Key Columns**:
  - `icustay_id`: Unique identifier for the ICU stay. (Primary Key)
  - `subject_id`: Identify the patient. (Foreign Key to PATIENTS)
  - `hadm_id`: Identify the hospital admission. (Foreign Key to ADMISSIONS)
  - `intime`: Time the patient entered the ICU.
  - `outtime`: Time the patient left the ICU.
  - `los`: Length of stay in the ICU (days).

### DIAGNOSES_ICD.csv
List of ICD-9 diagnosis codes for each hospital admission.
- **Key Columns**:
  - `row_id`: Unique row identifier. (Primary Key)
  - `subject_id`: Identify the patient. (Foreign Key to PATIENTS)
  - `hadm_id`: Identify the hospital admission. (Foreign Key to ADMISSIONS)
  - `icd9_code`: The ICD-9 diagnosis code.
  - `seq_num`: Priority sequence of the diagnosis.

### LABEVENTS.csv
Contains laboratory measurements for patients.
- **Key Columns**:
  - `row_id`: Unique row identifier. (Primary Key)
  - `subject_id`: Identify the patient. (Foreign Key to PATIENTS)
  - `hadm_id`: Identify the hospital admission (if applicable). (Foreign Key to ADMISSIONS)
  - `itemid`: Identify the lab test performed. (Foreign Key to D_LABITEMS)
  - `charttime`: Time when the measurement was recorded.
  - `valuenum`: Numeric value of the result.
  - `flag`: Abnormality flag (e.g., 'abnormal').

## 2. Relationships Data Model

- **PATIENTS (1) -> (Many) ADMISSIONS**: A patient can have multiple hospital admissions. linked by `subject_id`.
- **ADMISSIONS (1) -> (Many) ICUSTAYS**: A single hospital admission can include multiple ICU stays (e.g., if a patient is transferred between units), linked by `hadm_id`.
- **ADMISSIONS (1) -> (Many) DIAGNOSES_ICD**: Each admission has multiple diagnosis codes associated with it, linked by `hadm_id`.
- **ADMISSIONS (1) -> (Many) LABEVENTS**: Lab tests are performed during an admission, linked by `hadm_id` (and `subject_id`). Note that `LABEVENTS` can also be linked directly to `PATIENTS` for outpatient labs where `hadm_id` might be null, but generally linked to admissions for inpatient analysis.

## 3. Key Identifiers
- **Primary Key**:
  - `PATIENTS`: `subject_id`
  - `ADMISSIONS`: `hadm_id`
  - `ICUSTAYS`: `icustay_id`
- **Foreign Keys**:
  - `ADMISSIONS.subject_id` references `PATIENTS.subject_id`
  - `ICUSTAYS.subject_id` references `PATIENTS.subject_id`
  - `ICUSTAYS.hadm_id` references `ADMISSIONS.hadm_id`
  - `DIAGNOSES_ICD.hadm_id` references `ADMISSIONS.hadm_id`
  - `LABEVENTS.hadm_id` references `ADMISSIONS.hadm_id`
