# -----------------------------------------------------------------------------
# Importing the modules
# -----------------------------------------------------------------------------
import paho.mqtt.client as mqtt
import subprocess
#----------------------------------
from dash import Dash, html, dcc, Input, Output, State
from collections import deque
from datetime import datetime
import plotly.graph_objects as go
#----------------------------------
# Add as many emg values depending on application needs
global current_emg1, current_emg2
current_emg1 = "NaN"
current_emg2 = "NaN"

#------------------------------------
# Reading CSV Files
# Replace CSV File Names as needed
import pandas as pd

df = pd.read_csv('sample_motion.csv')
X_data = df['X']
Y_data = df['Y']
Z_data = df['Z']

df_cdc = pd.read_csv('sample_strain.csv')

df_emg = pd.read_csv('sample_emg.csv')



external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    }
]

# Initializing our Time (x) and EMG (y) data structures
time_Values1 = deque(maxlen=20)
emg_Values1 = deque(maxlen=20)

time_Values2 = deque(maxlen=20)
emg_Values2 = deque(maxlen=20)

# -----------------------------------------------------------------------------
# MQTT Subscribe
# -----------------------------------------------------------------------------
mqttc = mqtt.Client()
mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)

# Runs the publish.py script as a background process (to continuously deliver data)
# Following Methods only needed for bluetooth stream data
def run_publish():
    subprocess.Popen(['python3', 'publish.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("sensor/emg1")
    mqttc.subscribe("sensor/emg2")
    run_publish()

def on_message(client, userdata, msg):
    global current_emg1, current_emg2

    topic = msg.topic
    payload = msg.payload.decode()
    if topic == "sensor/emg1":
        current_emg1 = payload
    elif topic == "sensor/emg2":
        current_emg2 = payload

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.loop_start()

# -----------------------------------------------------------------------------
# Defining Dash app
# -----------------------------------------------------------------------------
app = Dash(__name__, external_stylesheets=external_stylesheets, update_title=None)
app.title = "PRS Health Monitoring System"

# Add as many sections needed for graph
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="PRS Health Monitoring System", className="header-title"
                ),
            ],
            className="header",
        ), 
        html.Div(
            children=[      
                html.Div(
                    children=[     
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.H1(
                                            children="Patient ID:",
                                            style={
                                            "text-align": "center",
                                            "margin-top": "20px",
                                            "font-size": "25px",
                                            },
                                        ),
                                    ],
                                ),
                        html.Div(
                            children=[
                                html.H1(
                                    children="Name:",
                                    style={
                                    "text-align": "left",
                                    "display": "inline-block",
                                    "font-size": "25px",
                                    "margin-left": "15px",
                                    },
                                ),
                            html.H1(
                                children="Birthday:",
                                style={
                                "text-align": "right",
                                "display": "inline-block",
                                "font-size": "25px",
                                "margin-left": "185px",
                            },
                        ),
                    ],
                    ),
                    html.H1(
                        children="Session:",
                        style={
                        "text-align": "left",
                        "margin-top": "20px",
                        "font-size": "25px",
                        "margin-left": "15px",
                        },
                    ),
                    html.H1(
                        children="New Session",
                        className="panelButton",
                        style={
                        "margin-left": "80px",
                        },
                    ),
                    html.H1(
                        children="Start",
                        className="panelButton",
                    ),
                    html.H1(
                        children="Export",
                        className="panelButton",
                    ),
            ],
            className="card",
            style={"height": "300px"}
        ),
                html.Div([
                    dcc.Graph(id='ble-test1-graph', animate=False, config={'displayModeBar': False}, ),
                    dcc.Interval(
                            id='ble-test1-interval',
                            interval=1000,
                            n_intervals=0,
                       ),
                    ],
                        className="card"
                ),
                html.Div([
                    dcc.Graph(id='ble-test2-graph', animate=True, config={'displayModeBar': False}, ),
                    dcc.Interval(
                            id='ble-test2-interval',
                            interval=1000,
                            n_intervals=0,
                       ),
                    ],
                        className="card"
                ),
                html.Div([
                    dcc.Graph(id='ble-test3-graph', config={'displayModeBar': False}, ),
                    dcc.Interval(
                            id='ble-test3-interval',
                            interval=1000,
                            n_intervals=0,
                       ),
                    ],
                        className="card"
                ),
            ],
            className="grid",
        ),
    ],
    className="wrapper",
        ),
    ],
    style={'height': '300px'},
)

# -----------------------------------------------------------------------------
# Callback for updating Sample Motion data
# -----------------------------------------------------------------------------
# Each graph requires a callback (add more depending on number of graphs)
@app.callback(
    Output('ble-test1-graph', 'figure'),
    [Input('ble-test1-graph', 'n_intervals'),
     Input('ble-test1-graph', 'relayoutData')],
    State('ble-test1-graph', 'figure'),
)
def update_ble_test1_graph(n_intervals, relayout_data, current_figure):
    fig = go.Figure(current_figure)
    fig.data = []
    fig.add_trace(go.Scatter(x=df.index, y=X_data, mode='lines', name='X'))
    fig.add_trace(go.Scatter(x=df.index, y=Y_data, mode='lines', name='Y'))
    fig.add_trace(go.Scatter(x=df.index, y=Z_data, mode='lines', name='Z'))
    fig.update_layout(
        title='Sample Motion Data',
        xaxis=dict(title='Sample #'),
        yaxis=dict(title='Value'),
    )
    fig.update_layout(legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='center', x=0.5))
    
    return fig

# -----------------------------------------------------------------------------
# Callback for updating Sample Strain data
# -----------------------------------------------------------------------------
@app.callback(
    Output('ble-test2-graph', 'figure'),
    [Input('ble-test2-graph', 'n_intervals'),
     Input('ble-test2-graph', 'relayoutData')],
    State('ble-test2-graph', 'figure'),
)
def update_ble_test2_graph(n_intervals, relayout_data, current_figure):
    fig = go.Figure(current_figure)
    
    # Clear existing traces
    fig.data = []
    
    # Update graph data with CDC data and set legend label
    fig.add_trace(go.Scatter(x=df_cdc.index, y=df_cdc['CDC'], mode='lines', name='CDC'))
    
    # Update layout
    fig.update_layout(title='Sample Strain Data', xaxis_title='Sample #', yaxis_title='Value', showlegend=True)
    
    return fig

# -----------------------------------------------------------------------------
# Callback for updating Sample EMG data
# -----------------------------------------------------------------------------
@app.callback(
    Output('ble-test3-graph', 'figure'),
    [Input('ble-test3-graph', 'n_intervals'),
     Input('ble-test3-graph', 'relayoutData')],
    State('ble-test3-graph', 'figure'),
)
def update_ble_test3_graph(n_intervals, relayout_data, current_figure):
    fig = go.Figure(current_figure)
    
    # Clear existing traces
    fig.data = []
    
    # Update graph data with EMG data
    for column in df_emg.columns[1:]:
        fig.add_trace(go.Scatter(x=df_emg['Sample'], y=df_emg[column], mode='lines', name=f'Channel {column[-1]}'))
    
    # Update layout
    fig.update_layout(title='Sample EMG Data', xaxis_title='Sample #', yaxis_title='Value',
                      yaxis=dict(tickvals=[-5000000, -2500000, 0, 2500000, 5000000],
                                 ticktext=['-5M', '-2.5M', '0', '2.5M', '5M']),
                                 xaxis=dict(tickmode='linear', tick0=0, dtick=10000))
    
    
    return fig
# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)