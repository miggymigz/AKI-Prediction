-- Change to the directory containing the data files
\cd :data_dir

-- Load mimic data
\copy mimiciii.cohort_modify FROM 'mimic_cohort_modify.csv' DELIMITER ',' CSV HEADER NULL ''

-- Load eICU data
\copy eicu.cohort_modify FROM 'eicu_cohort_modify.csv' DELIMITER ',' CSV HEADER NULL ''