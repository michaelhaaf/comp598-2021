import os, sys
import pandas as pd
import numpy as np
import pickle

unique_zips = []
with open('../data/unique_zips.pk1', 'rb') as f:
    unique_zips = pickle.load(f)

unique_zips.append("average")
for zip in unique_zips:
    dummy_data = np.random.uniform(low=1, high=4000, size=(12))
    with open(f'../data/dummyzips/{zip}.pk1', 'wb+') as f:
        pickle.dump(dummy_data, f)





