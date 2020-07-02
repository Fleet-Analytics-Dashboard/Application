import pandas as pd
import dash_html_components as html
from database_connection import connect
import dash_table

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


layout = html.Div(children=[
    html.H1(children='Overview'),

    html.Div(children='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                      'labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco '
                      'laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in '
                      'voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat '
                      'non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'),

    html.Div(dash_table.DataTable(
        id='table-2',
        data=fleet_data.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in fleet_data.loc[:]
                 ],
    ), )
])
