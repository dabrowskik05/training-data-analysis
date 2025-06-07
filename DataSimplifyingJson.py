# %%
import pandas as pd
import DataDownloadJson as Dane

df = Dane.df


# %%
# %%
unit_labels = [
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
    "total_cycles [cycles]",
    "session_id"
]
work_names = [
    "end_date",
    "start_date",
    "start_latitude",
    "start_longitude",
    "elapsed_time",
    "active_time",
    "distance",
    "total_strokes",
    "nec_latitude",
    "nec_longitude",
    "swc_latitude",
    "swc_longitude",
    "avg_speed_enhanced",
    "max_speed_enhanced",
    "calories",
    "avg_speed_basic",
    "max_speed_basic",
    "total_ascent",
    "total_descent",
    "lap_count",
    "vertical_oscillation",
    "stance_time_pct",
    "stance_time",
    "vertical_ratio",
    "stance_balance",
    "step_length",
    "sport",
    "sub_sport",
    "avg_hr",
    "max_hr",
    "avg_cadence",
    "max_cadence",
    "training_effect",
    "avg_temperature",
    "max_temperature",
    "avg_cadence_fractional",
    "max_cadence_fractional",
    "anaerobic_effect",
    "fractional_ascent",
    "fractional_descent",
    "total_strides",
    "avg_run_cadence",
    "max_run_cadence",
    "total_cycles",
    "session_id"
]

df.columns = work_names

df
# %%
df.rename(columns={'timestamp' : 'end_date', 'start_time' : 'start_date'})
df.dropna(axis=0, subset=['start_date', 'end_date'], inplace=True)
df.reset_index()

df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])

df['start_date'] = df['start_date'].dt.tz_convert('Australia/Melbourne')
df['end_date'] = df['end_date'].dt.tz_convert('Australia/Melbourne')

df['start_day'] = df['start_date'].dt.date
df['start_time'] = df['start_date'].dt.time

df['end_day'] = df['end_date'].dt.date
df['end_time'] = df['end_date'].dt.time

df = df.sort_values("start_date")


df = df.loc[:, ['start_date', 'end_date'] + ['start_day','end_day'] + ['start_time', 'end_time'] + df.columns[2:-4].tolist()]
df

