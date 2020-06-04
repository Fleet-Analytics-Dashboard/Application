import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import dash
from datetime import datetime as dt
import re

fleet_data = pd.read_csv('../../batch-data/cleaned-data-for-fleet-dna.csv', index_col=0, parse_dates=True)
df_controlling_dropdown = fleet_data[['vid','vehicel_type','drivetrain_type']]

page_layout = html.Div([
    html.H1('Controlling'),
    html.Br(),
    dcc.Link('Go to to overview', href='/'),
    dcc.Link('Go to to controlling view ', href='/page-2'),
    dcc.Link('Go to downtimes view', href='/page-3'),
    dcc.Link('Go to vehicles tables view', href='/page-4'),
    html.Br(),
    html.Br(),
    html.Div(id='page-controlling-content'),
    dcc.RadioItems(
        id='page-controlling-radios',
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


# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='left part',
                             children=[
                                html.Div(
                                    className='div for datepicker',
                                    children=[
                                        dcc.DatePickerRange(
                                            id='controlling-date-picker-range',
                                            min_date_allowed=dt(1995, 8, 5),
                                            max_date_allowed=dt(2020, 6, 19),
                                            initial_visible_month=dt(2020, 6, 5),
                                            end_date=dt(2020, 6, 5).date()
                                        ),
                                        html.Div(id='output-container-date-picker-range')
                                    ]
                                ),
                                html.H2('Business Goals'),
                                dcc.RadioItems(
                                    id='page-controlling-radios',
                                    options=[{'label': i, 'value': i} for i in ['Revenue', 'Profit', 'Liquidity']],
                                    value='Revenue'),
                                html.Div(
                                    className='div for graph 1',
                                    children=[
                                        dcc.Graph(id='graph-goals', config={'displayModeBar': False}, animate=True)
                                    ]
                                ),
                                html.H2('Kept delivery dates'),
                                html.Div(
                                    className='div for graph 2',
                                    children=[
                                        dcc.Graph(id='graph-delivery-date', config={'displayModeBar': False}, animate=True)
                                    ]
                                ),
                                html.H2('Carbon footprint'),
                                html.Div(
                                    className='div for graph 2',
                                    children=[
                                        dcc.Graph(id='graph-carbon-footprint', config={'displayModeBar': False}, animate=True)
                                    ]
                                )
                            ]),
                    html.Div(className='right part',
                             children=[
                                html.H2('Costs'),
                                dcc.RadioItems(
                                    id='page-controlling-radios-2',
                                    options=[{'label': i, 'value': i} for i in ['Overall', 'Fuel', 'Maintenance','Insurance']],
                                    value='Overall'),
                                html.Div(
                                    className='div for dropdown',
                                    children=[
                                        dcc.Dropdown(
                                            id='controlling-dropdown',
                                            options=[{'label': i, 'value': i}
                                                     for i in df_controlling_dropdown.columns])
                                    ]
                                ),
                                html.Div(
                                    className='div for graph 1',
                                    children=[
                                        dcc.Graph(id='graph-costs', config={'displayModeBar': False}, animate=True)
                                    ]
                                        )

                            ])

                ])
    ])


@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

if __name__ == '__main__':
    app.run_server(debug=True)