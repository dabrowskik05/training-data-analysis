# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os, os.path
import glob
import json
import geopandas as gpd
# %%
!pip install shapely
from shapely.geometry import Point
# %%
path = "zebrane_dane.csv"

df = pd.read_csv(path)
df.columns
# %%
# %%
new_column_names = [
    "end_date",
    "start_date",
    "start_latitude [°]",
    "start_longitude [°]",
    "elapsed_time [s]",
    "active_time [s]",
    "distance [km]",
    "total_strokes [strokes]",
    "nec_latitude [°]",
    "nec_longitude [°]",
    "swc_latitude [°]",
    "swc_longitude [°]",
    "avg_speed_enhanced [km/h]",
    "max_speed_enhanced [km/h]",
    "calories [kcal]",
    "avg_speed_basic [km/h]",
    "max_speed_basic [km/h]",
    "total_ascent [m]",
    "total_descent [m]",
    "lap_count",
    "vertical_oscillation [mm]",
    "stance_time_pct [%]",
    "stance_time [ms]",
    "vertical_ratio [%]",
    "stance_balance [%]",
    "step_length [mm]",
    "sport",
    "sub_sport",
    "avg_hr [bpm]",
    "max_hr [bpm]",
    "avg_cadence [rpm]",
    "max_cadence [rpm]",
    "training_effect",
    "avg_temperature [°C]",
    "max_temperature [°C]",
    "avg_cadence_fractional [rpm]",
    "max_cadence_fractional [rpm]",
    "anaerobic_effect",
    "fractional_ascent [m]",
    "fractional_descent [m]",
    "total_strides [strides]",
    "avg_run_cadence [strides/min]",
    "max_run_cadence [strides/min]",
    "total_cycles [cycles]"
]

df.columns = new_column_names
df

df
# %%
df = df.sort_values("start_date")
df.loc[:, 'start_time'] = pd.to_datetime(df.loc[:,"start_date"]).dt.time
df.loc[:, 'end_time'] = pd.to_datetime(df.loc[:, "end_date"]).dt.time
df.loc[:,'start_date'] = pd.to_datetime(df.loc[:,"start_date"]).dt.date
df.loc[:,'end_date'] =  pd.to_datetime(df.loc[:, "end_date"]).dt.date
df = df.loc[:, ['start_date', 'end_date'] + ['start_time','end_time']+ df.columns[2:-2].tolist()]
df
# %%
#df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['start_latitude [°]'], df['start_longitude [°]']))
df['location'] = df.apply(lambda row: Point(row['start_latitude [°]'], row['start_longitude [°]']), axis=1)

# %%
df[~df.sport.isin(['running', 'cycling',"walking","hiking"])] # puste
# %%
df = df.loc[:, df.columns[0:6].tolist() + ['location']+ df.columns[6:-1].tolist()]
df

# %%
running = df.loc[df.sport == "running"].drop("sport", axis=1).dropna(axis=1,how="all").reset_index(drop = True)
cycling = df.loc[df.sport == "cycling"].drop("sport", axis=1).dropna(axis=1,how="all").reset_index(drop = True)
walking = df.loc[df.sport == "walking"].drop("sport", axis=1).dropna(axis=1,how="all").reset_index(drop = True)
hiking = df.loc[df.sport == "hiking"].drop("sport", axis=1).dropna(axis=1,how="all").reset_index(drop = True)
# %%
np.all(walking.anaerobic_effect == 0.0) # True
walking = walking.loc[:, ~(walking == 0).all()]
# %%
running['start_date'] = pd.to_datetime(running['start_date'])
running_m = running.groupby(running['start_date'].dt.to_period('M')).agg({
    'calories [kcal]': 'sum',
    'distance [km]': 'sum'
}).reset_index()

# Konwersja okresu na datę
running_m['start_date'] = running_m['start_date'].dt.to_timestamp()

# Wykres z dwiema osiami Y
fig, ax1 = plt.subplots(figsize=(12, 6))

# Kalorie
ax1.set_xlabel('Data (miesiące)')
ax1.set_ylabel('Kalorie [kcal]', color='tab:red')
ax1.plot(running_m['start_date'], running_m['calories [kcal]'], color='tab:red', label='Kalorie')
ax1.tick_params(axis='y', labelcolor='tab:red')

# Dystans
ax2 = ax1.twinx()
ax2.set_ylabel('Dystans [km]', color='tab:blue')
ax2.plot(running_m['start_date'], running_m['distance [km]'], color='tab:blue', label='Dystans')
ax2.tick_params(axis='y', labelcolor='tab:blue')

fig.tight_layout()
plt.title('Kalorie i Dystans na Miesiąc')
plt.show()
# %%
trail_running = running.loc[running.sub_sport == "trail"].drop("sub_sport", axis=1).reset_index(drop = True)
generic_running = running.loc[running.sub_sport == "generic"].drop("sub_sport", axis=1).reset_index(drop = True)
generic_walking = walking.drop("sub_sport", axis=1)
generic_cycling = cycling.drop("sub_sport", axis=1)
generic_hiking = hiking.drop("sub_sport", axis=1)
# %%
