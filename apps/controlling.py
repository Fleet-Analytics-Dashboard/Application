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
from database_connection import connect, return_engine
import dash_bootstrap_components as dbc

# connect to database
conn = connect()
sql = "select * from vehicle_data;"
df_vehicle_data = pd.read_sql_query(sql, conn)
sql = "select vid, vehicel_type, vocation, drivetrain_type, fuel_type from cleaned_data_fleet_dna;"
df_table = pd.read_sql_query(sql, conn)
sql = "select vid, vehicle_type, vocation from vehicle_data;"
df_vehicle_costs = pd.read_sql_query(sql, conn)
df_vehicle_costs = df_vehicle_costs.round(decimals=2)
sql = "select * from vehicle_cost_data"
df_cost_data = pd.read_sql_query(sql, conn)
df_cost_data = df_cost_data.round(decimals=2)
conn = None

# colors
colors_1 = ['rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)', 'rgb(67,67,67)']
colors = ['rgb(66,234,221)', 'rgb(7,130,130)', 'rgb(171,209,201)', 'rgb(151,179,208)', 'rgb(118,82,139)', 'rgb(173,239,209)', 'rgb(96,96,96)', 'rgb(214,65,97)']
colors_2 = ['rgb(171,209,201)', 'rgb(223,220,229)', 'rgb(219,176,74)', 'rgb(151,179,208)']
colors_3 = ['rgb(255,221,226)', 'rgb(250,160,148)', 'rgb(158,217,204)', 'rgb(0,140,118)']

colors_trend_1 = ['rgb(0,255,255)', 'rgb(0,0,139)', 'rgb(0,255,0)']
colors_trend = ['rgb(105,102,103)', 'rgb(105,102,103)', 'rgb(105,102,103)']

########### simulated data for the goals chart ###########
# goals data is company data/year; data in time range 2018-2021
years = np.vstack((np.arange(2016, 2021),) * 4)
y_data_revenue = np.random.normal(8, 1.5, 100)
y_data_revenue.sort()
y_data_profit = np.random.normal(7, 1.5, 100)
y_data_profit.sort()
y_data_liquidity = np.random.normal(7.5, 1.5, 100)
y_data_liquidity.sort()
y_data_goals = [y_data_revenue, y_data_profit, y_data_liquidity]
names_goals = ['Revenue', 'Profit', 'Liquidity']


############ data for the costs chart ##############
np.random.seed(1)
labels_costs = ['Overall', 'Fuel', 'Maintenance', 'Insurance']
mode_size = [8, 8, 12, 8]
line_size = [2, 2, 4, 2]

# period of a year in months (in this case until july)
x_data = np.array(['January', "February", 'March', 'April', 'Mai', 'June', 'July'])

# test data
y_data = np.array([
    [132, 138, 150, 144, 129, 128, 132, 145, 137, 138, 141, 147],
    [74, 82, 80, 74, 73, 72, 74, 70, 70, 66, 66, 69],
    [45, 42, 50, 46, 36, 36, 34, 35, 32, 31, 31, 28],
    [13, 14, 20, 24, 20, 24, 24, 40, 35, 41, 43, 50],
])

# transform the different columns of the data frame into lists
y_data_fuel_cost = df_cost_data['fuel_cost_total'].to_list()
y_data_insurance_cost = df_cost_data['insurance_cost'].to_list()
y_data_maintenance_cost = df_cost_data['maintenance_cost'].to_list()
y_data_total_cost = df_cost_data['total_cost'].to_list()

# summarise the cost lists in an array
y_data_cost = [y_data_total_cost, y_data_fuel_cost, y_data_maintenance_cost, y_data_insurance_cost]

###### chained dropdown for the filtering of chart costs ##########
# create option for dropdown
dropdown_options = {
    'Beverage Delivery': ['1', '2', '3', '4', '5', '6', '7', '8', '23', '24', '25'],
    'Food Delivery': ['47', '48', '49', '50', '51', '52', '154', '156', '573', '574'],
    'Linen Delivery': ['58', '59', '61', '62', '124', '125', '129', '130', '241'],
    'Parcel Delivery': ['9', '10', '11', '12', '20', '36', '37', '40', '42', '43', '108', '109', '110', '220'],
    'Telecom': ['284', '286', '287', '288', '290', '293', '306', '307'],
    'Utility': ['264', '242'],
    'Warehouse Delivery': ['28', '26', '30', '31', '29', '32', '33']
}

