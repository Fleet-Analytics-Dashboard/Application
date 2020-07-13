import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
import calendar
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc

from database_connection import connect, return_engine

# connect to database and add files to
conn = connect()
sql = "select * from vehicle_data;"
vehicle_data = pd.read_sql_query(sql, conn)
sql = "select * from cleaned_data_fleet_dna;"
fleet_data = pd.read_sql_query(sql, conn)
conn = None





# Daten
# fleet_data = pd.read_csv('cleaned-data-for-fleet-dna.csv')
# fleet_data = fleet_data.head(10)  # limits the displayed rows to 10
# fleet_data.iloc[:,1:3]


# Kalendar

# calenderview = open('calendar.html', 'wb')

# PieCharts

# Downtimes Overview graph
# dt = fleet_data[["maintenance"]]
# for i in dt

labels = ['Accidents', 'Traffic Jams', 'Maintenance', 'Unused']
# values = [20, 30, 10, 40]
values = vehicle_data.vehicle_status.value_counts()
# values = fleet_data[["vehicle_status"]].groupby('vehicle_status').count()


pie1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Need for Maintenance graph

labels = ['Need', 'Soon', 'No need']
values = [2, 5, 10]

pie2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Accident Probability graph

labels = ['Category 1', 'Category 2', 'Category 3']
values = [20, 30, 10, 40]

pie3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3,)])

#######################Mapbox###########################
# mapbox_access_token = open(".mapbox_token").read()

#######Vehicle  position data extraction###################
fleet_lat = vehicle_data.position_latitude
fleet_lon = vehicle_data.position_longitude
fleet_vid = vehicle_data.vid

fig = go.Figure(go.Scattermapbox(

    lat=fleet_lat,
    lon=fleet_lon,
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9
    ),
    text=fleet_vid,
))


fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
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
        zoom=10,
        style='mapbox://styles/jakobschaal/ckb1ekfv005681iqlj9tery0v',
    ),
)




layout = html.Div([

    ###### Tab-Layout ############

    dcc.Tabs([

        # Downtimes View

        dcc.Tab(label='Downtimes', children=[

            ################# Row 1 ###########################

            dbc.Row([

                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                html.H2('Vehicle Downtimes'),
                                style={'text-align': 'center'}
                            ),
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=pie1), className='piechart'),
                        dbc.Col([

##################Radiobuttons Downtimes###################

                            dcc.Checklist(
                                id='page-controlling-radios-2',
                                options=[{'label': i, 'value': i}
                                         for i in ['Unused', 'Traffic Jams', 'Accidents', 'Maintenance']],
                                value=['Unused', 'Traffic Jams', 'Accidents', 'Maintenance']),

##################Searchbox Downtimes###################

                            dcc.Dropdown(
                                id='searchbox_downtime_table',
                                options=[{'label': i, 'value': i} for i in sorted(vehicle_data['vid'])],
                                value='',
                                placeholder='Search for vehicle...'
                            ),

##################Table Downtimes#########################

                            dash_table.DataTable(
                                id="downtime_table",
                                style_table={
                                    'maxHeight': '',
                                    'maxWidth': '',
                                    'overflowY': ''
                                },
                                data=vehicle_data.to_dict('records'),
                                # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'vehicle_status']]],
                                page_size=10,
                                style_cell={'textAlign': 'left'},
                                style_cell_conditional=[

                                ]),

                        ]),
                    ]),
                ], className='container', width=True),

##################Map Accidents#########################

                dbc.Col(html.Div([
                    html.Div([
                        html.Div(
                            html.H2('Accidents'),
                            style={'text-align': 'center'}
                        ),
                        html.Div(
                            dcc.Graph(figure=fig, className='accidentsmap'),
                        ),
                    ]),

                ]), className='container', width=True),

            ]),

