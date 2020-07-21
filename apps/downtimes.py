import dash_table
##todo are imports unused or there on purpose?
##todo switch from csv to database
import dash_bootstrap_components as dbc
import datetime
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import statistics
from plotly.subplots import make_subplots
from dateutil.relativedelta import relativedelta


# from database_connection import connect, return_engine

# connect to database and add files to
# conn = connect()
# sql = "select * from vehicle_data;"
# df_vehicle_data = pd.read_sql_query(sql, conn)
# sql = "select * from cleaned_data_fleet_dna;"
# fleet_data = pd.read_sql_query(sql, conn)
# conn = None

# get data from csv files
df_vehicle_data = pd.read_csv('vehicle_data.csv')
fleet_data = pd.read_csv('driving_data.csv')

# colors theme
colors = ['rgb(66,234,221)', 'rgb(7,130,130)', 'rgb(171,209,201)', 'rgb(151,179,208)', 'rgb(118,82,139)', 'rgb(173,239,209)', 'rgb(96,96,96)', 'rgb(214,65,97)']

df_vehicle_data = df_vehicle_data.round(decimals=2)

######## Convert maintenance score to maintenance status############

df_maintenance_status = df_vehicle_data.copy()
conditions = [
    (df_vehicle_data['scheduled_maintenance'] >= 8),
    (df_vehicle_data['scheduled_maintenance'] < 8) & (df_vehicle_data['scheduled_maintenance'] > 1),
    (df_vehicle_data['scheduled_maintenance'] <= 1)]
choices = ['No need', 'Soon', 'Need']

df_maintenance_status['scheduled_maintenance'] = np.select(conditions, choices, default='null')



#fig_carbon = go.Figure()

# for i in range(0, 1):
#    fig_carbon.add_trace(go.Scatter(
#        x=x_data_carbon[i],
#        y=y_data_carbon_footprint[i], mode='lines+markers',
#        name='Carbon Footprint',
#        line=dict(color=colors[i], width=line_size[i]),
#        connectgaps=True,
#    ))

# PieCharts

############### Downtimes Overview graph################

###New dataframe for filter result####
df_vehicle_status = df_vehicle_data.copy()

###Array with accepted values###
accepted_vehicle_status_array = ['accident', 'unused', 'maintenance', 'traffic jam']

###filter####
df_vehicle_status = df_vehicle_status.loc[df_vehicle_data['vehicle_status'].isin(accepted_vehicle_status_array)]

####use unique values as labels###
labels = df_vehicle_status['vehicle_status'].unique()

####count values###
values = df_vehicle_status.vehicle_status.value_counts()

#index = df_vehicle_status.vid
text = len(df_vehicle_status)

pie1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
pie1.update_traces(marker=dict(colors=colors))
pie1.update_layout(
    annotations=[dict(text=text, font_size=20, showarrow=False)]
)

############################## Need for Maintenance graph###################################

####use unique values as labels###
labels = df_maintenance_status['scheduled_maintenance'].unique()

####count values###
values = df_maintenance_status.scheduled_maintenance.value_counts()

pie2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
pie2.update_traces(marker=dict(colors=colors))




##################### Accident Probability graph#####################################

labels = ['Category 1', 'Category 2', 'Category 3']
values = [20, 30, 10, 40]

pie3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, )])
pie3.update_traces(marker=dict(colors=colors))

####################### Mapbox ###########################
# mapbox_access_token = open(".mapbox_token").read()


#########Mapbox Accidents##############


###Data filter####

df_vehicle_accidents = df_vehicle_data.copy()

###Array with accepted values###
only_accidents_array = ['accident']

df_vehicle_accidents = df_vehicle_accidents.loc[df_vehicle_accidents['vehicle_status'].isin(only_accidents_array)]

fleet_lat = df_vehicle_accidents.position_latitude
fleet_lon = df_vehicle_accidents.position_longitude
fleet_text = df_vehicle_accidents.licence_plate

mapbox_accidents = go.Figure(go.Scattermapbox(
    text=fleet_text,
    lat=fleet_lat,
    lon=fleet_lon,
    mode='markers',
    #hoverinfo='all',
    marker=go.scattermapbox.Marker(
        size=12,
        symbol='fire-station',
        color='rgb(242, 177, 172)'
    ),

))

mapbox_accidents.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken='pk.eyJ1IjoiamFrb2JzY2hhYWwiLCJhIjoiY2tiMWVqYnYwMDEyNDJ5bWF3YWhnMTFnNCJ9.KitYnq2a645C15FwvFdqAw',
        bearing=0,
        center=dict(
            lat=40.92,
            lon=-91.07
        ),
        pitch=0,
        zoom=3,
        #style='mapbox://styles/jakobschaal/ckb1ekfv005681iqlj9tery0v',
        style='mapbox://styles/jakobschaal/ckcv9t67c097q1imzfqprsks9',
    ),
)

