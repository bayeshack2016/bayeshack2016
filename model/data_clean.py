import numpy as np
import pandas as pd
from helpers import indicate_outlier_values, get_income

df = pd.read_csv('temp_df.csv')

cols_to_use = ['educ', 'age', 'female', 'occ12', 'smsastat14', 'wage1', 'wage2', 'wage3','wage4', 'weekpay', 'pehrusl1']

#Pre-processing
df = df[cols_to_use]
df['outlier'] = df.apply(indicate_outlier_values, axis=1)
df = df[df.outlier == 0]
df['income'] = df.apply(get_income, axis=1)
df.dropna(subset=['income'], inplace=True)


df.drop(['wage1', 'wage2', 'wage3', 'wage4', 'weekpay', 'pehrusl1'], axis=1, inplace=True)

df.to_csv('final_df.csv')

#df.educ.map(educ_map, inplace=True)
#educ_dummies = pd.get_dummies(df.educ)

