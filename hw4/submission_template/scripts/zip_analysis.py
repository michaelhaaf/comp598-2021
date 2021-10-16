import os, sys
import pandas as pd
import numpy as np
import pickle

print('loading data...')
# df = pd.read_csv('../data/test-set.csv', header=None, low_memory=False)
df = pd.read_csv('../data/nyc_311_limit-trimmed.csv', header=None, low_memory=False)

zip_code_column = 8
create_date_column = 1
close_date_column = 2

df = df[~df.iloc[:, zip_code_column].isnull()]
df.iloc[:, zip_code_column] = df.iloc[:, zip_code_column].astype(int)

unique_zips = df.iloc[:, zip_code_column].unique()
unique_zips = [zipcode for zipcode in unique_zips if str(zipcode) != 'nan']

df = df[~df.iloc[:, close_date_column].isnull()]
df.iloc[:, close_date_column] = pd.to_datetime(df.iloc[:, close_date_column]) 
df.iloc[:, create_date_column] = pd.to_datetime(df.iloc[:, create_date_column]) 

# per zip
    # per close date month (Jan, then Feb, etc.) 
        # what is difference between open and close date?
        # average
zip_avg_map = {}
print('processing zip codes...')
for zipcode in unique_zips:
    monthly_avgs = [] 
    zip_df = df.loc[lambda df: df.iloc[:, zip_code_column] == zipcode, :]
    for month in range(1, 13):
        month_df = zip_df[zip_df.iloc[:, close_date_column].dt.month == month]
        time_diff_df = month_df.iloc[:, close_date_column] - month_df.iloc[:, create_date_column]
        time_diff_df = time_diff_df.astype('timedelta64[h]')
        time_diff_df = time_diff_df[time_diff_df[:] > 0]
        avg = time_diff_df.mean()
        if np.isnan(avg):
            monthly_avgs.append(0)
        else:
            monthly_avgs.append(avg)
    zip_avg_map[zipcode] = monthly_avgs
    with open(f'../data/zips/{zipcode}.pk1', 'wb+') as f:
        pickle.dump(monthly_avgs, f)

# overall_monthly_averages = [ for (zipcode, avgs) in zip_avg_map.items()]
# overall average
    # per zip
        # per month
            #average
print("")
print("processing average...")
overall_monthly_avgs = [0]*12
for zipcode, avgs in zip_avg_map.items():
    overall_monthly_avgs = [sum(x) for x in zip(overall_monthly_avgs, avgs)] 
overall_monthly_avgs = [x / len(zip_avg_map.items()) for x in overall_monthly_avgs]
print(overall_monthly_avgs)
with open(f'../data/zips/average.pk1', 'wb+') as f:
    pickle.dump(overall_monthly_avgs, f)
