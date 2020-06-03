import dash_core_components as dcc
import dash_html_components as html
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
df_vehicle_table1 = df[['vehicel_type','drivetrain_type','fuel_type','day_id','speed_data_duration_hrs_includes_zero']]


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

app.layout = html.Div(children=[
    html.H4(children='Vehicle Table'),
    generate_table(df_vehicle_table1)
])

if __name__ == '__main__':
    app.run_server(debug=True)