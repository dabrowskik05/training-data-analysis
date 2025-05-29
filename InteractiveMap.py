# %%
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import base64
from io import BytesIO
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import DataDownloadICsv as Dane
import DataMerge as DaneObrobione
import matplotlib.dates as mdates
import numpy as np

# %%
# Load your data
df_detailed = Dane.df
df_summary = DaneObrobione.summarised_df

# %%-

# App instance
app = Dash(__name__)

# === Function: Matplotlib chart with HR, Speed, Calories ===
def plot_hr_speed(data):
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 7), sharex=True)

    # Format x-axis: HH:MM
    time_fmt = mdates.DateFormatter('%H:%M')

    # Heart Rate
    ax1.plot(data['Full_Date'], data['Heart_Rate'], color='red')
    ax1.set_ylabel('Heart Rate (bpm)', color='red')
    ax1.tick_params(axis='y', labelcolor='red')
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(time_fmt)

    # Speed
    ax2.plot(data['Full_Date'], data['Speed'], color='blue')
    ax2.set_ylabel('Speed (km/h)', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.grid(True)
    ax2.xaxis.set_major_formatter(time_fmt)

    ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right', color='white')


    fig.suptitle('Heart Rate & Speed Over Time', color='white')
    plt.tight_layout()

    # Converts the plot into a PNG image that can be embedded in HTML.
    buf = BytesIO()
    plt.savefig(buf, format="png", facecolor='#111')  # match background
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getbuffer()).decode("utf8")

# === Function: Map plot ===
def make_map_figure(d):
    fig = go.Figure()

    # Only path trace
    fig.add_trace(go.Scattermapbox(
        lat=d["Latitude"],
        lon=d["Longitude"],
        mode="lines",
        name="Path",
        line=dict(color="blue", width=3)
    ))

    fig.update_layout(
        mapbox=dict(style="open-street-map",
                    center={"lat": np.mean(d["Latitude"]), "lon": np.mean(d["Longitude"])},
                    zoom=12),
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig

# === Layout ===
app.layout = html.Div([
    html.H1("Run Visualizer", style={"color": "white"}),
    dcc.Dropdown(
        id="session-dropdown",
        options=[{"label": str(s_id), "value": s_id} for s_id in df_summary['session_id']],
        value=df_summary['session_id'].iloc[0],
        style={"width": "50%"}
    ),
    html.Br(),
    html.Div(id="summary-box", style={"padding": "12px", "color": "white"}),
    dcc.Graph(id="map"),
    html.H2("Heart Rate, Speed & Calories", style={"color": "white", }),
    html.Img(id="hr-speed-img", style={"width": "100%", "border": "1px solid #ccc"})
], style={"backgroundColor": "#111", "padding": "20px"})

# === Callback ===
@app.callback(
    [Output("map", "figure"),
     Output("summary-box", "children"),
     Output("hr-speed-img", "src")],
    [Input("session-dropdown", "value")]
)
def update_dashboard(session_id):
    d = df_detailed[df_detailed['session_id'] == session_id].copy()
    s = df_summary[df_summary['session_id'] == session_id].iloc[0]
    duration = (d['Full_Date'].max() - d['Full_Date'].min()).total_seconds() / 60

    summary = html.Div([
        html.H3("Summary", style={"color": "white"}),
        html.P(f"Date: {s['Start_Date'].date()}"),
        html.P(f"Total Distance: {s['Total_Distance']:.2f} km"),
        html.P(f"Duration: {duration:.1f} min"),
        html.P(f"Calories Burned: {s['Calories']:.0f} kcal"),
        html.P(f"Average Heart Rate: {s['Avg_Heart_Rate']:.0f} bpm"),
        html.P(f"Average Speed: {s['Avg_Speed']:.2f} m/s"),
        html.P(f"Activity Type: {d['Activity_Type'].iloc[0]}"),
        html.P(f"Average Tempereature during the run: {s['Avg_Temperature']:.0f} C°")
    ])

    return make_map_figure(d), summary, plot_hr_speed(d)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

# %%
