import dash_bootstrap_components as dbc
import datetime
import dash
import mysql
from dash import dcc
from dash import html
from getMetrics import getMetric
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from pyorbital.orbital import Orbital
from getData import getValues
import mysql.connector
import numpy as np
from database import mydbConnection
from mysql.connector import Error

from getTime import getTime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H3("Weather Station", style={'text-align': 'center'}),
        dcc.Dropdown(id="slct_device",
                     options=[
                         {'label': 'py_saxion', 'value': 'py_saxion'},
                         {'label': 'py_wierden', 'value': 'py_wierden'},
                         {'label': 'lht_wierden', 'value': 'lht_wierden'},
                         {'label': 'lht_gronau', 'value': 'lht_gronau'},
                         {'label': 'Alfreds Baby', 'value': 'Alfreds Baby'},
                     ],
                     value=['py_saxion'],
                     multi=True,
                     searchable=False,
                     clearable=False,
                     style={'width': "80%", 'margin-left': '10%'}
                     ),

        dcc.Dropdown(id="slct_time",
                     options=[
                         {"label": "1 Hour", "value": '1 Hour'},
                         {"label": "24 Hours", "value": '24 Hours'},
                         {"label": "1 Month", "value": '1 Month'},
                         {"label": "1 Year", "value": '1 Year'}],
                     multi=False,
                     value='1 Hour',
                     style={'width': "40%", 'margin-left': '30%'}
                     ),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 5000,  # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    temp = getMetric("temp", datetime.datetime.now())
    light = getMetric("light", datetime.datetime.now())
    pressure = getMetric("pressure", datetime.datetime.now())
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Temperature: {}'.format(temp), style=style),
        html.Span('Light: {}'.format(light), style=style),
        html.Span('Pressure: {}'.format(pressure), style=style)
    ]


@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    data = {
        'Temperature': [],
        'Light': [],
        'Pressure': [],
        'Time': []
    }
    data['Temperature'] = getValues("temp", "day")
    data['Light'] = getValues("light", "day")
    data['Pressure'] = getValues("pressure", "day")
    data['Time'] = getTime()

    # Create the graph with subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Temperature", "Light", "Pressure"))

    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 30
    }

    fig.add_trace({
        'x': data['Time'],
        'y': data['Temperature'],
        'name': 'Temperature',
        'mode': 'lines',
        'type': 'scatter'
    }, row=1, col=1)
    fig.add_trace({
        'x': data['Time'],
        'y': data['Light'],
        'name': 'Light',
        'mode': 'lines',
        'type': 'scatter'
    }, row=1, col=2)
    fig.add_trace({
        'x': data['Time'],
        'y': data['Pressure'],
        'name': 'Pressure',
        'mode': 'lines',
        'type': 'scatter'
    }, row=2, col=1)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