######Mapbox total########
####### Vehicle  position data extraction ###################
fleet_lat = df_vehicle_data.position_latitude
fleet_lon = df_vehicle_data.position_longitude
fleet_vid = df_vehicle_data.vid

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
            lon=-100.07
        ),
        pitch=0,
        zoom=5,
        style='mapbox://styles/jakobschaal/ckb1ekfv005681iqlj9tery0v',
    ),
)

######Maintenance Calendar########
######## sorting dataframe for maintenace calendar############

df_vehicle_data = df_vehicle_data.sort_values(by='licence_plate', ascending=False)

#####oldest vehicle table#####
oldest_vehicle_data = df_vehicle_data.sort_values(by='vehicle_construction_year', ascending=False)


# Create figure with secondary y-axis
oldest_vehicle = make_subplots(specs=[[{"secondary_y": True}]])

x = statistics.mean(df_vehicle_data['vehicle_construction_year'])
df_vehicle_data['mean'] = x


# Add traces
oldest_vehicle.add_trace(
    go.Bar(x=oldest_vehicle_data['licence_plate'], y=oldest_vehicle_data['vehicle_construction_year'], name="yaxis data"),
    secondary_y=False,
)

oldest_vehicle.add_trace(
    go.Scatter(x=oldest_vehicle_data['licence_plate'], y=df_vehicle_data['mean'], name="yaxis2 data"),
    secondary_y=True,
)

# Add figure title
oldest_vehicle.update_layout(
    title_text="Oldest Vehicle"
)


# Set x-axis title
oldest_vehicle.update_xaxes(title_text="Licence Plate")

# Set y-axes titles
oldest_vehicle.update_yaxes(title_text="Year", secondary_y=False)
oldest_vehicle['layout']['yaxis'].update(range=[1999, 2020], dtick=5, autorange=False)
oldest_vehicle['layout']['yaxis2'].update(range=[1999, 2020], dtick=5, autorange=False)


#### view layout #####

