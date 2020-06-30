import copy
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import numpy as np
import os
import pandas as pd
import plotly
import time

from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from flask import Flask
from plotly import graph_objs as go
from plotly.graph_objs import *


app = dash.Dash(__name__)
server = app.server

# Datasets



fleet_data = pd.read_csv('../cleaned-data-for-fleet-dna_v3.csv')
fleet_data.drop_duplicates(keep=False,inplace=True)

dfnames = pd.read_csv('../names/names.csv')
#rounded data
fleet_data_rounded = fleet_data.round(decimals=2)


df_vehicle = fleet_data[['vid','vehicle_class', 'vocation', 'vehicel_type', 'drivetrain_type','pid']].copy()
df_vehicle = df_vehicle.drop_duplicates(subset=None, keep='first', inplace=False)

df_vehicle_class = fleet_data[['vehicle_class','vid', 'fuel_type', 'vocation','vehicel_type']].copy()
df_vehicle_class = df_vehicle_class.drop_duplicates(subset=None, keep='first', inplace=False)


df_group_vehicle_class = fleet_data.groupby(["vehicle_class"], as_index=False)["vid"].count()
df_group_vehicle_class.columns = (["Klasse", "anzahl"])
df_group_vehicle_class = df_group_vehicle_class.drop_duplicates(subset=None, keep='first', inplace=False)


df_driver = pd.merge(df_vehicle, dfnames, how='left', on='pid').copy()
df_driver = df_driver.rename(columns={"pid": "pp"}).copy()


#available_vid = fleet_data_rounded['vid'].unique()

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

layout = dict(
    autosize=True,
    height=450,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=45,
        r=15,
        b=45,
        t=35
    )
)

# Layout
app.layout = html.Div([
    # Title - Row
    html.Div(
        [
            html.H1(
                'Test App',
                style={'font-family': 'Helvetica',
                       "margin-left": "20",
                       "margin-bottom": "0"},
                className='eight columns',
            )
        ],
        className='row'
    ),

    #block 2
    html.Div([
        dcc.Store(id = 'memory'),
        html.H3('Cars'),
        html.Div(
            [
                html.Div(
                    [
                        html.P('Models:'),
                        dcc.Dropdown(
                                id = 'filter_x',
                                options=[
                                    {'label': 'No filter', 'value': 0},
                                    {'label': '2', 'value': 1},
                                    {'label': '3', 'value': 2},
                                    {'label': '4', 'value': 3}
                                ],
                                value='0'
                        ),
                    ],
                    className='three columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Price:'),
                        dcc.Dropdown(
                                id = 'filter_y',
                                options=[
                                    {'label': 'No filter', 'value': 0},
                                    {'label': '1 to 20k', 'value': 1},
                                    {'label': '20k to 30k', 'value': 2},
                                    {'label': '30k+', 'value': 3}
                                ],
                                value='0'
                        )
                    ],
                    className='three columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.Button('Reset Chart', id='button_chart')
                    ],
                    className='one columns',
                    style={'margin-top': '40'}
                ),
                html.Div(
                    [
                        html.Button('Previous Level', id='back_button')
                    ],
                    className='one columns',
                    style={'margin-top': '40', 'margin-left':'50'}
                )
            ],
            className='row'
        ),

        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='chart-2')
                    ], className = "four columns", style = {'margin-top': 35,
                                                            'padding': '15',
                                                            'border': '1px solid #C6CCD5'}
                ),
                html.Div(id = 'table-box'),
                html.Div(dt.DataTable(id = 'table', data=[{}]), style={'display': 'none'})
            ], className = 'row'
        )
    ], className = 'row',  style = {'margin-top': 20, 'border':
                                    '1px solid #C6CCD5', 'padding': 15,
                                    'border-radius': '5px'})
], style = {'padding': '25px'})

#Table function
def make_table(data, output):
    return html.Div(
    [
        dt.DataTable(
            id = output,
            data=data.to_dict('rows'),
            columns=[{'id': c, 'name': c} for c in data.columns],
            selected_rows=[],
            style_cell={'padding': '5px',
                        'whiteSpace': 'no-wrap',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'maxWidth': 0,
                        'height': 30,
                        'textAlign': 'left'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'color': 'black'

            },


        ),
    ], className="seven columns", style = {'margin-top': '35',
                                           'margin-left': '15',
                                           'border': '1px solid #C6CCD5'}
)

