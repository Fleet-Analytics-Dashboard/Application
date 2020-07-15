import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from database_connection import connect
import dash_table
from apps.downtimes import df_vehicle_data
import plotly.graph_objects as go

# connect to database and add files to
# conn = connect()
# sql = "select * from cleaned_data_fleet_dna;"
# df = pd.read_sql_query(sql, conn)
# df = df.head(10)
# conn = None

# Daten
fleet_data = pd.read_csv('cleaned-data-for-fleet-dna.csv')
fleet_data = fleet_data.head(10)  # limits the displayed rows to 10
# fleet_data.iloc[:,1:3]


####Mapbox####


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
            lon=-77.07
        ),
        pitch=0,
        zoom=10,
        style='mapbox://styles/jakobschaal/ckb1ekfv005681iqlj9tery0v',
    ),
)


layout = html.Div(
    className='home-content card',
    children=[
        html.H1(children='Home'),

        html.Div(
            children='',
            className="home-welcome-text"),

        dcc.Graph(figure=fig),

        html.Div(dash_table.DataTable(
            id='table-2',
            data=fleet_data.to_dict('records'),
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
            columns=[{'name': i, 'id': i} for i in fleet_data.loc[:]
                     ],
        ), )
    ])
