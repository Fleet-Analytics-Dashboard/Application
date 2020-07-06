import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import dash
from datetime import datetime as dt
import re
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from database_connection import connect, return_engine

# connect to database and add files to
#conn = connect()
#sql = "select vid, vehicel_type, vocation, drivetrain_type, fuel_type from cleaned_data_fleet_dna;"
#df_table = pd.read_sql_query(sql, conn)
#conn = None
df_table = pd.read_csv(r'C:\Users\Larisa\PycharmProjects\Application\batch-data\cleaned-data-for-fleet-dna_v3.csv')

#df = pd.read_csv('../../batch-data/cleaned-data-for-fleet-dna.csv', index_col=0, parse_dates=True)
#column_name_dropdown = fleet_data[['vid', 'vocation']]
df_goals = pd.read_csv(r'C:\Users\Larisa\PycharmProjects\Application\apps\Graph Goals.csv')
#df_goals = pd.read_csv('GraphGoals.csv', index_col=0, parse_dates=True)
df_goals.index = pd.to_datetime(df_goals['Id'])

#mock data for goals chart
years = np.vstack((np.arange(2014, 2021),)*4)
y_data_revenue = np.random.normal(8, 1.5, 100)
y_data_revenue.sort()
y_data_profit = np.random.normal(7, 1.5, 100)
y_data_profit.sort()
y_data_liquidity = np.random.normal(7.5, 1.5, 100)
y_data_liquidity.sort()
y_data_goals = [y_data_revenue, y_data_profit, y_data_liquidity]
names_goals =['Revenue', 'Profit', 'Liquidity']

# regression
#reg = LinearRegression().fit(np.vstack(df_goals_chart['X']), y_data_revenue)
#df_goals_chart['bestfit'] = reg.predict(np.vstack(df_goals_chart['X']))


# mock data for costs chart
np.random.seed(1)
colors = ['rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)', 'rgb(67,67,67)']
colors_trend = ['rgb(0,255,0)', 'rgb(0,0,139)', 'rgb(0,255,255)']
labels_goals = ['Revenue', 'Profit', 'Liquidity']
labels_costs = ['Overall', 'Fuel', 'Maintenance', 'Insurance']
mode_size = [8, 8, 12, 8]
line_size = [2, 2, 4, 2]

x_data = np.vstack((np.arange(2009, 2022),)*4)

y_data = np.array([
    [132, 138, 150, 144, 129, 128, 132, 145, 137, 138, 141, 147],
    [74, 82, 80, 74, 73, 72, 74, 70, 70, 66, 66, 69],
    [45, 42, 50, 46, 36, 36, 34, 35, 32, 31, 31, 28],
    [13, 14, 20, 24, 20, 24, 24, 40, 35, 41, 43, 50],
])

#bar chart goals

fig_goals = go.Figure()

for i in range(0, 3):
    fig_goals.add_trace(go.Bar(x=years[i],
                               y=y_data_goals[i],
                               name=names_goals[i],
                               marker_color=colors[i]))
    fig_goals.add_trace(go.Scatter(x=years[i],
                                   y=y_data_goals[i],
                                   mode='lines+markers',
                                   line=dict(
                                       width=3,
                                   ),
                                   connectgaps=True,
                                   marker_color=colors_trend[i],
                                   name=names_goals[i]
                                   ))


fig_goals.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='EUR (millions)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate
)

annotations_1 = []

# Title chart goals
annotations_1.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                        xanchor='left', yanchor='bottom',
                        text='Business Goals',
                        font=dict(family='Arial',
                                  size=30,
                                  color='rgb(37,37,37)'),
                        showarrow=False))

fig_goals.update_layout(annotations=annotations_1)

# line chart carbon footprint

fig_carbon = go.Figure()

for i in range(0,1):
    fig_carbon.add_trace(go.Scatter(
        x=x_data[i],
        y=df_goals['Carbon'], mode='lines',
        name='Carbon footprint',
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True
    ))


fig_carbon.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True,
        title='t CO2/Year',
        titlefont_size=16,
        tickfont_size=14,

    ),
    legend=dict(
        x=0,
        y=1.0),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),

    showlegend=True,
    plot_bgcolor='white'
)
annotations_1 = []

