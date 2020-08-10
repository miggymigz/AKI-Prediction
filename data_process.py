from imblearn.over_sampling import SMOTE
from pathlib import Path
# from collections import Counter

import psycopg2
import numpy as np
import getpass

np.set_printoptions(threshold=np.inf)


class data_process():
    def __init__(self, data_base):
        self.data_base = data_base
        # the 11 measurements of blood gas in MIMIC-III database
        if self.data_base == 'mimic':
            self.dict_lab = {50882: 0, 50902: 1, 50912: 2, 50931: 3, 50960: 4, 50971: 5, 50983: 6, 51006: 7, 51222: 8,
                             51265: 9, 51301: 10}
            self.dim = 16
        # the 10 measurements of blood gas in eICU database
        elif self.data_base == 'eicu':
            self.dict_lab = {'bicarbonate': 0, 'chloride': 1, 'creatinine': 2, 'glucose': 3, 'magnesium': 4,
                             'potassium': 5, 'sodium': 6, 'Hgb': 7, 'platelets x 1000': 8, 'WBC x 1000': 9}
            self.dim = 15

    def data_num(self, conn):
        cur = conn.cursor()
        # write the Select sentence with your own database name
        if self.data_base == 'mimic':
            cur.execute(
                "with s1 as(select distinct icustay_id from mimiciii.cohort_modify) select count(*) from s1")
        elif self.data_base == 'eicu':
            cur.execute(
                "with s1 as(select distinct patientunitstayid from eicu.cohort_modify) select count(*) from s1")
        rows = cur.fetchall()
        # get the number of patient in the database
        pat_num = rows[0]
        conn.commit()
        cur.close()
        # print(pat_num[0])
        return pat_num[0]

    def read_data(self, conn):

        data = np.zeros((self.pat_num, self.dim), dtype=np.float)
        label = np.zeros((self.pat_num,), dtype=np.float)
        i = 0
        cur = conn.cursor()
        # write the Select sentence with your own database name
        if self.data_base == 'mimic':
            cur.execute(
                "select distinct icustay_id, gender, age, mean_weight, height, bmi_group, aki_stage from mimiciii.cohort_modify order by icustay_id")
        elif self.data_base == 'eicu':
            cur.execute(
                "select distinct patientunitstayid, gender, age, weight, height, bmi_group, aki_stage from eicu.cohort_modify order by patientunitstayid")

        rows = cur.fetchall()
        # write the results of the Select to an array named 'data'
        for row in rows:
            for j in range(5):
                data[i][j] = row[j + 1]
            label[i] = row[6]
            i += 1
        # print(len(label))
        # print(label)
        i = 0
        j = 0

        if self.data_base == 'mimic':
            cur.execute(
                "select distinct icustay_id, itemid, valuenum from mimiciii.cohort_modify order by icustay_id, itemid")
        elif self.data_base == 'eicu':
            cur.execute(
                "select distinct patientunitstayid, labname, labresult from eicu.cohort_modify order by patientunitstayid, labname")

        rows = cur.fetchall()
        # write the measurements of blood gas to an array named 'data'
        for row in rows:
            if row[1] in self.dict_lab:
                # print(row[1])
                # print(row[2])
                data[i][self.dict_lab[row[1]] + 5] = row[2]
                # print(dict_lab[row[1]]+5)
            if j + 1 >= len(rows):
                break
            if rows[j + 1][0] != rows[j][0]:
                # print(data[i])
                i += 1
            j += 1
        print(data)
        conn.commit()
        cur.close()

        return data, label
    # OverSample using SMOTE algorithm

    def OverSamp(self, data_tr, label_tr):
        oversampler = SMOTE(
            sampling_strategy='auto',
            random_state=np.random.randint(100),
            k_neighbors=5,
            n_jobs=1,
        )

        for i in range(len(data_tr)):
            for j in range(self.dim):
                if np.isnan(data_tr[i][j]):
                    data_tr[i][j] = 0

        data_tr_res, label_tr_res = oversampler.fit_sample(data_tr, label_tr)
        # print('Resampled dataset shape {}'.format(Counter(label_tr_res)))
        return data_tr_res, label_tr_res

    # running this method, every patient can be represented as a picture with the dimension of 1×self.dim
    def run(self):
        conn = psycopg2.connect(
            database='aki',
            user=getpass.getuser(),
            password='',
            host='localhost',
            port='5432',
        )
        print("Opened database successfully")

        self.pat_num = self.data_num(conn)
        data, label = self.read_data(conn)
        data_res, label_res = self.OverSamp(data, label)
        pat_num_res = len(label_res)

        # ensure output dir exists
        output_dir = Path('data_set')
        output_dir.mkdir(parents=False, exist_ok=True)

        # save output file
        output_file = f'{self.data_base}_processed_1D.npz'
        output_path = output_dir / output_file
        np.savez(output_path, pat_num_res, data_res, label_res)

        # data = np.load(str(self.data_base) + "_processed_1D.npz")
        # print('pat_num_res is', data["arr_0"])
        # print('data_res num is', data["arr_1"].shape)
        # print('label_res num is', data["arr_2"].shape)

        conn.close()
