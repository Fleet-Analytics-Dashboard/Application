import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go

#Daten

fleet_data = pd.read_csv('../batch-data/cleaned-data-for-fleet-dna.csv')
fleet_data = fleet_data.head(10) # limits the displayed rows to 10
#fleet_data.iloc[:,1:3]


#PieCharts

#Downtimes Overview

labels = ['Accidents','Traffic Jams','Maintenance','Unused']
values = [20, 30, 10, 40]

pie1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#Need for Maintenance

labels = ['Need','Soon','No need']
values = [2, 5, 10]

pie2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#Accident Probability

labels = ['Category 1','Category 2','Category 3']
values = [20, 30, 10, 40]

pie3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

#Mapbox
#mapbox_access_token = open(".mapbox_token").read()

fig = go.Figure(go.Scattermapbox(
        lat=['38.91427','38.91538','38.91458',
             '38.92239','38.93222','38.90842',
             '38.91931','38.93260','38.91368',
             '38.88516','38.921894','38.93206',
             '38.91275'],
        lon=['-77.02827','-77.02013','-77.03155',
             '-77.04227','-77.02854','-77.02419',
             '-77.02518','-77.03304','-77.04509',
             '-76.99656','-77.042438','-77.02821',
             '-77.01239'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=["Truck 1","Truck 2","Truck 3",
             "Truck 4","Truck 5","Truck 6",
             "Truck 7","Truck 8","Truck 9",
             "Truck 10","Truck 11","Truck 12",
             "Truck 13"],
    ))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken='pk.eyJ1IjoiamFrb2JzY2hhYWwiLCJhIjoiY2tiMWVqYnYwMDEyNDJ5bWF3YWhnMTFnNCJ9.KitYnq2a645C15FwvFdqAw',
        bearing=0,
        center=dict(
            lat=38.92,
            lon=-77.07
        ),
        pitch=0,
        zoom=10
    ),
)






page_layout = html.Div([

#Tab-Layout

    dcc.Tabs([

#Downtimes View

        dcc.Tab(label='Downtimes', children=[
        #html.H2('Downtimes'),
#Row 1
        html.Div([

                html.Div([
                    html.Div(
                        html.H2('Vehicle Downtimes'),
                        style={'text-align': 'center'}
                        ),
                    html.Div([
                        #Graph Towntimes
                        dcc.Graph(figure=pie1, style={'width': '59%', 'margin': '0'}),

                       # dcc.Graph(figure=pie1, style={'width': '40%', 'margin': '0'}),
                    ]),
                ],style={'width': '49%', 'display': 'inline-block', 'margin': '0'}),


#Accidents
            html.Div([
                html.Div([
                    html.Div(
                        html.H2('Accidents'),
                        style={'text-align': 'center'}
                        ),
                    html.Div(
                        dcc.Graph(figure=fig),
                        ),
                ]),

            ],style={'width': '49%', 'display': 'inline-block', 'margin': '0'}),
        ]),


#Row 2

            #Need for Maintenance View
            html.Div([
                html.Div(
                    html.H2('Need for Maintanance'),
                    style={'text-align': 'center'}
                ),
                html.Div([
                    #Graph - Need for Maintanance
                    dcc.Graph(figure=pie1, style={'width': '59%', 'margin': '0'}),

                    #Table - Need for maintenance

                ]),
            ], style={'width': '49%', 'display': 'inline-block'}),

            #Accident probability view
            html.Div([
                html.Div(
                    html.H2('Accident probability'),
                    style={'text-align': 'center'}
                ),
                html.Div([
                    # Graph - Accident probability
                    dcc.Graph(figure=pie1, style={'width': '59%', 'margin': '0'}),

                    # Table - Accident probability

                ]),
            ], style={'width': '49%', 'display': 'inline-block'}),

#Row 3 - Truck / Driver information

        #Overstepping speed limit table
        html.Div(
            dash_table.DataTable(
            data=fleet_data.to_dict('records'),
            #columns=[{'id': c, 'name': c} for c in fleet_data.columns],
            columns=[{'name': i, 'id': i} for i in fleet_data.loc[:,['vid','vehicle_class']]],
            style_cell={'textAlign': 'left'},
            style_cell_conditional=[

            ]),
            style={'width': '19%', 'display': 'inline-block'}),

        #Oldest Vehicles table
        html.Div(
            dash_table.DataTable(
            data=fleet_data.to_dict('records'),
            #columns=[{'id': c, 'name': c} for c in fleet_data.columns],
            columns=[{'name': i, 'id': i} for i in fleet_data.loc[:,['vid','vehicle_class']]],
            style_cell={'textAlign': 'left'},
            style_cell_conditional=[

            ]),
            style={'width': '19%', 'display': 'inline-block'}),

        #Excessive speeding table
        html.Div(
            dash_table.DataTable(
            data=fleet_data.to_dict('records'),
            #columns=[{'id': c, 'name': c} for c in fleet_data.columns],
            columns=[{'name': i, 'id': i} for i in fleet_data.loc[:,['vid','vehicle_class']]],
            style_cell={'textAlign': 'left'},
            style_cell_conditional=[

            ]),
            style={'width': '19%', 'display': 'inline-block'}),

        #Excessive acceleration table
        html.Div(
            dash_table.DataTable(
            data=fleet_data.to_dict('records'),
            #columns=[{'id': c, 'name': c} for c in fleet_data.columns],
            columns=[{'name': i, 'id': i} for i in fleet_data.loc[:,['vid','vehicle_class']]],
            style_cell={'textAlign': 'left'},
            style_cell_conditional=[

            ]),
            style={'width': '19%', 'display': 'inline-block'}),

        #Excessive breaking table
        html.Div(
            dash_table.DataTable(
            data=fleet_data.to_dict('records'),
            #columns=[{'id': c, 'name': c} for c in fleet_data.columns],
            columns=[{'name': i, 'id': i} for i in fleet_data.loc[:,['vid','vehicle_class']]],
            style_cell={'textAlign': 'left'},
            style_cell_conditional=[

            ]),
            style={'width': '19%', 'display': 'inline-block'}),


        ]),

# Maintenance Calendar View
        dcc.Tab(label='Maintenance Calendar', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                         'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),

        #Fleet location map view
        dcc.Tab(label='Realtime Map', children=[

            dcc.Graph(figure=fig),

        dash_table.DataTable(
        data=fleet_data.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in fleet_data.columns],
        style_cell={'textAlign': 'left'},
        style_cell_conditional=[
            {
                'if': {'column_id': 'Region'},
                'textAlign': 'left'
            }
        ])







        ]),
    ])
])
