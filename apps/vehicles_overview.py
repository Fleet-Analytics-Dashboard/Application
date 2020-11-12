import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
import plotly.graph_objects as go
import plotly.express as px

# from database_connection import connect

# get data from database
# conn = connect()
# sql = "select * from vehicle_data;"
# df_vehicle_data = pd.read_sql_query(sql, conn)
# sql = "select * from driving_data;"
# fleet_data = pd.read_sql_query(sql, conn)
# sql = "select * from driver_names;"
# dfnames = pd.read_sql_query(sql, conn)
# conn = None

# get data from csv files
df_vehicle_data = pd.read_csv('csv_data_files/vehicle_data.csv')
fleet_data = pd.read_csv('csv_data_files/driving_data.csv')
dfnames = pd.read_csv('csv_data_files/names.csv')

# Rounded data
fleet_data_rounded = fleet_data.round(decimals=2)

df_vehicle = df_vehicle_data[['vid','licence_plate', 'vehicle_class',   'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type']].copy()
df_vehicle = pd.merge(df_vehicle, fleet_data, how='left', on='vid')
df_vehicle = df_vehicle[['vid', 'vehicle_class', 'licence_plate', 'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type', 'pid']]

df_vehicle_class = df_vehicle_data[['vehicle_class', 'vid', 'fuel_type', 'vocation', 'vehicle_type']].copy()
df_vehicle_class = df_vehicle_class.drop_duplicates(subset=None, keep='first', inplace=False)

df_group_vehicle_class = df_vehicle_class.groupby(['vehicle_class', 'vocation', 'vehicle_type'])['vid'].count().reset_index()
df_group_vehicle_class.columns = (["Vehicle Class", 'Transport Goal', 'Typ', "Amount"])

df_driver = pd.merge(df_vehicle, dfnames, how='left', on='pid').copy()
df_driver = df_driver.drop(columns=['ip_address'])
df_driver = df_driver.drop_duplicates(subset=None, keep='first', inplace=False)


df_group_driver = df_driver.groupby(['licence_plate', 'last_name'])['pid'].count().reset_index()
df_group_driver.columns = (['License Plate', 'Name', 'Amount'])

df_map_data = df_vehicle_data.copy()



####Mapbox####


fleet_lat = df_vehicle_data.position_latitude
fleet_lon = df_vehicle_data.position_longitude
fleet_vid = df_vehicle_data.vid
fleet_status = df_vehicle_data.vehicle_status

fig = go.Figure(
    px.scatter_mapbox(df_vehicle_data, text="licence_plate", lat=fleet_lat, lon=fleet_lon, color="vehicle_status",
                      color_continuous_scale=px.colors.cyclical.IceFire,
                      size_max=20, zoom=10, height=650))

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    autosize=True,
    clickmode='event+select',
    legend=dict(
        x=0,
        y=1,
        font=dict(
            family="Courier",
            size=12,
            color="black"
        ),
        bgcolor="LightSteelBlue",
        bordercolor="Black",
        borderwidth=2
    ),
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
        style='mapbox://styles/jakobschaal/ckcv9t67c097q1imzfqprsks9',
    ),
)

layout = html.Div(
    className='home-content card',
    children=[


        dcc.Tabs([

            #########Realtime Map############
            dcc.Tab(label='Realtime Map', children=[

                html.Div(

                    children=[
                        dcc.Dropdown(
                            id='map-filter',
                            options=[{'label': i, 'value': i} for i in sorted(df_vehicle_data['licence_plate'])],
                            value='',
                            placeholder='Search for vehicle...'
                        ),
                        dcc.Graph(figure=fig, id='mapbox-overview', className='realtime-map'),

                    ],
                    id='map-container',
                    className="home-welcome-text"),


            ]),

            ############Vehicles###############
            dcc.Tab(label='Vehicles', children=[

                html.Div(
                    className='card',
                    children=[
                        html.H1('Select One Option'),
                        dcc.RadioItems(
                            id='graph-filter',
                            options=[
                                {'label': ' Transport Goals   ', 'value': 'Voc'},
                                {'label': ' Vehicles   ', 'value': 'vic_type'},
                                {'label': ' Drivers   ', 'value': 'person'}
                            ],
                            value='Voc',
                        ),
                        dcc.Graph(
                            id='graph'
                        ),
                    ]),
                html.Div(
                    className='card',
                    children=[
                        html.H1('Table'),
                        html.Div(
                            'In the following bar, a certain vehicle, driver, or other information can be searched.'
                            'Further, one of the following transport goals can be exclude.'
                            'Lastly, the table can be resetted via the reset button'),

                        html.Div([
                            dcc.Dropdown(
                                id='vocation-dropdown-table',
                                options=[{'label': i, 'value': i} for i in
                                         sorted(df_driver['vocation'].unique())],
                                value=df_driver['vocation'].unique(),
                                multi=True,
                            ),
                        ], className='table-menu'),

                        dt.DataTable(
                            id='vehicle-table2',
                            data=[{}],
                            columns=[{'id': c, 'name': c, "deletable": True, "selectable": True, "hideable": "last"} for c in
                                     df_driver.columns],

                            filter_action="native",
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            page_action="native",
                            page_current=0,
                            page_size=40,
                            style_as_list_view=True,
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
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Date', 'Region']
                            ],
                            export_format='xlsx',
                            export_headers='display',
                        ),
                    ])

            ]),
        ]),

    ])
