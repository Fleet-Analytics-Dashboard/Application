import dash_core_components as dcc
import dash_html_components as html
import dash_table
from pandas.tests.groupby.test_value_counts import df
import pandas as pd

fleet_data = pd.read_csv('../batch-data/cleaned-data-for-fleet-dna.csv')

page_4_layout = html.Div([
    html.H1('Vehicles Tables'),
    html.Br(),
    dcc.Link('Go to to overview', href='/'),
    html.Br(),
    dcc.Link('Go to to controlling view ', href='/page-2'),
    html.Br(),
    dcc.Link('Go to downtimes view', href='/page-3'),
    html.Br(),
    dcc.Link('Go to vehicles tables view', href='/page-4'),
    html.Br(),
    html.Br(),
    html.Div(id='page-4-content'),
    dcc.RadioItems(
        id='page-4-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Br(),
    html.Br(),
    dash_table.DataTable(
        data=fleet_data.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in fleet_data.columns],
        style_cell={'textAlign': 'left'},
        style_cell_conditional=[
            {
                'if': {'column_id': 'Region'},
                'textAlign': 'left'
            }
        ])
])
