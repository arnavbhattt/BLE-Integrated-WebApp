# -----------------------------------------------------------------------------
# Importing the modules
# -----------------------------------------------------------------------------
import paho.mqtt.client as mqtt
#----------------------------------
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from collections import deque
from datetime import datetime
import plotly.graph_objects as go
#----------------------------------
global current_emg1, current_emg2 # add as many emg values depending on application needs
current_emg1 = "NaN"
current_emg2 = "NaN"

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
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

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("sensor/emg1")
    mqttc.subscribe("sensor/emg2")

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
                    dcc.Graph(id='ble-test2-graph', animate=False, config={'displayModeBar': False}, ),
                    dcc.Interval(
                            id='ble-test2-interval',
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
# Callback for updating temperature data
# -----------------------------------------------------------------------------
@app.callback(
    Output('ble-test1-graph', 'figure'),
    Input('ble-test1-interval', 'n_intervals'),
    State('ble-test1-graph', 'figure'),
)
def update_ble_test1_graph(n_intervals, current_figure):
    global timeValues1, emg_Values1, current_emg1
   
    # Returns current state of figure of no data is available
    if current_emg1 == "NaN":
        current_emg1 = 0

    # Updating the deque with new time and EMG values
    current_time = datetime.now().strftime('%M:%S')
    time_Values1.append(current_time)
    emg_Values1.append(float(current_emg1))

    # Updating the figure as per the graph display
    fig_BLE_Test1 = go.Figure()
    fig_BLE_Test1.add_trace(go.Scatter(x=list(time_Values1), y=list(emg_Values1), mode='lines', name='BLE Test Data (2)', line=dict(color='blue')))
    fig_BLE_Test1.update_layout(
        title='<b>BLE Test Data (1)<b>',
        title_x=0.95,
        xaxis=dict(title='<b>Time (s)<b>', range=[min(time_Values1), max(time_Values1)], tickmode='linear', tick0=0, dtick=5),
        yaxis=dict(title='<b>EMG (mV)<b>', range=[1, 5], tickvals=[1, 2, 3, 4, 5], ticktext=['1 mV  ', '2 mV  ', '3 mV  ', '4 mV  ', '5 mV  '], title_standoff=10),
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_gridcolor='lightgray',
        yaxis_gridcolor='lightgray',
        height=300,
    )
    return fig_BLE_Test1

@app.callback(
    Output('ble-test2-graph', 'figure'),
    Input('ble-test2-interval', 'n_intervals'),
    State('ble-test2-graph', 'figure'),
)
def update_ble_test1_graph(n_intervals, current_figure):
    global timeValues2, emg_Values2, current_emg2
   
    # Returns current state of figure of no data is available
    if current_emg2 == "NaN":
        current_emg2 = 0

    # Updating the deque with new time and EMG values
    current_time = datetime.now().strftime('%M:%S')
    time_Values2.append(current_time)
    emg_Values2.append(float(current_emg2))

    # Updating the figure as per the graph display
    fig_BLE_Test2 = go.Figure()
    fig_BLE_Test2.add_trace(go.Scatter(x=list(time_Values2), y=list(emg_Values2), mode='lines', name='BLE Test Data (2)', line=dict(color='red')))
    fig_BLE_Test2.update_layout(
        title='<b>BLE Test Data (2)<b>',
        title_x=0.95,
        xaxis=dict(title='<b>Time (s)<b>', range=[min(time_Values2), max(time_Values2)], tickmode='linear', tick0=0, dtick=5),
        yaxis=dict(title='<b>EMG (mV)<b>', range=[1, 5], tickvals=[1, 2, 3, 4, 5], ticktext=['1 mV  ', '2 mV  ', '3 mV  ', '4 mV  ', '5 mV  '], title_standoff=10),
        xaxis_showgrid=True,
        yaxis_showgrid=True,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_gridcolor='lightgray',
        yaxis_gridcolor='lightgray',
        height=300,
    )
    return fig_BLE_Test2

# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)