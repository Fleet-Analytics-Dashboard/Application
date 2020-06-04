import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

fleet_data = pd.read_csv('../batch-data/cleaned-data-for-fleet-dna.csv')
fleet_data = fleet_data.head(10) # limits the displayed rows to 10

page_layout = html.Div([
    html.H1('Controlling'),
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
