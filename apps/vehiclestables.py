import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
from database_connection import connect, return_engine

# Datasets
# fleet_data = pd.read_csv('cleaned-data-for-fleet-dna_v3.csv')

# Connect to database and add files to
conn = connect()
sql = "select * from cleaned_data_fleet_dna;"
fleet_data = pd.read_sql_query(sql, conn)
conn = None

dfnames = pd.read_csv('names.csv')

# Rounded data
fleet_data_rounded = fleet_data.round(decimals=2)

df_vehicle = fleet_data[
    ['vid', 'vehicle_class', 'vocation', 'vehicel_type', 'fuel_type', 'drivetrain_type', 'pid']].copy()

df_vehicle_class = fleet_data[['vehicle_class', 'vid', 'fuel_type', 'vocation', 'vehicel_type']].copy()
df_vehicle_class = df_vehicle.drop_duplicates(subset=None, keep='first', inplace=False)
df_group_vehicle_class = df_vehicle_class.groupby(['vehicle_class', 'vocation', 'vehicel_type'])[
    'vid'].count().reset_index()
df_group_vehicle_class.columns = (["Vehicle Typ", 'Transport Goal', 'Typ', "Amount"])

df_driver = pd.merge(df_vehicle, dfnames, how='left', on='pid').copy()
df_driver = df_driver.drop(columns=['ip_address'])
df_group_driver = df_driver.groupby(['vid', 'last_name'])['pid'].count().reset_index()
df_group_driver.columns = (['License Plate', 'Name', 'Amount'])

# Layout

layout = html.Div(
    className='vehiclestables-content',
    children=[
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
                html.Div(id='year-table')
            ])
    ])