################# Row 2 ###########################

            dbc.Row([

                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                html.H2('Need for Maintenance'),
                                style={'text-align': 'center'}
                            ),
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=pie2)),
                        dbc.Col([

                            ##################Radio-Buttons Maintenance################

                            dcc.Checklist(
                                id='page-controlling-radios-2',
                                options=[{'label': i, 'value': i}
                                         for i in ['Need', 'Soon', 'No need']],
                                value=['Need', 'Soon', 'No need']),

                            ##################Searchbox Maintenance###################

                            dcc.Dropdown(
                                id='filter_x',
                                options=[{'label': i, 'value': i} for i in sorted(vehicle_data['vid'])],
                                value='',
                                placeholder='Search for vehicle...'
                            ),

                            dash_table.DataTable(
                                data=vehicle_data.to_dict('records'),
                                # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'maintenance']]],
                                page_size=10,
                                style_cell={'textAlign': 'left'},
                                style_cell_conditional=[

                                ]),
                        ]),
                    ]),
                ], className='container', width=True),

                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                html.H2('Accident Probability'),
                                style={'text-align': 'center'}
                            ),
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=pie3)),
                        dbc.Col([
                            ##################Searchbox Accidents###################

                            dcc.Checklist(
                                id='page-controlling-radios-2',
                                options=[{'label': i, 'value': i}
                                         for i in ['Category 1', 'Category 2', 'Category 3']],
                                value=['Category 1', 'Category 2', 'Category 3']),

                            ##################Searchbox Accidents###################

                            dcc.Dropdown(
                                id='filter_x',
                                options=[{'label': i, 'value': i} for i in sorted(vehicle_data['vid'])],
                                value='',
                                placeholder='Search for vehicle...'
                            ),

                            dash_table.DataTable(
                                data=vehicle_data.to_dict('records'),
                                # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'maintenance']]],
                                page_size=10,
                                style_cell={'textAlign': 'left'},
                                style_cell_conditional=[
                                ]),
                        ]),
                    ]),
                ], className='container', width=True),

            ]),

            ############# Row 3 #############

            dbc.Row([

                # Overstepping speed limit table

                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                html.H2('Overstepping Speed Limit'),
                                style={'text-align': 'center'}
                            ),
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dash_table.DataTable(
                            data=vehicle_data.to_dict('records'),
                            # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                            columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'maintenance']]],
                            page_size=5,
                            style_cell={'textAlign': 'left'},
                            style_cell_conditional=[

                            ]), ),
                    ]),
                ], className='container', width=True),

                # Oldest Vehicles table

                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                html.H2('Oldest Vehicles'),
                                style={'text-align': 'center'}
                            ),
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dash_table.DataTable(
                            data=vehicle_data.to_dict('records'),
                            # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                            columns=[{'name': i, 'id': i} for i in
                                     vehicle_data.loc[:, ['vid', 'vehicle_construction_year']]],
                            page_size=5,
                            style_cell={'textAlign': 'left'},
                            style_cell_conditional=[

                            ]), ),
                    ]),
                ], className='container', width=True),

                # Excessive speeding table

                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                html.H2('Excessive Speeding'),
                                style={'text-align': 'center'}
                            ),
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dash_table.DataTable(
                            data=vehicle_data.to_dict('records'),
                            # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                            columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'maintenance']]],
                            page_size=5,
                            style_cell={'textAlign': 'left'},
                            style_cell_conditional=[

                            ]), ),
                    ]),
                ], className='container', width=True),

                # Excessive acceleration table

                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                html.H2('Excessive Acceleration'),
                                style={'text-align': 'center'}
                            ),
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dash_table.DataTable(
                            data=vehicle_data.to_dict('records'),
                            # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                            columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'maintenance']]],
                            page_size=5,
                            style_cell={'textAlign': 'left'},
                            style_cell_conditional=[

                            ]), ),
                    ]),
                ], className='container', width=True),

                # Excessive breaking table

                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                html.H2('Excessive Breaking'),
                                style={'text-align': 'center'}
                            ),
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dash_table.DataTable(
                            data=vehicle_data.to_dict('records'),
                            # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                            columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'maintenance']]],
                            page_size=5,
                            style_cell={'textAlign': 'left'},
                            style_cell_conditional=[

                            ]), ),
                    ]),
                ], className='container', width=True),
            ]),

        ]),

        ################### Maintenance Calendar View ##################
        dcc.Tab(label='Maintenance Calendar', children=[
            # dcc.Graph(figure=calenderview),
            html.Div([
                html.Embed(src='assets/calendar.html', className="calContainer")
            ], className="")

        ]),

        # Fleet location map view
        dcc.Tab(label='Realtime Map', children=[

            dcc.Graph(figure=fig),

            dash_table.DataTable(
                data=vehicle_data.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
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
