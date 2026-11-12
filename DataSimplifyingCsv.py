# %%
import pandas as pd
import numpy as np
import DataDownloadICsv as Dane

df = Dane.df
unit_labels = Dane.unit_labels

# %%

df.dropna(axis=0, subset=['Full_Date', 'Latitude', 'Longitude'], inplace=True)
df.reset_index()
lon = df['Latitude']
lat =  df['Longitude']

df['Full_Date'] = pd.to_datetime(df['Full_Date'])
df['Full_Date'] = df['Full_Date'].dt.tz_convert('Australia/Melbourne')

df['Date'] = df['Full_Date'].dt.date
df['Time'] = df['Full_Date'].dt.time


df = df.loc[:, ['Full_Date', 'Date', 'Time'] + df.columns.to_list()[1:len(df.columns)-2]]

# %%
# Aggregating sessions into one record

df = df.groupby('session_id').agg(Date = ('Date', 'min'), Total_Distance = ('Distance', 'max'), Avg_Speed = 
    ('Speed', 'mean'), Max_Speed = ('Speed', 'max'), Min_Speed = ('Speed', 'min'), Avg_Altitude = ('Altitude', 'mean'), 
    Max_Altitude = ('Altitude', 'max'), Min_Altitude = ('Altitude', 'min'), Avg_Heart_Rate = ('Heart_Rate', 'mean'), 
    Max_Heart_Rate = ('Heart_Rate', 'max'), Min_Heart_Rate = ('Heart_Rate', 'min'), Avg_Cadence = ('Cadence','mean'),
      Avg_Temperature = ('Temperature', 'mean'), Max_Temperature = ('Temperature', 'max'), Min_Temperature = ('Temperature', 'min'),
    Fractional_Cadence = ('Fractional_Cadence', 'mean'), Vertical_Oscillation = ('Vertical_Oscillation', 'mean'),
    Stance_Time_Percent = ('Stance_Time_Percent', lambda x: x.iloc[-1] ), Stance_Time = ('Stance_Time', lambda x: x.iloc[-1]),
    Vertical_Ratio = ('Vertical_Ratio', 'mean'), Stance_Time_Balance = ('Stance_Time_Balance', lambda x: x.iloc[-1]),
    Step_Length = ('Step_Length', 'mean'), Activity_Type = ('Activity_Type', lambda x: x.iloc[-1]) ).reset_index()

df = df.sort_values('Date')

df.loc[:, 'session_id'] = np.arange(len(df.iloc[:, 0]))

df.reset_index(drop=True)
# %%

df.to_csv("zebrane_dane_csv.csv", index=False)

# %%