def make_chart(df, x, y, label = 'Author', size = 'Size'):
    graph = []
    if size == '':
        s = 15
    else:
        s = df[size]
    graph.append(go.Scatter(
            x=df[x],
            y=df[y],
            mode='markers',
            text = ['{}: {}'.format(label, a) for a in df[label]],
            opacity=0.7,
            marker={
                'size': s,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name='X'
        ))

    return graph

# Callbacks and functions
@app.callback(dash.dependencies.Output('memory', 'data'),
              [dash.dependencies.Input('table', 'selected_cells'),
               dash.dependencies.Input('table', 'derived_virtual_data')],
              [dash.dependencies.State('memory', 'data')])
def tab(sel, table, state):
    # to initialize variables when it is None
    if state is None:
        state = {}
    if table is None:
        state['data'] = df_group_vehicle_class.to_dict('records')
        table = [{}]
    else:
        state['data'] = table #save current table value afer it gets initialized

    # store information of selected rows to retrieve them when back button is clicked
    # information is stored in json format
    #
    if sel:
        if 'vid' in table[0].keys():
            state['vid'] = table[0]['vid']
        if 'vehicle_class' in table[0].keys() and table is not None:
            state['vehicle_class'] = table[0]['vehicle_class']

    return state

@app.callback(
    dash.dependencies.Output('table-box', 'children'),
    [dash.dependencies.Input('filter_x', 'value'),
    dash.dependencies.Input('filter_y', 'value'),
    dash.dependencies.Input('button_chart', 'n_clicks_timestamp'),
    dash.dependencies.Input('back_button', 'n_clicks_timestamp'),
    dash.dependencies.Input('table', 'selected_cells')],
    [dash.dependencies.State('memory', 'data')])
def update_image_src(fx, fy, button, back, selected_cell, current_table):
    res = df_group_vehicle_class.copy()
    if fx == 1:
        res = res[res['vehicle_class'] == 2]
    if fx == 2:
        res = res[res['vehicle_class'] == 3]


    # Reset Chart Button conditionals
    # stamp: actual timestamp
    # button: timestamp of button click
    # if stamp == button then there's a new click. The str transformation was
    # necessary as time.time() returns 10 digits and button 13 digits
    # ex.: time.time() --> 1548657188 button -->1548657188440
    if button is None:
        button = 0
    stamp = str(time.time())[:10]
    if stamp == str(button)[:10]:
        return make_table(res, 'table')

    # Retrieves data saved in browser memory to remember previous level selection
    # then apply to previous level dataset
    # ex.: if select Honda --> Civic --> back button, when back button is clicked
    # it will remember to show only Honda cars
    #if back is None:
     #   back = 0
    #stamp = str(time.time())[:10]
    #if stamp == str(back)[:10]:
     #   if 'Price' in current_table['data'][0].keys():
      #      return make_table(res, 'table')
       # if 'Date' in current_table['data'][0].keys():
        #    return make_table(models[models['Brand'] == current_table['Brand']], 'table')

    # When selection occurs, the code looks for the current table and based on a
    # differentiator column (unique among all datasets) it decides the next level table
    # ex.: if Average Price is in current table columns, then current table is "brands"
    # and next table is "models"
    if selected_cell:
        print(current_table)
        if 'Klasse' in current_table['data'][0].keys():
            res = df_vehicle[df_vehicle['vehicle_class'] == current_table['data'][list(selected_cell)[0]['row']]['Klasse']]
        if 'pid' in current_table['data'][0].keys():
            res = df_driver[df_driver['pp'] == current_table['data'][list(selected_cell)[0]['row']]['pid']]

    return make_table(res, 'table')

@app.callback(
    dash.dependencies.Output('chart-2', 'figure'),
    [dash.dependencies.Input('table', 'data')])
def update_image_src(data):
    layout_individual = copy.deepcopy(layout)
    layout_individual['legend'] = legend=dict(x=0.05, y=1)

    df = pd.DataFrame(data)
    graph = []

    # The callback retrieve the new data after click and based on its columns,
    # we decide the x axis, y axis, label and size of dots to pass to make_chart()
    if 'Average Price' in data[0].keys():
        layout_individual['title'] = 'Chart XYZ'
        layout_individual['xaxis'] = dict(title='Models')
        layout_individual['yaxis'] = dict(title='Average Price')
        graph = make_chart(pd.DataFrame(data), 'Models', 'Average Price', 'Brand', '')

    if 'Price' in data[0].keys():
        layout_individual['title'] = 'Chart XYZ 2'
        layout_individual['xaxis'] = dict(title='Price')
        layout_individual['yaxis'] = dict(title='Sales')
        graph = make_chart(pd.DataFrame(data), 'Price', 'Sales', 'Model', 'Sales')

    if 'Date' in data[0].keys():
        layout_individual['title'] = 'Chart XYZ 3'
        layout_individual['xaxis'] = dict(title='X')
        layout_individual['yaxis'] = dict(title='Y')
        graph = make_chart(pd.DataFrame(data), 'x', 'y', 'Model', '')

    figure = {
        'data': graph,
        'layout': layout_individual
    }

    return figure

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)