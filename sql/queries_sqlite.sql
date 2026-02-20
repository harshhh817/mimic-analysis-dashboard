
# 5. Comprehensive Analytical Dataset View
# Note: SQLite does not support advanced date functions like 'age()', using julianday for approximation.
CREATE VIEW analytical_dataset AS
SELECT
    p.subject_id,
    p.gender,
    (julianday(a.admittime) - julianday(p.dob)) / 365.25 AS age_years,
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
