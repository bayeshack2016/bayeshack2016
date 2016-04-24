import numpy as np
import pandas as pd
from fuzzywuzzy import process
from maps import job_title_map, city_name_map, gender_map
from model_parameters import coefficients, fields
from collections import defaultdict

def predict_income(city, job, age, education, gender):

    city_names = city_name_map.keys()
    job_names = job_title_map.keys()

    standardized_city_name = process.extractOne(city, city_names)[0]
    standardized_job_name = process.extractOne(job, job_names)[0]

    given = [city_name_map[standardized_city_name], job_title_map[standardized_job_name], education]

    data = defaultdict(lambda: defaultdict(list))
    data_values = defaultdict(lambda: defaultdict(float))

    with open('income_data.csv', 'rb') as f:
        for line in f.readlines():
            line = line.split(',')
            educ = line[1]
            occ = line[4]
            income = float(line[-1])
            data[educ][occ].append(income)

    for educ in data:
        for occ in data[educ]:
            if len(data[educ][occ]) > 0:
                data_values[educ][occ] = sum(data[educ][occ])/len(data[educ][occ])
            else:
                data_values[educ][occ] = 0

    job_names = job_title_map.keys()
    standardized_job_name = process.extractOne(job, job_names)[0]
    job_id = job_title_map[standardized_job_name]

    benchmark = None
    if education in data_values and job_id in data_values[education]:
        benchmark = data_values[education][job_id]

    inputs = []
    for field in fields:
        if field in given:
            inputs.append(1)
        else:
            inputs.append(0)

    age = float(age)
    age_std = (age - 16) / (85 - 16)
    inputs[fields.index('age')] = age_std

    inputs[fields.index('female')] = gender_map[gender]
    pred = np.dot(inputs, coefficients)

    if pred < benchmark:
        return benchmark
    else:
        return pred
