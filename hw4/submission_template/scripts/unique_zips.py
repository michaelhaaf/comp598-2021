import os, sys
import pandas as pd
import numpy as np
import pickle

# df = pd.read_csv('../data/test-set.csv', dtype=str, header=None, low_memory=False)
df = pd.read_csv('../data/nyc_311_limit-trimmed.csv', dtype=str, header=None, low_memory=False)
zip_code_column = 8
unique_zips = df.iloc[:, zip_code_column].unique()
unique_zips = [zip for zip in unique_zips if str(zip) != 'nan']

print(unique_zips)
with open('../data/unique_zips.pk1', 'wb') as f:
     pickle.dump(unique_zips, f)

