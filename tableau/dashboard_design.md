# Tableau Dashboard Design Specification

## Overview
This document outlines the design for three dashboards analyzing the MIMIC-III ICU dataset.

---

## 1. Dashboard Structure & Layout

### Dashboard 1: ICU Overview & Demographics
**Objective**: Provide a high-level summary of ICU activity and patient demographics.

**Key Performance Indicators (KPIs) - Top Row**:
- **Total Patients**: Distinct count of `subject_id`.
- **Total ICU Stays**: Distinct count of `icustay_id`.
- **Average Length of Stay (LOS)**: Average of `total_icu_los`.
- **In-Hospital Mortality Rate**: Average of `hospital_expire_flag` (Formatted as Percentage).

**Visualizations**:
1. **Age Distribution (Histogram)**:
   - **Type**: Histogram/Bar Chart
   - **Metrics**: Count of Patients by Age Bin (use `age_group`).
   - **Filters**: Gender.
2. **Gender Distribution (Donut Chart)**:
   - **Type**: Pie/Donut Chart.
   - **Metric**: % of Total Patients by Gender.
   - **Color**: Male (Blue), Female (Pink/Orange).
3. **LOS Distribution (Box Plot or Histogram)**:
   - **Type**: Box Plot
   - **Metric**: Distribution of `total_icu_los`.
   - **Insight**: Identify outliers (long stays).

**Filters**:
- Admission Type (Emergency/Elective/Urgent).
- Age Group.
- Gender.

---

### Dashboard 2: Diagnosis & Clinical Conditions
**Objective**: Analyze the primary reasons for admission and their impact on resource utilization.

**Visualizations**:
1. **Top 10 Diagnoses (Bar Chart)**:
   - **Type**: Horizontal Bar Chart.
   - **Metric**: Count of Admissions.
   - **Dimension**: `diagnosis` (or `icd9_code`).
   - **Sort**: Descending by Count.
2. **Average LOS by Diagnosis (Bar Chart)**:
   - **Type**: Bar Chart.
   - **Metric**: Average `total_icu_los`.
   - **Dimension**: `diagnosis`.
   - **Insight**: Identify which conditions require the longest stays.
3. **Diagnosis vs Mortality Rate (Scatter Plot)**:
   - **Type**: Scatter Plot
   - **X-Axis**: Count of Patients (Volume).
   - **Y-Axis**: Mortality Rate (Average `hospital_expire_flag`).
   - **Size**: Average LOS.
   - **Color**: Diagnosis Category (if available) or Diagnosis.

**Filters**:
- Diagnosis (Top N Filter).
- LOS Category (Short/Medium/Long).

---

### Dashboard 3: Lab Results Analysis
**Objective**: Explore the distribution of critical lab values and their relationship with patient outcomes.

**Visualizations**:
1. **Glucose Level Distribution (Histogram)**:
   - **Type**: Histogram
   - **Metric**: Count of Measurements
   - **Filter**: `itemid` IN (50931, 50809).
   - **Reference Line**: Normal Range (70-100 mg/dL).
2. **Creatinine Level vs. LOS (Scatter Plot)**:
   - **Type**: Scatter Plot.
   - **X-Axis**: Average Creatinine Level per Patient.
   - **Y-Axis**: `total_icu_los`.
   - **Details**: Color by Mortality (Survived/Died).
3. **Lab Abnormalities by Age (Heatmap)**:
   - **Type**: Heatmap.
   - **Rows**: Age Group.
   - **Columns**: Lab Test Name (Glucose, Creatinine, etc.).
   - **Color**: Average Value or % Abnormal.

**Filters**:
- Lab Item Name.
- Patient Outcome (Survived/Died).

---

## 2. Calculated Fields (Tableau)

If the data is not pre-processed, use these formulas:

1. **Age Group** (If `age_group` column missing):
   ```
   IF [Age] <= 18 THEN "0-18"
   ELSEIF [Age] <= 40 THEN "19-40"
   ELSEIF [Age] <= 60 THEN "41-60"
   ELSEIF [Age] <= 80 THEN "61-80"
   ELSE "80+"
   END
   ```

2. **LOS Category** (If `los_category` missing):
   ```
   IF [Total Icu Los] < 2 THEN "Short (<2 Days)"
   ELSEIF [Total Icu Los] <= 7 THEN "Medium (2-7 Days)"
   ELSE "Long (>7 Days)"
   END
   ```

3. **Mortality Rate**:
   ```
   AVG([Hospital Expire Flag])
   ```

4. **Is Abnormal Lab**:
   ```
   IF [Flag] = "abnormal" THEN 1 ELSE 0 END
   ```

---

## 3. Recommended Actions
- Use `processed_admissions.csv` as the primary data source for Dashboard 1 & 2.
- Join `LABEVENTS.csv` with `processed_admissions.csv` on `hadm_id` for Dashboard 3. Be careful with data volume; filter for specific lab items first.
- Use distinct colors for consistent categorical data (e.g., Survived = Green, Died = Red/Grey).
