# %%
import pandas as pd
import numpy as np
import DataDownloadICsv as DaneCsv
import data_simplifying as DaneJson

# %%
df_csv = DaneCsv.df_csv
df_json = DaneJson.df
# %%

df_csv['Full_Date'] = pd.to_datetime(df_csv['Full_Date'])
df_csv['Full_Date'] = df_csv['Full_Date'].dt.tz_convert('Australia/Melbourne')

df_csv['Date'] = df_csv['Full_Date'].dt.date
df_csv['Time'] = df_csv['Full_Date'].dt.time


df_csv = df_csv.loc[:, ['Full_Date', 'Date', 'Time'] + df_csv.columns.to_list()[1:len(df_csv.columns)-2]]

df_csv = df_csv.sort_values('Full_Date').reset_index(drop=True)
# %%
df_csv.Latitude = np.round(df_csv.Latitude, 5)
df_json.start_latitude = np.round(df_json.start_latitude, 5)

df_csv.Longitude = np.round(df_csv.Longitude, 5)
df_json.start_longitude = np.round(df_json.start_longitude, 5)
# %%

# Let's assume:
# df_summary has columns: 'start_lat', 'start_lon'
# df_detail has columns: 'Latitude', 'Longitude'

# Make a set of start points as tuples
start_points = set(zip(df_json[''], df_summary['start_lon']))

# Flag rows that are start of a new session
df_detail['is_start'] = list(zip(df_detail['Latitude'], df_detail['Longitude'])).isin(start_points)