import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import dash
import plotly.graph_objects as go
import numpy as np
from database_connection import connect
import dash_bootstrap_components as dbc

# connect to database
# conn = connect()
# sql = "select * from vehicle_data;"
# df_vehicle_data = pd.read_sql_query(sql, conn)
# sql = "select * from vehicle_cost_data"
# df_cost_data = pd.read_sql_query(sql, conn)
# df_cost_data = df_cost_data.round(decimals=2)
# sql = "select * from driving_data"
# df_driving_data = pd.read_sql_query(sql, conn)
# df_driving_data = df_driving_data.round(decimals=2)
# conn = None

# get data from csv files
df_vehicle_data = pd.read_csv('csv_data_files/vehicle_data.csv')
df_driving_data = pd.read_csv('csv_data_files/driving_data.csv')
df_driving_data = df_driving_data.round(decimals=2)
df_cost_data = pd.read_csv('csv_data_files/vehicle_cost_data.csv')
df_cost_data = df_cost_data.round(decimals=2)

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
ids = set(df_cost_data['vid'])
np.random.seed(1)
labels_costs = ['Overall', 'Fuel', 'Maintenance', 'Insurance']
mode_size = [8, 8, 12, 8]
line_size = [2, 2, 4, 2]

# period of a year in months (in this case until july)
x_data = np.array(['January', "February", 'March', 'April', 'Mai', 'June', 'July'])

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
        title='USD (millions)',
        titlefont_size=16,
        tickfont_size=14,
    ),
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
        line=dict(color=colors[1], width=line_size[i]),
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
        line=dict(color=colors[3], width=line_size[i]),
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

######## pie chart vehicle capacity ########

# new dataframe for filter result
df_vehicle_status = df_vehicle_data.copy()

# array with accepted values
accepted_vehicle_status_array = ['on time', 'delayed', 'unused', 'maintenance', 'idle', 'accident']

# filter
df_vehicle_status = df_vehicle_status.loc[df_vehicle_data['vehicle_status'].isin(accepted_vehicle_status_array)]

# use unique values as labels
lables = df_vehicle_status.groupby(['vehicle_status'])['licence_plate'].count().reset_index()
lables.columns = (['vehicle_status', 'Amount'])

# count values
values = df_vehicle_status.vehicle_status.value_counts()

text = len(df_vehicle_status)

pie_capacity = go.Figure(data=[go.Pie(labels=lables['vehicle_status'], values=lables['Amount'], hole=.3)])
pie_capacity.update_traces(marker=dict(colors=colors))
pie_capacity.update_layout(
    annotations=[dict(text=text, font_size=20, showarrow=False)]
)



########## calculation for title cards ############

    ##Cost Juli

cost_juli = df_cost_data.groupby(['month']).sum()
cost_juli = cost_juli.loc['July']
cost_juli = cost_juli.round(decimals=2)

cost_juni = df_cost_data.groupby(['month']).sum()
cost_juni = cost_juni.loc['June']
cost_juni = cost_juni.round(decimals=2)

cost_change = (cost_juli['total_cost'] / cost_juni['total_cost'])-1
cost_change = cost_change*100
cost_change = cost_change.round(decimals=2)

##vehicle_active + total

df_vehicle_active = values.loc[['delayed', 'idle', 'on time']]
df_vehicle_active = df_vehicle_active.sum()

df_vehicle_total = values
df_vehicle_total = df_vehicle_total.sum()

## availability rate

availability_rate = values.loc[['accident', 'delayed', 'idle', 'maintenance', 'on time']]
availability_rate = availability_rate.sum()
availability_rate = (1 - (availability_rate / df_vehicle_total)) * 100
availability_rate = availability_rate.round(decimals=2)

    ## profit

profit = 100000
revenue = (cost_juli['total_cost']) + (profit)


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

        html.Div(className='top-cards around',
                 children=[
                     dbc.Row([
                         # Profit
                         dbc.Col(html.Div([
                             html.H5('Profit'),
                             html.H2(str(profit) + "$"),
                             html.H4("+3%")
                         ], className='card'), width=True),

                         # Revenue
                         dbc.Col(html.Div([
                             html.H5('Revenue'),
                             html.H2(str(revenue) + "$"),
                             html.H4("+8%")
                         ], className='card'), width=True),

                         # Cost card
                         dbc.Col(html.Div([
                             html.H5('Cost'),
                             html.H2(str(cost_juli['total_cost']) + '$'),
                             html.H4("+" + str(cost_change) + "%")
                         ], className='card'), width=True),

                         # Total Number vehicle
                         dbc.Col(html.Div([
                             html.H5('Total Number of Vehicles'),
                             html.H2(df_vehicle_total),
                             html.H4(" ")
                         ], className='card'), width=True),

                         # Vehicle active
                         dbc.Col(html.Div([
                             html.H5('Active Vehicle'),
                             html.H2(df_vehicle_active),
                             html.H4(" ")
                         ], className='card'), width=True),

                         # Vehicle maintenance
                         dbc.Col(html.Div([
                             html.H5('Vehicle in Maintenance'),
                             html.H2(values['maintenance']),
                             html.H4(" ")
                         ], className='card'), width=True),

                         # Vehicle unused
                         dbc.Col(html.Div([
                             html.H5('Unused Vehicle'),
                             html.H2(values['unused']),
                             html.H4(" ")
                         ], className='card'), width=True),

                         # Availability rate
                         dbc.Col(html.Div([
                             html.H5('Availability rate'),
                             html.H2(str(availability_rate) + "%"),
                             html.H4(" ")
                         ], className='card'), width=True),
                     ]),
                ]),
        dbc.Row([
            # Business Goals
            dbc.Col(html.Div([
                html.H1('Business Goals'),
                dcc.Graph(id='graph-goals', figure=fig_goals)
            ], className='card'), width=True),

            # Costs
            dbc.Col(html.Div([
                html.H1('Costs'),
                html.Div([
                    dcc.Dropdown(
                        id='dropdown-category',
                        options=[{'label': option, 'value': option}
                                 for option in dropdown_options],
                        value=list(dropdown_options.keys())[0],
                        placeholder="Select vehicle category",
                    ),
                    dcc.Dropdown(
                        id='id-dropdown',
                        options=[{'value': x, 'label': x} for x in ids],
                        multi=True, value=['1', '2', '3'],
                        placeholder="Select vehicle id",
                    ),
                    dcc.Dropdown(id='memory-field', options=[
                        {'value': 'fuel_cost_total', 'label': 'Fuel Cost'},
                        {'value': 'maintenance_cost', 'label': 'Maintenance cost'},
                        {'value': 'insurance_cost', 'label': 'Insurance cost'},
                        {'value': 'total_cost', 'label': 'Total costs'}
                    ], value='total_cost'),
                ], className='dropdown-alignment'),
                dcc.Store(id='memory-output'),
                html.Div([
                    dcc.Graph(id='costs-chart'),
                ]),
            ], className='card'), width=True),
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
                                 html.H1('Vehicle Status'),
                                 dcc.Graph(figure=pie_capacity, config={'responsive': True}, className='piechart'),
                                 ], className='card'), width=True),

                         # Capacity overview pro vehicle
                         dbc.Col(html.Div([
                                 html.H1('Capacity Overview'),
                                 dcc.Checklist(
                                         id='page-controlling-radios-3',
                                         options=[{'label': i, 'value': i}
                                                  for i in ['on time', 'delayed', 'maintenance', 'idle', 'unused', 'accident']],
                                         value=['on time', 'delayed', 'maintenance', 'idle', 'unused', 'accident'],
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
                 ])
    ])
