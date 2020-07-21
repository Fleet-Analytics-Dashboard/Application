import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from database_connection import connect
import dash_table as dt
from apps.downtimes import df_vehicle_data
import plotly.graph_objects as go
from apps.downtimes import fleet_data
from apps.vehiclestables import df_driver, df_vehicle_class
import plotly.express as px

# conn = connect()
# sql = "select * from vehicle_data;"
# df_vehicle_data = pd.read_sql_query(sql, conn)
# sql = "select * from cleaned_data_fleet_dna;"
# fleet_data = pd.read_sql_query(sql, conn)
# conn = None

df_map_data = df_vehicle_data.copy()

# Data from csv
fleet_data = pd.read_csv('driving_data.csv')
df_vehicle_data = pd.read_csv('vehicle_data.csv')
# fleet_data = fleet_data.head(10)  # limits the displayed rows to 10
# fleet_data.iloc[:,1:3]


####Mapbox####


fleet_lat = df_vehicle_data.position_latitude
fleet_lon = df_vehicle_data.position_longitude
fleet_vid = df_vehicle_data.vid
fleet_status = df_vehicle_data.vehicle_status

fig = go.Figure(
    px.scatter_mapbox(df_vehicle_data, text="licence_plate", lat=fleet_lat, lon=fleet_lon, color="vehicle_status",
                      custom_data=['licence_plate'], color_continuous_scale=px.colors.cyclical.IceFire,
                      size_max=20, zoom=10))

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
        #style='mapbox://styles/jakobschaal/ckb1ekfv005681iqlj9tery0v',
        style='mapbox://styles/jakobschaal/ckcv9t67c097q1imzfqprsks9',
    ),
)

layout = html.Div(
    className='home-content card',
    children=[
        # html.H1(children='Home'),

        dcc.Tabs([

        #########Realtime Map############
            dcc.Tab(label='Realtime Map', children=[

                html.Div(
                    children='',
                    className="home-welcome-text"),

                dcc.Graph(figure=fig, id='mapbox-overview'),


                html.Div(dt.DataTable(
                    id='vehicle-table-overview',
                    data=[{}],
                    columns=[{'id': c, 'name': c, "deletable": True, "selectable": True} for c in
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
                ),

                )

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
                html.Div('In the following bar, a certain vehicle, driver, or other information can be searched.'
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
                    html.A('Reset table (Refresh)', className='button', href='/vehicles-tables'),
                ], className='table-menu'),

                dt.DataTable(
                    id='vehicle-table2',
                    data=[{}],
                    columns=[{'id': c, 'name': c, "deletable": True, "selectable": True} for c in
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
                ),
            ])



            ]),
        ]),

    ])
