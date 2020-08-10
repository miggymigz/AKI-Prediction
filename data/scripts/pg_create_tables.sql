CREATE SCHEMA IF NOT EXISTS mimiciii;
CREATE SCHEMA IF NOT EXISTS eicu;

DROP TABLE IF EXISTS mimiciii.cohort_modify;
DROP TABLE IF EXISTS eicu.cohort_modify;

CREATE TABLE mimiciii.cohort_modify
(
    icustay_id INT NOT NULL,
    gender INT NOT NULL,
    age INT NOT NULL,
    mean_weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi_group INT NOT NULL,
    itemid INT NOT NULL,
    charttime BIGINT NOT NULL,
    valuenum REAL, -- some values are empty for some reason
    aki_stage INT NOT NULL
);
CREATE TABLE eicu.cohort_modify
(
    patientunitstayid INT NOT NULL,
    gender INT NOT NULL,
    age INT NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi_group INT NOT NULL,
    labname VARCHAR(100) NOT NULL,
    labtime INT NOT NULL,
    labresult REAL, -- some values are empty for some reason
    aki_stage INT NOT NULL
);