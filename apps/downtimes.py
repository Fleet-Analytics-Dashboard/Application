import dash_table
##todo are imports unused or there on purpose?
import dash_bootstrap_components as dbc
import datetime
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from dateutil.relativedelta import relativedelta


from database_connection import connect, return_engine

# connect to database and add files to
conn = connect()
sql = "select * from vehicle_data;"
df_vehicle_data = pd.read_sql_query(sql, conn)
sql = "select * from cleaned_data_fleet_dna;"
fleet_data = pd.read_sql_query(sql, conn)
conn = None

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
fleet_vid = df_vehicle_accidents.vid

mapbox_accidents = go.Figure(go.Scattermapbox(

    lat=fleet_lat,
    lon=fleet_lon,
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9
    ),
    text=fleet_vid,
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
        style='mapbox://styles/jakobschaal/ckb1ekfv005681iqlj9tery0v',
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
def maintenance_calendar():
    today = datetime.date.today()
    year, week_num, day_of_week = today.isocalendar()
    # d1 represents starting day (yyyy-mm-dd) and d2 end day
    #d1 = today - datetime.date.month

    d1 = today + relativedelta(weeks=-26)

    d2 = today + relativedelta(weeks=+26)

    delta = d2 - d1


    dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days+1)] # gives me a list with datetimes for each day a year
    # weekdays_in_year = [i.weekday() for i in dates_in_year] #gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
    weeknumber_of_dates = [i.strftime("%Gcw%V")[2:] for i in
                           dates_in_year]  # gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
    weeknumber_of_dates = list(dict.fromkeys(weeknumber_of_dates))
    # create numpy array for the maintenance dates for each vehicle
    z = np.zeros(shape=(len(df_vehicle_data['vid']), len(weeknumber_of_dates)), dtype=float)

    # set status of vehicles which are currently in maintenance to 1
    today_maintenance = df_vehicle_data.index[df_vehicle_data['vehicle_status'] == 'maintenance'].tolist()
    for i in today_maintenance:
        z[i][26] = 1

    # set status for scheduled maintenance
    for index, row in df_vehicle_data.iterrows():
        z[index][26 + int(row['scheduled_maintenance'])] = 1

    # set status for previous maintenance
    np.random.seed(1)
    random_date = np.random.randint(0, 23, size=len(df_vehicle_data.vid) )
    index = 0
    for i in random_date:
        z[index][i] = 1
        index += 1

    # set status for scheduled maintenance
    for index, row in df_vehicle_data.iterrows():
        if row.predicted_weeks_until_maintenance < 30:
            z[index][26 + int(row['predicted_weeks_until_maintenance'])] = 0.5

    #text = [str(i) for i in dates_in_year] #gives something like list of strings like ‘2018-01-25’ for each date. Used in data trace to make good hovertext.
    #4cc417 green #347c17 dark green
    colorscale = [[0, '#eeeeee'], [0.5, 'red'], [1, 'rgb(7, 130, 130)']]
    data = [
    go.Heatmap(
    x = weeknumber_of_dates,
    y = df_vehicle_data['licence_plate'],
    z = z,
   # text=text,
   # hoverinfo='text',
    xgap=3, # this
    ygap=3, # and this is used to make the grid-like apperance
    showscale=False,
    colorscale=colorscale
    )]


    layout = go.Layout(
    height=4000,
    yaxis=dict(
    showline = False, showgrid = False, zeroline = False,
   # tickmode='array',
    ticktext=df_vehicle_data['licence_plate'],
   # tickvals=[0,1,2,3,4,5,6],
    ),
    xaxis=dict(
    showline = False, showgrid = False, zeroline = False, side = 'top',
    ),
   #font={'size':'10', 'color':'#9e9e9e'},
    plot_bgcolor=('#fff'),
    margin = dict(t=40),
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


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
                                         df_vehicle_data.loc[:, ['licence_plate', 'vehicle_construction_year']]],
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
                    dcc.Graph(id='heatmap-test', figure=maintenance_calendar(), config={'displayModeBar': False})
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
