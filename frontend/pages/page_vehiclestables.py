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
    id='table-paging-and-sorting',
    columns=[
        {'name': i, 'id': i, 'deletable': True} for i in df_vehicle_table1.columns
    ],
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom',

    sort_action='custom',
    sort_mode='single',
    sort_by=[]
)

@app.callback(
    Output('table-paging-and-sorting', 'data'),
    [Input('table-paging-and-sorting', "page_current"),
     Input('table-paging-and-sorting', "page_size"),
     Input('table-paging-and-sorting', 'sort_by')])
def update_table(page_current, page_size, sort_by):
    if len(sort_by):
        dff = df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df_vehicle_table1

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, port=8055)