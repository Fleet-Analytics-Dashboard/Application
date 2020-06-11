import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import dash
from datetime import datetime as dt
import re
from loremipsum import get_sentences

fleet_data = pd.read_csv('../../batch-data/cleaned-data-for-fleet-dna.csv', index_col=0, parse_dates=True)
column_name_dropdown = fleet_data[['vid', 'vocation']]

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
                                html.Div(
                                    className='div for graph 1',
                                    children=[
                                        dcc.RadioItems(
                                            id='page-controlling-radios',
                                            options=[{'label': i, 'value': i} for i in ['Revenue', 'Profit', 'Liquidity']],
                                            value='Revenue'),
                                        #html.Div(id='radio-items-output'),
                                        dcc.Graph(id='graph-goals', config={'displayModeBar': False}, animate=True),
                                        #dcc.Tabs(
                                            #children=[
                                                #{'label': 'Revenue', 'value': 1},
                                                #{'label': 'Profit', 'value': 2},
                                                #{'label': 'Liquidity', 'value': 3}
                                            #],
                                            #value=3,
                                            #id='test'
                                        #),
                                        #html.Div(id='radio-items-output')
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
                                    className='div for graph 3',
                                    children=[
                                        dcc.Graph(id='graph-carbon-footprint', config={'displayModeBar': False}, animate=True)
                                    ]
                                )
                             ]),
                    html.Div(className='right part',
                             children=[
                                html.H2('Costs'),
                                html.Div(
                                    className='div for graph 4',
                                    children=[
                                        dcc.RadioItems(
                                            id='page-controlling-radios-2',
                                            options=[{'label': i, 'value': i}
                                                     for i in ['Overall', 'Fuel', 'Maintenance', 'Insurance']],
                                            value='Overall'),
                                        html.Div(
                                            className='div for dropdown',
                                            children=[
                                                dcc.Dropdown(
                                                    id='controlling-dropdown',
                                                    options=[{'label': i, 'value': i}
                                                             for i in fleet_data.vid.unique()],
                                                    placeholder="Choose vehicle id",
                                                ),
                                                html.Div(id='dd-output-container')
                                            ]
                                        ),
                                        dcc.Graph(id='graph-costs', config={'displayModeBar': False}, animate=True),
                                    ]),
                                html.H2('Vehicle capacity'),
                                html.Div(
                                    className="div for graph 5",
                                    children=[
                                        dcc.Checklist(
                                            id='page-controlling-radios-3',
                                            options=[{'label': i, 'value': i}
                                                     for i in ['In time', 'Delayed', 'Downtime', 'Unused']],
                                            value=['In time']),
                                        dash_table.DataTable(
                                            id='table-for-capacity',
                                            style_table={
                                              'maxHeight': '400px',
                                              'maxWidth': '400px',
                                              'overflowY': 'scroll'
                                            },
                                            style_data={
                                                'whiteSpace': 'normal',
                                                'height': 'auto',
                                                'align': 'left'
                                            },
                                            columns=[{'name': i, 'id': i} for i in column_name_dropdown.columns],
                                            data=column_name_dropdown.to_dict('records')
                                        ),
                                        html.Div(id='table-output-container')

                                    ])
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


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('controlling-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    dash.dependencies.Output('radio-items-output', 'children'),
    [dash.dependencies.Input('page-controlling-radios', 'value')])
def display_content(value):
    data = [
        {
            'x': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                  2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
            'y': [219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                  350, 430, 474, 526, 488, 537, 500, 439],
            'name': 'Rest of world',
            'marker': {
                'color': 'rgb(55, 83, 109)'
            },
            'type': ['bar', 'scatter', 'box'][int(value) % 3]
        },
        {
            'x': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                  2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
            'y': [16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                  299, 340, 403, 549, 499],
            'name': 'China',
            'marker': {
                'color': 'rgb(26, 118, 255)'
            },
            'type': ['bar', 'scatter', 'box'][int(value) % 3]
        }
    ]

    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                    'margin': {
                        'l': 30,
                        'r': 0,
                        'b': 30,
                        't': 0
                    },
                    'legend': {'x': 0, 'y': 1}
                }
            }
        ),
        html.Div(' '.join(get_sentences(10)))
    ])


#@app.callback(
#        dash.dependencies.Output('table-output-container', 'children'),
#        [dash.dependencies.Input('table-for-capacity', 'page_current')])
#def update_output(page_current):
#    return 'You have selected "{}"'.format(page_current)


if __name__ == '__main__':
    app.run_server(debug=True)