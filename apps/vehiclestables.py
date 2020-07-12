import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
from database_connection import connect, return_engine


# Datasets
#fleet_data = pd.read_csv('cleaned-data-for-fleet-dna_v3.csv')

# connect to database and add files to
conn = connect()
sql = "select * from cleaned_data_fleet_dna;"
fleet_data = pd.read_sql_query(sql, conn)
conn = None

dfnames = pd.read_csv('names.csv')

# rounded data
fleet_data_rounded = fleet_data.round(decimals=2)

df_vehicle = fleet_data[['vid', 'vehicle_class', 'vocation', 'vehicel_type', 'fuel_type', 'drivetrain_type', 'pid']].copy()
df_vehicle = df_vehicle.drop_duplicates(subset=None, keep='first', inplace=False)

df_vehicle_class = fleet_data[['vehicle_class', 'vid', 'fuel_type', 'vocation', 'vehicel_type']].copy()
df_vehicle_class = df_vehicle.drop_duplicates(subset=None, keep='first', inplace=False)


df_group_vehicle_class = df_vehicle_class.groupby(['vehicle_class','vocation'])['vid'].count().reset_index()
df_group_vehicle_class.columns = (["Klasse", 'Typ',"anzahl"])




df_driver = pd.merge(df_vehicle, dfnames, how='left', on='pid').copy()

df_driver = df_driver.rename(columns={"pid": "pp"}).copy()


# Layout
layout = html.Div([

    # dict(
    #   autosize=True,
    #  height=450,
    # font=dict(color="#191A1A"),
    # titlefont=dict(color="#191A1A", size='14'),
    # margin=dict(
    #   l=45,
    #  r=15,
    # b=45,
    # t=35
    # )
    # ),
    # Title - Row
    html.Div(
        [
            html.H1(
                'Test App',
                className='example',
            )
        ],
        className='example'
    ),

    # block 2
    html.Div([
        dcc.Store(id='memory'),
        html.H3('Vehicle Overview'),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="graph",
                ),
                html.Div(
                    [
                        html.P('Insert the vehicle number here:'),
                        dcc.Dropdown(
                            id='filter_x',
                            options=[{'label': i, 'value': i} for i in sorted(df_vehicle['vid'])],

                            value=''
                        ),
                    ],
                    className='three-columns'
                ),
                html.Div(
                    [
                        html.P('Insert the vehicle number here:'),
                        dcc.Dropdown(
                            id='filter_y',
                            options=[{'label': i, 'value': i} for i in sorted(df_vehicle['vocation'])],

                            value=''
                        ),
                    ],
                    className='three-columns'
                ),
                html.Div(
                    [
                        html.P('Type:'),
                        dcc.Dropdown(
                            id='type',
                            options=[{'label': str(item),
                                      'value': str(item)}
                                     for item in set(fleet_data['vehicle_class'])],
                            multi=True,
                            value=list(set(fleet_data['vehicle_class']))
                        )
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.Button('Back',
                                    id='back_button',
                                    className='vehicles-tables-button-previous-level')
                    ],
                )
            ],
            className='example'
        ),

        html.Div(
            [
                html.Div(id='table-box'),
                html.Div(dt.DataTable(
                id='table',
                data=[{}],
                ),
                ),
            ], className='vehicles-tables-data-table'
        ),
    ], className='chart')
], className='vehicles-tables-content')

])