# Title chart carbon
annotations_1.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                        xanchor='left', yanchor='bottom',
                        text='Carbon footprint',
                        font=dict(family='Arial',
                                  size=30,
                                  color='rgb(37,37,37)'),
                        showarrow=False))

fig_carbon.update_layout(annotations=annotations_1)

# line chart costs
fig_costs = go.Figure()

for i in range(0, 4):
    fig_costs.add_trace(go.Scatter(x=x_data[i], y=y_data[i], mode='lines',
        name=labels_costs[i],
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
    ))

    # endpoints
    fig_costs.add_trace(go.Scatter(
        x=[x_data[i][0], x_data[i][-1]],
        y=[y_data[i][0], y_data[i][-1]],
        mode='markers',
        marker=dict(color=colors[i], size=mode_size[i])
    ))


fig_costs.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
    ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=False,
    plot_bgcolor='white'
)

annotations = []

# Adding labels
for y_trace, label, color in zip(y_data, labels_costs, colors):
    # labeling the left_side of the plot
    annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],
                                  xanchor='right', yanchor='middle',
                                  text=label,
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))
    # labeling the right_side of the plot
    annotations.append(dict(xref='paper', x=0.95, y=y_trace[11],
                            xanchor='left', yanchor='middle',
                            text='{} MEUR'.format(y_trace[11]),
                            font=dict(family='Arial',
                                      size=14),
                            showarrow=False))


# Title chart costs
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                        xanchor='left', yanchor='bottom',
                        text='Costs',
                        font=dict(family='Arial',
                                  size=30,
                                  color='rgb(37,37,37)'),
                        showarrow=False))


fig_costs.update_layout(annotations=annotations)

# pie chart vehicle capacity

labels_capacity = ['In Time', 'Delayed', 'Downtime', 'Unused']
values_capacity = [20, 30, 10, 40]
pie_capacity = go.Figure(data=[go.Pie(labels=labels_capacity, values=values_capacity, hole=.3)])


# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


def get_options(list_data):
    dict_list = []
    for i in list_data:
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


layout = html.Div([
        html.Div(className='row',
                 children=[
                    html.Div(className='left part',
                             children=[
                                html.Div([
                                    dcc.DatePickerRange(
                                        id='controlling-date-picker-range',
                                        min_date_allowed=dt(1995, 8, 5),
                                        max_date_allowed=dt(2020, 6, 19),
                                        initial_visible_month=dt(2020, 6, 5),
                                        end_date=dt(2020, 6, 5).date()
                                    ),
                                    html.Div(id='output-container-date-picker-range')
                                ]),

                                html.Div([
                                    #dcc.Dropdown(
                                        #id='page_controlling_radios',
                                        #options=[{'label': i, 'value': i} for i in labels_goals],
                                        #options=get_options(df['goals'].unique()),
                                        #multi=True,
                                        #value=[df['goals'].sort_values()[0]],
                                        #className='stockselektor'),
                                    #html.Div(id='display-selected-values'),
                                    dcc.Graph(id='graph-goals', figure=fig_goals)
                                ],
                                    #style={'width': '49%', 'display': 'inline-block'},
                                ),

                                #html.H2('Kept delivery dates'),
                                #html.Div([
                                    #dcc.Graph(id='graph-delivery-date',
                                              #config={'displayModeBar': False},
                                              #animate=True)
                                #], style={'width': '25%', 'display': 'inline-block'}),

                                html.Div([
                                    dcc.Graph(id='graph-carbon-footprint', figure=fig_carbon)
                                ],
                                    style={'width': '25%', 'display': 'inline-block'})
                             ]),
                    html.Div(className='right part',
                             children=[
                                html.Div([
                                    html.Div([
                                        dcc.Dropdown(
                                            id='controlling-dropdown',
                                            options=[{'label': i, 'value': i}
                                                     for i in df_table.vid.unique()],
                                            placeholder="Choose vehicle id",
                                        ),
                                        #dcc.RadioItems(
                                        #    id='page-controlling-radios-2',
                                        #    options=[{'label': i, 'value': i}
                                        #             for i in ['Overall', 'Fuel', 'Maintenance', 'Insurance']],
                                        #    value='Overall',
                                        #    labelStyle={'display': 'inline-block'}
                                        #),

                                    ],
                                        style={'width': '49%', 'display': 'inline-block'}),
                                    dcc.Graph(id='indicator-graphic', figure=fig_costs)
                                ]),

                                html.H2('Vehicle capacity'),
                                html.Div([
                                    dcc.Checklist(
                                        id='page-controlling-radios-3',
                                        options=[{'label': i, 'value': i}
                                                 for i in ['In time', 'Delayed', 'Idle', 'Unused']],
                                        value=['In time']),
                                    dash_table.DataTable(
                                        id='table-for-capacity',
                                        style_table={
                                            'maxHeight': '400px',
                                            'maxWidth': '800px',
                                            'overflowY': 'scroll'
                                        },
                                        style_data={
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'align': 'right'
                                        },
                                        columns=[{'name': i, 'id': i} for i in df_table.columns],
                                        data=df_table.to_dict('records')
                                    ),
                                    dcc.Graph(figure=pie_capacity, style={'width': '59%', 'margin': '0'}),
                                    html.Div(id='table-output-container'),


                                ],
                                    style={'width': '50%', 'display': 'inline-block'})

                             ])

                     ])
    ])

