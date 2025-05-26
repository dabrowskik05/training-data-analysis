# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
import seaborn as sns
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import DataDownloadICsv as Dane
import DataSimplifyingCsv as DaneObrobione
# %%
df = Dane.df
df_summarised = DaneObrobione.df
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
df = df.sort_values('Date')
# %%

# Initialize app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Interactive Exercise Viewer"),
    dcc.Dropdown(
        id="session-dropdown",
        options=[{"label": f"Session {sid}", "value": sid} for sid in df['session_id'].unique()],
        value=df['session_id'].iloc[0],
        style={'width': '50%'}
    ),
    html.Div(id="summary-box"),
    dcc.Graph(id="map"),
    dcc.Graph(id="time-series"),
])

# Callbacks
@app.callback(
    [Output("map", "figure"),
     Output("time-series", "figure"),
     Output("summary-box", "children")],
    [Input("session-dropdown", "value")]
)
def update_dashboard(session_id):
    d = df[df['session_id'] == session_id]
    d_sum = df_summarised[df_summarised['session_id'] == session_id]

    # MAP
    map_fig = px.line_mapbox(d,
                              lat="Latitude",
                              lon="Longitude",
                              color_discrete_sequence=["blue"],
                              zoom=15,
                              height=400)
    map_fig.update_layout(mapbox_style="open-street-map")

    # TIME SERIES: e.g., Heart Rate
    time_fig = px.line(d, x="Full_Date", y="Heart_Rate", title="Heart Rate Over Time")

    # STATS SUMMARY
    total_dist = d_sum['Total_Distance'].iloc[0]
    duration = (pd.to_datetime(d['Full_Date'].iloc[-1]) - pd.to_datetime(d['Full_Date'].iloc[0])).total_seconds() / 60
    avg_hr = d_sum['Avg_Heart_Rate'].iloc[0]
    avg_speed = d_sum['Avg_Speed'].iloc[0]

    summary = html.Div([
        html.H4("Summary"),
        html.P(f"Total Distance: {total_dist:.2f} km"),
        html.P(f"Duration: {duration:.1f} min"),
        html.P(f"Avg Heart Rate: {avg_hr:.0f} bpm"),
        html.P(f"Avg Speed: {avg_speed:.2f} m/s"),
    ])

    return map_fig, time_fig, summary

# Run app
if __name__ == '__main__':
    app.run(debug=True)
# %%
