import numpy as np


df = pd.io.stata.read_stata('cepr_org_2015.dta', convert_categoricals=False, convert_missing=True)


cols_to_use = ['educ']


df.educ.map(educ_map)


pd.to_dummies()