# callback chart costs; still not working
#@app.callback(
#    dash.dependencies.Output('indicator-graphic', 'figure'),
#    [dash.dependencies.Input('controlling-dropdown', 'value'),
#     dash.dependencies.Input('page-controlling-radios-2', 'value')])
#def update_graph(controlling_dropdown_name, controlling_radios_name):
#    return {
#        'data': [dict(
#            x=column_name_dropdown['vid'] == x_data['value'],
#            y=column_name_dropdown['vid'] == y_data['value'],
#            mode='markers',
#            marker={
#                'size': 15,
#                'opacity': 0.5,
#                'line': {'width': 0.5, 'color': 'white'}
#            }
#        )],
#        'layout': dict(
#            xaxis={
#                'title': controlling_dropdown_name,
#                'type': 'fuel' if controlling_radios_name == 'fuel' else 'overall'
#            },
#            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
#            hovermode='closest'
#        )
#    }


# callback chart goals; still not working
#@app.callback(
#    Output('graph-goals', 'figure'),
#    [Input('page_controlling_radio', 'value')])
#def update_graph_goals(selected_filter):
#    trace1 = []
#    df_sub = df
#    for goals in selected_filter:
#        trace1.append(go.Scatter(x=df_sub[df_sub['goals'] == goals].index,
#                                 y=df_sub[df_sub['goals'] == goals]['value'],
#                                 mode='lines',
#                                 opacity=0.7,
#                                 name=goals,
#                                 textposition='bottom center'))
#    traces = [trace1]
#    data = [val for sublist in traces for val in sublist]
#    figure = {'data': data,
#              'layout': go.Layout(
#                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
#                  template='plotly_dark',
#                  paper_bgcolor='rgba(0, 0, 0, 0)',
#                  plot_bgcolor='rgba(0, 0, 0, 0)',
#                  margin={'b': 15},
#                  hovermode='x',
#                  autosize=True,
#                  title={'text': 'Business Goals', 'font': {'color': 'white'}, 'x': 0.5},
#                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
#              ),

#              }

#    return figure



#@app.callback(
#    dash.dependencies.Output('graph-goals', 'value'),
#    [dash.dependencies.Input('graph-goals', 'figure')])
#def set_graph_value(available_options):
#    return available_options[0]['value']


#@app.callback(
#    dash.dependencies.Output('display-selected-values', 'children'),
#    [dash.dependencies.Input('page_controlling_radio', 'value'),
#     dash.dependencies.Input('graph-goals', 'value')])
#def set_display_children(selected_filter, selected_output):
#    return selected_filter, selected_output

# callback fill dropdown with fleet_data values; working
@app.callback(
    Output('dd-output-container', 'children'),
    [Input('controlling-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


# callback for date-picker
@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
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


#if __name__ == '__main__':
#    app.run_server(debug=True)