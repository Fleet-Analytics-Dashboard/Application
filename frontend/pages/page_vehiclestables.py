import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import dash

fleet_data = pd.read_csv('../../batch-data/cleaned-data-for-fleet-dna.csv')

page_layout = html.Div([
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
    html.Div(id='page-vehicles-tables-content'),
    dcc.RadioItems(
        id='page-vehicles-tables-radios',
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


df = pd.read_csv('../../batch-data/cleaned-data-for-fleet-dna.csv')
df_vehicle_table1 = df[['vid','vehicel_type','drivetrain_type','fuel_type','day_id','speed_data_duration_hrs_includes_zero']]


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

PAGE_SIZE = 10

app.layout = dash_table.DataTable(
    id='datatable-paging',
    columns=[
        {"name": i, "id": i} for i in sorted(df_vehicle_table1.columns)
    ],
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom',
)

@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
     Input('datatable-paging', "page_size")])
def update_table(page_current,page_size):
    return df_vehicle_table1.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, port=8055)