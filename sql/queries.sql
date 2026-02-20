-- 1. Join PATIENTS and ADMISSIONS
-- This query retrieves patient demographics along with their admission details.
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
JOIN ADMISSIONS a ON p.subject_id = a.subject_id;

-- 2. Join ADMISSIONS and ICUSTAYS
-- This query links hospital admissions to ICU stays to analyze length of stay.
SELECT 
    a.subject_id,
    a.hadm_id,
    a.admittime,
    i.icustay_id,
    i.intime,
    i.outtime,
    i.los AS icu_length_of_stay
FROM ADMISSIONS a
JOIN ICUSTAYS i ON a.hadm_id = i.hadm_id;

-- 3. Join DIAGNOSES_ICD
-- This query retrieves all diagnosis codes for each admission.
SELECT 
    a.subject_id,
    a.hadm_id,
    d.seq_num,
    d.icd9_code
FROM ADMISSIONS a
JOIN DIAGNOSES_ICD d ON a.hadm_id = d.hadm_id
ORDER BY a.hadm_id, d.seq_num;

-- 4. Join LABEVENTS
-- This query retrieves lab measurements for admissions.
-- Note: LABEVENTS can be very large, so filtering by specific items is recommended.
SELECT 
    l.subject_id,
    l.hadm_id,
    l.charttime,
    l.itemid,
    l.valuenum,
    l.valueuom,
    l.flag
FROM LABEVENTS l
JOIN ADMISSIONS a ON l.hadm_id = a.hadm_id
-- Example: Filter for Glucose (50931) and Creatinine (50912)
WHERE l.itemid IN (50931, 50912);

-- 5. Comprehensive Join for Analytical Dataset
-- Creates a view combining patient, admission, ICU stay, and primary diagnosis.
CREATE VIEW analytical_dataset AS
SELECT
    p.subject_id,
    p.gender,
    EXTRACT(YEAR FROM age(a.admittime, p.dob)) AS age_years,
    a.hadm_id,
    a.admittime,
    a.dischtime,
    i.icustay_id,
    i.los,
    d.icd9_code AS primary_diagnosis
FROM PATIENTS p
JOIN ADMISSIONS a ON p.subject_id = a.subject_id
LEFT JOIN ICUSTAYS i ON a.hadm_id = i.hadm_id
LEFT JOIN DIAGNOSES_ICD d ON a.hadm_id = d.hadm_id AND d.seq_num = 1;