layout = html.Div(
    className='downtimes-content',
    children=[

        ###### Tab-Layout ############

        dcc.Tabs([

            # Downtimes Home

            dcc.Tab(label='Downtimes', children=[

                ################# Row 1 ###########################

                dbc.Row([

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H1('Vehicle Downtimes'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=pie1, config={'responsive': True}), className='piechart'),
                            dbc.Col([

                                ##################Radiobuttons Downtimes###################

                                dcc.Checklist(
                                    id='page-downtimes-radios-1',
                                    options=[{'label': i, 'value': i}
                                             for i in ['unused', 'accident', 'maintenance']],
                                    value=['unused', 'accident', 'maintenance']),

                                ##################Searchbox Downtimes###################

                                # dcc.Dropdown(
                                #     id='searchbox_downtime_table',
                                #     options=[{'label': i, 'value': i} for i in sorted(vehicle_data['vid'])],
                                #     value='',
                                #     placeholder='Search for vehicle...'
                                # ),

                                ##################Table Downtimes#########################

                                dash_table.DataTable(
                                    id="downtime_table",
                                    filter_action='native',
                                    sort_action='native',
                                    style_table={
                                        'maxHeight': '',
                                        'maxWidth': '',
                                        'overflowY': ''
                                    },
                                    data=[{}],

                                    columns=[{'name': i, 'id': i} for i in
                                             df_vehicle_data.loc[:, ['licence_plate', 'vehicle_status']]],
                                    page_size=10,
                                    style_header={
                                        'backgroundColor': '#f1f1f1',
                                        'fontWeight': 'bold',
                                        'fontSize': 12,
                                        'fontFamily': 'Open Sans'
                                    },
                                    style_cell={
                                        'padding': '5px',
                                        'fontSize': 13,
                                        'fontFamily': 'sans-serif'
                                    },
                                    style_cell_conditional=[

                                    ]),
                            ]),
                        ]),
                    ], className='card-tab card', width=True),

                    ##################Map Accidents#########################

                    dbc.Col(html.Div([
                        html.Div([
                            html.Div(
                                html.H1('Accidents'), className='map-margin'
                            ),
                            html.Div(
                                dcc.Graph(figure=mapbox_accidents, config={'responsive': True},
                                          className='accidentsmap'),
                            ),
                        ]),

                    ]), className='card-tab card', width=True),

                ]),

                ################# Row 2 ###########################

                dbc.Row([

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H1('Need for Maintenance'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=pie2)),
                            dbc.Col([

                                ################## Radio-Buttons Maintenance ################

                                dcc.Checklist(
                                    id='page-downtimes-radios-2',
                                    options=[{'label': i, 'value': i}
                                             for i in ['Need', 'Soon', 'No need']],
                                    value=['Need', 'Soon', 'No need']),

                                ################## Searchbox Maintenance ###################

                                # dcc.Dropdown(
                                #     id='maintenance_filter_x',
                                #     options=[{'label': i, 'value': i} for i in sorted(vehicle_data['vid'])],
                                #     value='',
                                #     placeholder='Search for vehicle...'
                                # ),

                                dash_table.DataTable(
                                    id='maintenance_table',
                                    data=[{}],
                                    filter_action='native',
                                    sort_action='native',
                                    columns=[{'name': i, 'id': i} for i in
                                             df_maintenance_status.loc[:, ['licence_plate', 'scheduled_maintenance']]],
                                    page_size=10,
                                    style_header={
                                        'backgroundColor': '#f1f1f1',
                                        'fontWeight': 'bold',
                                        'fontSize': 12,
                                        'fontFamily': 'Open Sans'
                                    },
                                    style_cell={
                                        'padding': '5px',
                                        'fontSize': 13,
                                        'fontFamily': 'sans-serif'
                                    },
                                    style_cell_conditional=[

                                    ]),
                            ]),
                        ]),
                    ], className='card-tab card', width=True),

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H1('Accident Probability'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=pie3)),
                            dbc.Col([
                                ################## Searchbox Accidents ###################

                                dcc.Checklist(
                                    id='page-downtimes-radios-3',
                                    options=[{'label': i, 'value': i}
                                             for i in ['Category 1', 'Category 2', 'Category 3']],
                                    value=['Category 1', 'Category 2', 'Category 3']),

                                ################## Searchbox Accidents ###################

                                # dcc.Dropdown(
                                #     id='accident_filter_x',
                                #     options=[{'label': i, 'value': i} for i in sorted(vehicle_data['vid'])],
                                #     value='',
                                #     placeholder='Search for vehicle...'
                                # ),

                                dash_table.DataTable(
                                    data=df_vehicle_data.to_dict('records'),
                                    filter_action='native',
                                    sort_action='native',
                                    # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                    columns=[{'name': i, 'id': i} for i in
                                             df_vehicle_data.loc[:, ['licence_plate', 'scheduled_maintenance']]],
                                    page_size=10,
                                    style_header={
                                        'backgroundColor': '#f1f1f1',
                                        'fontWeight': 'bold',
                                        'fontSize': 12,
                                        'fontFamily': 'Open Sans'
                                    },
                                    style_cell={
                                        'padding': '5px',
                                        'fontSize': 13,
                                        'fontFamily': 'sans-serif'
                                    },
                                    style_cell_conditional=[
                                    ]),
                            ]),
                        ]),
                    ], className='card-tab card', width=True),

                ]),

                ############# Row 3 #############

                dbc.Row([

                    # Overstepping speed limit table

                    # dbc.Col([
                    #     dbc.Row(
                    #         dbc.Col(
                    #             html.Div(
                    #                 html.H3('Overstepping Speed Limit'),
                    #                 style={'textAlign': 'center'}
                    #             ),
                    #         ),
                    #     ),
                    #     dbc.Row([
                    #         dbc.Col(dash_table.DataTable(
                    #             data=vehicle_data.to_dict('records'),
                    #             # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                    #             columns=[{'name': i, 'id': i} for i in vehicle_data.loc[:, ['vid', 'maintenance']]],
                    #             page_size=5,
                    #             style_cell={'textAlign': 'left'},
                    #             style_cell_conditional=[
                    #
                    #             ]), ),
                    #     ]),
                    # ], className='card', width=True),

                    # Oldest Vehicles table

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H3('Oldest Vehicles'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dash_table.DataTable(
                                data=df_vehicle_data.to_dict('records'),
                                filter_action='native',
                                sort_action='native',
                                # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                                columns=[{'name': i, 'id': i} for i in
                                         oldest_vehicle_data.loc[:, ['licence_plate', 'vehicle_construction_year']]],
                                page_size=5,
                                style_header={
                                    'backgroundColor': '#f1f1f1',
                                    'fontWeight': 'bold',
                                    'fontSize': 12,
                                    'fontFamily': 'Open Sans'
                                },
                                style_cell={
                                    'padding': '5px',
                                    'fontSize': 13,
                                    'fontFamily': 'sans-serif'
                                },
                                style_cell_conditional=[

                                ]), ),
                        ]),
                        dbc.Col([
                         dbc.Row(
                            dcc.Graph(id='graph-carbon-footprint', figure=oldest_vehicle)
                         )
                    ], className='card-tab card', width=True),

                    # Excessive speeding table

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H3('Longest Distance'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dash_table.DataTable(
                                data=df_vehicle_data.to_dict('records'),
                                filter_action='native',
                                sort_action='native',
                                # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                columns=[{'name': i, 'id': i} for i in
                                         df_vehicle_data.loc[:, ['licence_plate', 'scheduled_maintenance']]],
                                page_size=5,
                                style_header={
                                    'backgroundColor': '#f1f1f1',
                                    'fontWeight': 'bold',
                                    'fontSize': 12,
                                    'fontFamily': 'Open Sans'
                                },
                                style_cell={
                                    'padding': '5px',
                                    'fontSize': 13,
                                    'fontFamily': 'sans-serif'
                                },
                                style_cell_conditional=[

                                ]), ),
                        ]),
                    ], className='card-tab card', width=True),

                    # Excessive acceleration table

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H3('Excessive Acceleration'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dash_table.DataTable(
                                data=df_vehicle_data.to_dict('records'),
                                filter_action='native',
                                sort_action='native',
                                # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                columns=[{'name': i, 'id': i} for i in
                                         df_vehicle_data.loc[:, ['licence_plate', 'scheduled_maintenance']]],
                                page_size=5,
                                style_header={
                                    'backgroundColor': '#f1f1f1',
                                    'fontWeight': 'bold',
                                    'fontSize': 12,
                                    'fontFamily': 'Open Sans'
                                },
                                style_cell={
                                    'padding': '5px',
                                    'fontSize': 13,
                                    'fontFamily': 'sans-serif'
                                },
                                style_cell_conditional=[

                                ]), ),
                        ]),
                    ], className='card-tab card', width=True),

                    # Excessive breaking table

                    dbc.Col([
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    html.H3('Excessive Breaking'),
                                ),
                            ),
                        ),
                        dbc.Row([
                            dbc.Col(dash_table.DataTable(
                                data=df_vehicle_data.to_dict('records'),
                                filter_action='native',
                                sort_action='native',
                                # columns=[{'id': c, 'name': c} for c in vehicle_data.columns],
                                columns=[{'name': i, 'id': i} for i in
                                         df_vehicle_data.loc[:, ['vid', 'scheduled_maintenance']]],
                                page_size=5,
                                style_header={
                                    'backgroundColor': '#f1f1f1',
                                    'fontWeight': 'bold',
                                    'fontSize': 12,
                                    'fontFamily': 'Open Sans'
                                },
                                style_cell={
                                    'padding': '5px',
                                    'fontSize': 13,
                                    'fontFamily': 'sans-serif'
                                },
                                style_cell_conditional=[

                                ]), ),
                        ]),
                    ], className='card-tab card', width=True),
                ]),

            ]),

            # Maintenance Calendar
            dcc.Tab(label='Maintenance Calendar', children=[

                html.Div(children=[
                    dcc.Dropdown(id='heatmap-dropdown',
                                 options=[{'value': x, 'label': x} for x in df_vehicle_data['licence_plate']],
                                 #multi=True,
                                 #value='x',
                                 placeholder='Select license plate'),
                    dcc.Graph(id='heatmap',
                              #figure=maintenance_calendar(), config={'displayModeBar': False}
                    )
                ], style={'overflowX': 'scroll', 'height': 550}
                )

                ]),
            ]),

            # Fleet Location Map
            # dcc.Tab(label='Realtime Map', children=[
            #
            #     dcc.Graph(figure=fig),
            #
            #     html.H3('Vehicle Details'),
            #
            #     dash_table.DataTable(
            #         data=df_vehicle_data.to_dict('records'),
            #         columns=[{'id': c, 'name': c} for c in df_vehicle_data.columns],
            #         style_header={
            #             'backgroundColor': 'lightgrey',
            #             'fontWeight': 'bold',
            #             'fontSize': 12,
            #             'fontFamily': 'Open Sans'
            #         },
            #         style_cell={
            #             'padding': '5px',
            #             'fontSize': 13,
            #             'fontFamily': 'sans-serif'
            #         },
            #         style_cell_conditional=[
            #             {
            #                 'if': {'column_id': 'Region'},
            #                 'textAlign': 'left'
            #             }
            #         ])
            # ]),
        ])
])