option = list(dropdown_options.keys())
nestedOptions = dropdown_options[option[0]]

########## simulated data for the carbon footprint chart ###########
x_data_carbon = np.vstack((np.arange(2016, 2021),) * 4)
y_data_carbon = np.random.normal(0.5, 0.1, 100)
# sort the data descending
y_data_carbon = np.sort(y_data_carbon)[::-1]
y_data_carbon_footprint = [y_data_carbon]

########## simulated data for delivery dates chart ###########
x_data_delivery = np.array(['January', "February", 'March', 'April', 'Mai', 'June', 'July'])
y_data_delivery = np.random.random_integers(400, 450, 900)
y_data_kept_delivery = [y_data_delivery]

########## goals bar chart ############
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
                                   marker_color=colors[i],
                                   name=names_goals[i]
                                   ))

fig_goals.update_layout(
    plot_bgcolor='white',
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
        title='Dollar (millions)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    #legend=dict(
    #    x=0,
    #    y=1.0
    #),
    barmode='group',
    bargap=0.15,  # gap between bars of adjacent location coordinates
    bargroupgap=0.1  # gap between bars of the same location coordinate
)

annotations_1 = [dict(xref='paper', yref='paper', x=0.0, y=1.05,
                      xanchor='left', yanchor='bottom',
                      text='',
                      font=dict(family='Arial',
                                size=30,
                                color='rgb(37,37,37)'),
                      showarrow=False)]

# Title chart goals

fig_goals.update_layout(annotations=annotations_1)

####### line chart carbon footprint #########

fig_carbon = go.Figure()

for i in range(0, 1):
    fig_carbon.add_trace(go.Scatter(
        x=x_data_carbon[i],
        y=y_data_carbon_footprint[i], mode='lines+markers',
        name='Carbon Footprint',
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
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
    autosize=True,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),

    showlegend=False,
    plot_bgcolor='white'
)

annotations = [dict(xref='paper', yref='paper', x=0.0, y=1.05,
                    xanchor='left', yanchor='bottom',
                    text='',
                    font=dict(family='Arial',
                              size=30,
                              color='rgb(37,37,37)'),
                    showarrow=False)]

# Title chart carbon

fig_carbon.update_layout(annotations=annotations)

######### line chart kept delivery dates #############

fig_delivery_dates = go.Figure()

for i in range(0, 1):
    fig_delivery_dates.add_trace(go.Scatter(
        x=x_data_delivery,
        y=y_data_kept_delivery[i], mode='lines+markers',
        name='Kept delivery dates',
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True
    ))


fig_delivery_dates.update_layout(
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
        title='kept delivery dates/month',
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

    showlegend=False,
    plot_bgcolor='white'
)

########### line chart costs #############
fig_costs = go.Figure()

for i in range(0, 4):
    fig_costs.add_trace(go.Scatter(
        x=x_data,
        y=y_data_cost[i], mode='lines+markers',
        name=labels_costs[i],
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
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
    autosize=True,
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
for y_trace, label, color in zip(y_data_cost, labels_costs, colors):
    # labeling the left_side of the plot
    annotations.append(dict(xref='paper', x=0.05, y=y_trace[0],  # hier stand 0 (?)
                            xanchor='right', yanchor='middle',
                            text=label,
                            font=dict(family='Arial',
                                      size=16),
                            showarrow=False))
    # labeling the right_side of the plot
    annotations.append(dict(xref='paper', x=0.95, y=y_trace[11],  # hier stand 11
                            xanchor='left', yanchor='middle',
                            text='{} $'.format(y_trace[11]),  # hier stand 11
                            font=dict(family='Arial',
                                      size=14),
                            showarrow=False))

# Title chart costs
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                        xanchor='left', yanchor='bottom',
                        text='',
                        font=dict(family='Arial',
                                  size=30,
                                  color='rgb(37,37,37)'),
                        showarrow=False))

fig_costs.update_layout(annotations=annotations)

######## pie chart vehicle capacity ########

# new dataframe for filter result
df_vehicle_status = df_vehicle_data.copy()

