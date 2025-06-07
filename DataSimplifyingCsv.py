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

df = df.groupby('session_id').agg(Date = ('Date', 'min'), Total_Distance = ('Distance', 'max'), 
    Avg_Speed = ('Speed', 'mean'), Max_Speed = ('Speed', 'max'), Min_Speed = ('Speed', 'min'), 
    Avg_Altitude = ('Altitude', 'mean'), Max_Altitude = ('Altitude', 'max'), Min_Altitude = ('Altitude', 'min'),
    Avg_Heart_Rate = ('Heart_Rate', 'mean'), Max_Heart_Rate = ('Heart_Rate', 'max'), Min_Heart_Rate = ('Heart_Rate', 'min'),
    Avg_Cadence = ('Cadence','mean'), Avg_Temperature = ('Temperature', 'mean'), Max_Temperature = ('Temperature', 'max'), Min_Temperature = ('Temperature', 'min'),
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
'''
# Group by activity type
df.loc[:, 'Activity_Type'].unique()
df_running = df.loc[df.loc[:, 'Activity_Type'] == 'running', :]
df_walking = df.loc[df.loc[:, 'Activity_Type'] == 'walking', :]
df_cycling = df.loc[~df.Activity_Type.isin(['running', 'walking']), :]
# %%
# All runs in one table
groups_running = [g for _, g in df_running.groupby(['Date', 'session_id'])]
groups_walking = [g for _, g in df_walking.groupby(['Date', 'session_id'])]
groups_cycling = [g for _, g in df_cycling.groupby(['Date', 'session_id'])]

# %%
one_ride = groups_cycling[1]
one_ride
one_run = groups_running[1]
one_run
#one_walk = groups_walking[5]
#one_walk
# %%

#show_case = df.groupby(['Date', 'session_id'], as_index=False).first().reset_index()
#show_case = show_case.loc[:, ['Full_Date', 'Date', 'Time'] + show_case.columns.tolist()[5:len(df.columns)-1] + ['session_id']]
# %%
#show_case.to_csv("zebrane_dane_json.csv", index = False)
'''

# %%
'''
Stance_Time = ('Stance_Time', 'mean'), Vertical_Ratio = ('Vertical_Ratio', 'mean'),
                    Stance_Time_Balance = ('Stance_Time_Balance', 'mean'), Step_Length = ('Step_Length', 'mean')


# %%
#########################################################################################################
#                TO DO
map_center = [np.mean(lon, axis=0), np.mean(lat, axis=0)]
run_map = folium.Map(location=map_center, zoom_start=14)

# Group by run (e.g., by date)
for run_date, group in df.groupby('Time'):
    coords = group[['Latitude', 'Longitude']].values.tolist()
    folium.PolyLine(coords, color='blue', weight=4.5, opacity=0.8, tooltip=str(run_date)).add_to(run_map)
    folium.Marker(coords[0], tooltip=f"Start: {run_date}").add_to(run_map)
    folium.Marker(coords[-1], tooltip=f"End: {run_date}", icon=folium.Icon(color="red")).add_to(run_map)

run_map.save("professor_runs_map.html")



# %%

#               TO DO
# Starting location – center of the run
start_location = [one_run['Latitude'].iloc[0], one_run['Longitude'].iloc[0]]

# Create the map
m = folium.Map(location=start_location, zoom_start=15)

# Add path as a line
locations = one_run[['Latitude', 'Longitude']].values.tolist()
folium.PolyLine(locations, color="blue", weight=2.5, opacity=1).add_to(m)

# Optionally add start and end markers
folium.Marker(locations[0], tooltip="Start").add_to(m)
folium.Marker(locations[-1], tooltip="End").add_to(m)

# Display the map
m

#########################################################################################################
'''