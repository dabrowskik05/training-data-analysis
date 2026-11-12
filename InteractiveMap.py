# %%
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import DataDownloadICsv as Dane
import DataMerge as DaneObrobione
import matplotlib.dates as mdates
import numpy as np

# %%
df_detailed = Dane.df
df_summary = DaneObrobione.summarised_df

# %%-

# App instance
app = Dash(__name__)

# Matplotlib chart with HR and Speed 
def plot_hr_speed(data):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 7), sharex=True)

    # Format x-axis like HH:MM
    time_format = mdates.DateFormatter('%H:%M')

    # Heart Rate plot
    ax1.plot(data.loc[:, 'Full_Date'], data.loc[:, 'Heart_Rate'], color='red')
    ax1.set_ylabel('Heart Rate (bpm)', color='red')
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(time_format)

    # Speed plot
    ax2.plot(data.loc[:, 'Full_Date'], data.loc[:, 'Speed'], color='blue')
    ax2.set_ylabel('Speed (km/h)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.grid(True)
    ax2.xaxis.set_major_formatter(time_format)

    ax2.xaxis.set_major_locator(mdates.AutoDateLocator()) # pretty date format

    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right', color='white') # rotation of date ticks


    fig.suptitle('Heart Rate & Speed Over Time', color='white')
    plt.tight_layout()

    # Converts the plot into a PNG image that can be embedded in HTML.
    buf = BytesIO()
    plt.savefig(buf, format="png", facecolor='#111')  # match background
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getbuffer()).decode("utf8") 

# Map plot 
def make_map_figure(data):
    fig = go.Figure()

    # Path trace
    fig.add_trace(go.Scattermapbox(
        lat=data["Latitude"],
        lon=data["Longitude"],
        mode="lines",
        name="Path",
        line=dict(color="blue", width=3)
    ))

    # Fatigue intervals
    fatigue_intervals = detect_fatigue_intervals(data, window=4)

    add_legend = False
    for start, end in fatigue_intervals:
        fig.add_trace(go.Scattermapbox(
            lat=data["Latitude"].iloc[start:end],
            lon=data["Longitude"].iloc[start:end],
            mode="lines",
            name="Fatigue",
            line=dict(color="orange", width=4),
            hoverinfo="none",
            showlegend = not add_legend
        ))
        add_legend = True

    # Start marker
    fig.add_trace(go.Scattermapbox(
        lat=[data.iloc[0]["Latitude"]],
        lon=[data.iloc[0]["Longitude"]],
        mode="markers",
        name="Start",
        marker=dict(size=14, color="green", symbol="circle"),
        hoverinfo="text",
        text=["Start"]
    ))
    
    # Stop marker
    fig.add_trace(go.Scattermapbox(
        lat=[data.iloc[-1]["Latitude"]],
        lon=[data.iloc[-1]["Longitude"]],
        mode="markers",
        marker=dict(size=14, color="red", symbol="circle"),
        name="End",
        hoverinfo="text",
        text=["End"]
    ))


    fig.update_layout(
        mapbox=dict(style="open-street-map",
                    center={"lat": np.mean(data.loc[:, "Latitude"]), "lon": np.mean(data.loc[:, "Longitude"])}, # setting the center of the map
                    zoom=12),
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0} # margins right, top, left, bottom
    )
    return fig

# Layout 
app.layout = html.Div([  # new section
    html.H1("Map of Run and Stats", style={"color": "white"}),
    dcc.Dropdown(                   # dropdown to choose the number of session
    id="session-dropdown",
    options=[
        {
            "label": f"{session_id} — {df_summary[df_summary['session_id'] == session_id]['Start_Date'].dt.date.values[0]}",
            "value": session_id
        }
        for session_id in df_summary['session_id']
    ],
    value=df_summary['session_id'].iloc[0],
    style={"width": "50%"}
),
    html.Br(),      # break line
    html.Div(id="summary-box", style={"padding": "12px", "color": "white"}), 
    dcc.Graph(id="map"),        # placeholder for map
    html.H2("Heart Rate, Speed & Calories", style={"color": "white", }), 
    html.Img(id="hr-speed-img", style={"width": "100%", "border": "1px solid #ccc"})    # placeholder for charts
], style={"backgroundColor": "#111", "padding": "20px"})


# detects fatigue interval where heart rate increase and speed decrease in minimum 'window' next points and return the list of intervals
def detect_fatigue_intervals(data, window):
    
    data = data.copy()
    data['HR_Diff'] = data.loc[: ,'Heart_Rate'].diff()
    data['Speed_Diff'] = data.loc[: ,'Speed'].diff()

    fatigue_points = (data.loc[:, 'HR_Diff'] > 0) & (data.loc[:, 'Speed_Diff'] < 0)

    fatigue_ranges = []
    start = None

    for i, point in enumerate(fatigue_points):
        if point:
            if start is None:
                start = i
        else:
            if start is not None:
                if i - start >= window:
                    fatigue_ranges.append((start, i))
                start = None

    # if end of data is still fatigue
    if start is not None and len(data) - start >= window:
        fatigue_ranges.append((start, len(data)))

    return fatigue_ranges

# Callback
@app.callback(
    [Output("map", "figure"), # updates the map
     Output("summary-box", "children"), # updates the summary box
     Output("hr-speed-img", "src")], # update charts
    [Input("session-dropdown", "value")] # get the session id and updates the rest
)
def update_dashboard(session_id):
    session_data = df_detailed[df_detailed.loc[:, 'session_id'] == session_id].copy() 
    session_summary = df_summary[df_summary.loc[:, 'session_id'] == session_id].iloc[0] 
    duration = (session_data.loc[:, 'Full_Date'].max() - session_data.loc[:, 'Full_Date'].min()).total_seconds() / 60

    summary = html.Div([          # summary box
        html.H3("Summary", style={"color": "white"}),
        html.P(f"Date: {session_summary['Start_Date'].date()}"),
        html.P(f"Total Distance: {session_summary['Total_Distance']:.2f} km"),
        html.P(f"Duration: {duration:.1f} min"),
        html.P(f"Calories Burned: {session_summary['Calories']:.0f} kcal"),
        html.P(f"Average Heart Rate: {session_summary['Avg_Heart_Rate']:.0f} bpm"),
        html.P(f"Average Speed: {session_summary['Avg_Speed']:.2f} km/h"),
        html.P(f"Activity Type: {session_summary['Activity_Type']}"),
        html.P(f"Average Tempereature during the run: {session_summary['Avg_Temperature']:.0f} C°")
    ])

    return make_map_figure(session_data), summary, plot_hr_speed(session_data)

if __name__ == '__main__':
    app.run(debug=True)

# http://127.0.0.1:8050/

# %%