# array with accepted values
accepted_vehicle_status_array = ['in time', 'delayed', 'unused', 'maintenance', 'idle']

# filter
df_vehicle_status = df_vehicle_status.loc[df_vehicle_data['vehicle_status'].isin(accepted_vehicle_status_array)]

# use unique values as labels
labels = df_vehicle_status['vehicle_status'].unique()

# count values
values = df_vehicle_status.vehicle_status.value_counts()

pie_capacity = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
pie_capacity.update_traces(marker=dict(colors=colors))


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


layout = html.Div(
    className='controlling-content',
    children=[

        # Date Picker
        html.Div(
            [
                dcc.DatePickerRange(
                    id='controlling-date-picker-range',
                    min_date_allowed=dt(1995, 8, 5),
                    max_date_allowed=dt(2020, 6, 19),
                    initial_visible_month=dt(2020, 6, 5),
                    end_date=dt(2020, 6, 5).date()
                ),
                html.Div(id='output-container-date-picker-range')
            ], className='data-picker',
        ),

        dbc.Row([
            # Business Goals
            dbc.Col(html.Div([
                html.H1('Business Goals'),
                dcc.Graph(id='graph-goals', figure=fig_goals)
            ], className='card'), width=True),

            # Costs
            dbc.Col(html.Div([
                html.H1('Costs'),
                dcc.Dropdown(
                    id='dropdown-category',
                    options=[{'label': option, 'value': option}
                             for option in dropdown_options],
                    value=list(dropdown_options.keys())[0],
                    placeholder="Select vehicle category",
                ),
                dcc.Dropdown(
                    id='id-dropdown',
                    options=[{'label': i, 'value': i}
                             for i in df_cost_data.vid.unique()],
                    placeholder="Select vehicle id",
                ),

                html.Div(id='display-selected-values'),
                dcc.Graph(id='costs-chart',
                          figure=fig_costs
                          ),
            ], style=dict(display='flex'), className='card'), width=True),
        ]),

        html.Div(className='bottom-cards around',
                 children=[
                     dbc.Row([
                         # Carbon Footprint
                         dbc.Col(html.Div([
                             html.H1('Carbon Footprint'),
                             dcc.Graph(id='graph-carbon-footprint', figure=fig_carbon)
                         ], className='card'), width=True),
                         # Kept delivery dates
                         dbc.Col(html.Div([
                            html.H1('Kept delivery dates'),
                            dcc.Graph(id='graph-delivery-date', figure=fig_delivery_dates)
                             ], className='card'), width=True),
                         ]),
                     dbc.Row([
                         # Vehicle capacity
                         dbc.Col(html.Div([
                             html.H1('Vehicle Capacity'),
                             dbc.Row([
                                 dbc.Col(html.Div([
                                     dcc.Graph(figure=pie_capacity, config={'responsive': True}, className='piechart'),
                                 ], className='card'), width=True),
                                 dbc.Col(html.Div([
                                     dcc.Checklist(
                                         id='page-controlling-radios-3',
                                         options=[{'label': i, 'value': i}
                                                  for i in ['in time', 'delayed', 'maintenance', 'idle', 'unused']],
                                         value=['in time', 'delayed', 'maintenance', 'idle', 'unused'],
                                         ),
                                     dash_table.DataTable(
                                         id='table-for-capacity',
                                         filter_action='native',
                                         sort_action='native',
                                         style_table={
                                             'maxHeight': '',
                                             'maxWidth': '',
                                             'overflowY': '',

                                         },
                                         data=[{}],
                                         columns=[{'name': i, 'id': i} for i in
                                                  df_vehicle_data.loc[:, ['licence_plate', 'vehicle_status']]],
                                         page_size=10,
                                         style_data={
                                             'whiteSpace': 'normal',
                                             'height': 'auto',
                                             'align': 'right'
                                         },
                                         style_header={
                                             'backgroundColor': '#f1f1f1',
                                             'fontWeight': 'bold',
                                             'fontSize': 12,
                                             'fontFamily': 'Open Sans'
                                         },
                                         style_cell={
                                             'padding': '5px',
                                             'fontSize': 13,
                                             'fontFamily': 'sans-serif'
                                         },

                                     ), ], className='card'), width=True),
                             ]),

                         ], className='card'), width=True)
                     ]),
                 ])
    ])


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
