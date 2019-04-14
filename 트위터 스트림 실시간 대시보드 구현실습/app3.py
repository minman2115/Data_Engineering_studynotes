# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request, url_for
import ast

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

labels = ['Waiting']
values = [0]

server = Flask(__name__)

@server.route('/test', methods=['GET'])
def test_api_request():
    print('IM IN ROUTE /TEST')
    return 'success'

@server.route('/update_data', methods=['POST'])
def update_data():
    print('IM IN ROUTE /UPDATE_DATA')
    
    global labels, values
    if not request.form or 'tag_count' not in request.form:
        return "error",400
    print(request)
    print(request.form)
    labels = ast.literal_eval(request.form['tag'])
    labels.reverse()
    values = ast.literal_eval(request.form['tag_count'])
    values.reverse()
    print("labels received: " + str(labels))
    print("data received: " + str(values))
    return "success",201

app = dash.Dash(__name__, server=server)

app.layout = html.Div(children=[
    html.H1('Twitter stream DashBoard'),

    dcc.Graph(
        id='live-update-graph'
    ),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):

    figure={
        'data': [
            go.Bar(x=values, 
                    y=labels,
                    orientation='h',
                    width=0.2)
        ],
        'layout': {
            'title': 'Dash Data Visualization 13'
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)

