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

df_vehicle_class = fleet_data[['vehicle_class', 'vid', 'fuel_type', 'vocation', 'vehicel_type']].copy()


df_group_vehicle_class = df_vehicle_class.groupby(['vehicle_class','vocation'])['vid'].count().reset_index()
df_group_vehicle_class.columns = (["Klasse", 'Typ',"anzahl"])


df_driver = pd.merge(df_vehicle, dfnames, how='left', on='pid').copy()
df_driver = df_driver.drop(columns=['ip_address'])

# Layout

layout = html.Div([
    dcc.Dropdown(
        id='graph-filter',
        options=[
            {'label': 'Vocation', 'value': 'Voc'},
            {'label': 'Vehicle Class', 'value': 'Vic_clas'},
            {'label': 'Vehicle Type', 'value': 'vic_tipe'},
            {'label': 'Person per Fahrzeug', 'value': 'person'}
        ],
        value=df_driver['vocation'].unique(),
        multi=True,
    ),
    dcc.Graph(
        id='graph'
    ),
    dcc.Dropdown(
        id='vocation-dropdown-table',
        options=[{'label': i, 'value': i} for i in sorted(df_driver['vocation'].unique())],
        value=df_driver['vocation'].unique(),
        multi=True,
    ),
    html.A(html.Button('Refresh Settings'),id='back_button',className='vehicles-tables-button-previous-level', href='/'),
    dt.DataTable(
        id='year-table2',
        data=[{}],
        columns=[{'id': c, 'name': c, "deletable": True, "selectable": True} for c in df_driver.columns],
        filter_action="native",
        editable=True,
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        selected_columns=[],
        page_action="native",
        page_current= 0,
        page_size= 40,
    ),
    html.Div(id='year-table')
])