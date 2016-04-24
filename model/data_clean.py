import numpy as np
import pandas as pd
from fuzzywuzzy import process
from maps import job_title_map, city_name_map, gender_map
from job_ids import ordered_job_ids
from city_ids import ordered_city_ids
from model_parameters import coefficients, fields

def predict_income(city, job, age, education, gender):

	city_names = city_name_map.keys()
	job_names = job_title_map.keys()
	
	standardized_city_name = process.extractOne(city, city_names)[0]
	standardized_job_name = process.extractOne(job, job_names)[0]

	given = [city_name_map[standardized_city_name], job_title_map[standardized_job_name], education]

	inputs = []
	for field in fields:
		if field in given:
			print field
			inputs.append(1)
		else:
			inputs.append(0)

	age = float(age)
	age_std = (age - 16) / (85 - 16)
	inputs[fields.index('age')] = age_std

	inputs[fields.index('female')] = gender_map[gender]

	return np.dot(inputs, coefficients) * 1.5




