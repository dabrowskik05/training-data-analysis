# %%
import pandas as pd
import glob
import os

folder_patch = "pdu-2025L-dane-csv/"

csv_files = glob.glob(os.path.join(folder_patch, "*.csv"))

data = []

for i, file in enumerate(csv_files):
    df1 = pd.read_csv(file)
    df1.insert(1, 'session_id', 1)
    df1.loc[:, 'session_id'] = i
    data.append(df1)

df = pd.concat(data)

unit_labels = {
    'timestamp': 'Full_Date',
    'position_lat@deg': 'Latitude (°)',
    'position_long@deg': 'Longitude (°)',
    'distance@km': 'Distance (km)',
    'enhanced_speed@km/h': 'Speed (km/h)',
    'enhanced_altitude@m': 'Altitude (m)',
    'heart_rate@bpm': 'Heart Rate (bpm)',
    'cadence@rpm': 'Cadence (rpm)',
    'temperature@C': 'Temperature (°C)',
    'fractional_cadence@rpm': 'Fractional Cadence (rpm)',
    'vertical_oscillation@mm': 'Vertical Oscillation (mm)',
    'stance_time_percent@percent': 'Stance Time (%)',
    'stance_time@ms': 'Stance Time (ms)',
    'vertical_ratio@percent': 'Vertical Ratio (%)',
    'stance_time_balance@percent': 'Stance Time Balance (%)',
    'step_length@mm': 'Step Length (mm)',
    'activity_type': 'Activity Type',
    'altitude@m': 'Raw Altitude (m)',
    'speed@km/h': 'Raw Speed (km/h)',
    'session_id' : 'session_id'
}

work_names = {
    'timestamp': 'Full_Date',
    'position_lat@deg': 'Latitude',
    'position_long@deg': 'Longitude',
    'distance@km': 'Distance',
    'enhanced_speed@km/h': 'Speed',
    'enhanced_altitude@m': 'Altitude',
    'heart_rate@bpm': 'Heart_Rate',
    'cadence@rpm': 'Cadence',
    'temperature@C': 'Temperature',
    'fractional_cadence@rpm': 'Fractional_Cadence',
    'vertical_oscillation@mm': 'Vertical_Oscillation',
    'stance_time_percent@percent': 'Stance_Time_Percent',
    'stance_time@ms': 'Stance_Time',
    'vertical_ratio@percent': 'Vertical_Ratio',
    'stance_time_balance@percent': 'Stance_Time_Balance',
    'step_length@mm': 'Step_Length',
    'activity_type': 'Activity_Type',
    'altitude@m': 'Raw_Altitude',
    'speed@km/h': 'Raw_Speed',
    'session_id' : 'session_id'
}
df.rename(columns=work_names, inplace=True)

df.loc[df.loc[:, 'Activity_Type'].isna(), 'Activity_Type'] = 'cycling'

# %%
