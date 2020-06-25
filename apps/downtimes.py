import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go
import calendar
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc
import app

# from database_connection import connect, return_enginge

# connect to database and add files to
# conn = connect()
# sql = "select * from cleaned_data_fleet_dna;"
# fleet_data = pd.read_sql_query(sql, conn)
# conn = None

# Daten
fleet_data = pd.read_csv('cleaned-data-for-fleet-dna.csv')
fleet_data = fleet_data.head(10)  # limits the displayed rows to 10
# fleet_data.iloc[:,1:3]


# PieCharts

# Downtimes Overview

labels = ['Accidents', 'Traffic Jams', 'Maintenance', 'Unused']
values = [20, 30, 10, 40]

pie1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Need for Maintenance

labels = ['Need', 'Soon', 'No need']
values = [2, 5, 10]

pie2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Accident Probability

labels = ['Category 1', 'Category 2', 'Category 3']
values = [20, 30, 10, 40]

pie3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Mapbox
# mapbox_access_token = open(".mapbox_token").read()

fig = go.Figure(go.Scattermapbox(
    lat=['38.91427', '38.91538', '38.91458',
         '38.92239', '38.93222', '38.90842',
         '38.91931', '38.93260', '38.91368',
         '38.88516', '38.921894', '38.93206',
         '38.91275'],
    lon=['-77.02827', '-77.02013', '-77.03155',
         '-77.04227', '-77.02854', '-77.02419',
         '-77.02518', '-77.03304', '-77.04509',
         '-76.99656', '-77.042438', '-77.02821',
         '-77.01239'],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9
    ),
    text=["Truck 1", "Truck 2", "Truck 3",
          "Truck 4", "Truck 5", "Truck 6",
          "Truck 7", "Truck 8", "Truck 9",
          "Truck 10", "Truck 11", "Truck 12",
          "Truck 13"],
))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken='pk.eyJ1IjoiamFrb2JzY2hhYWwiLCJhIjoiY2tiMWVqYnYwMDEyNDJ5bWF3YWhnMTFnNCJ9.KitYnq2a645C15FwvFdqAw',
        bearing=0,
        center=dict(
            lat=38.92,
            lon=-77.07
        ),
        pitch=0,
        zoom=10,
        style='mapbox://styles/jakobschaal/ckb1ekfv005681iqlj9tery0v',
    ),
)

###Kalender###

calendar.setfirstweekday(0)
w_days = 'Sun Mon Tue Wed Thu Fri Sat'.split()
m_names = '''
January February March April
May June July August
September October November December'''.split()


class MplCalendar(object):

    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.cal = calendar.monthcalendar(year, month)
        # monthcalendar creates a list of lists for each week
        # Save the events data in the same format
        self.events = [[[] for day in week] for week in self.cal]

    def _monthday_to_index(self, day):
        for week_n, week in enumerate(self.cal):
            try:
                i = week.index(day)
                return week_n, i
            except ValueError:
                pass
        # couldn't find the day
        raise ValueError("There aren't {} days in the month".format(day))

    def add_event(self, day, event_str):
        week, w_day = self._monthday_to_index(day)
        self.events[week][w_day].append(event_str)

    def show(self):
        ##create calendar
        f, axs = plt.subplots(len(self.cal), 7, sharex=True, sharey=True)
        for week, ax_row in enumerate(axs):
            for week_day, ax in enumerate(ax_row):
                ax.set_xticks([])
                ax.set_yticks([])
                if self.cal[week][week_day] != 0:
                    ax.text(.02, .98,
                            str(self.cal[week][week_day]),
                            verticalalignment='top',
                            horizontalalignment='left')
                contents = "\n".join(self.events[week][week_day])
                ax.text(.03, .85, contents,
                        verticalalignment='top',
                        horizontalalignment='left',
                        fontsize=9)

        # use the titles of the first row as the weekdays
        for n, day in enumerate(w_days):
            axs[0][n].set_title(day)

        # Place subplots in a close grid
        f.subplots_adjust(hspace=0)
        f.subplots_adjust(wspace=0)
        f.suptitle(m_names[self.month] + ' ' + str(self.year),
                   fontsize=20, fontweight='bold')

    plt.show()


plt = go.Figure(plt.show())

layout = html.Div([

    # Tab-Layout

    dcc.Tabs([

        # Downtimes View

        dcc.Tab(label='Downtimes', children=[

#################Row 1###########################

            dbc.Row([

                dbc.Col([
                    dbc.Row(
                        html.Div(
                            html.H2('Vehicle Downtimes'),
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=pie1)),
                        dbc.Col(dash_table.DataTable(
                            data=fleet_data.to_dict('records'),
                            # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                            columns=[{'name': i, 'id': i} for i in fleet_data.loc[:, ['vid', 'vehicle_class']]],
                            style_cell={'textAlign': 'left'},
                            style_cell_conditional=[

                            ]), ),
                    ]),
                ], width=True),

                dbc.Col(html.Div([
                    html.Div([
                        html.Div(
                            html.H2('Accidents'),
                            style={'text-align': 'center'}
                        ),
                        html.Div(
                            dcc.Graph(figure=fig),
                        ),
                    ]),

                ]), width=True),

            ]),

#################Row 2###########################

            dbc.Row([

                dbc.Col([
                    dbc.Row(
                        html.Div(
                            html.H2('Need for Maintenance'),
                            style={'text-align': 'center'}
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=pie2)),
                        dbc.Col(dash_table.DataTable(
                            data=fleet_data.to_dict('records'),
                            # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                            columns=[{'name': i, 'id': i} for i in fleet_data.loc[:, ['vid', 'vehicle_class']]],
                            style_cell={'textAlign': 'left'},
                            style_cell_conditional=[

                            ]), ),
                    ]),
                ], width=True),

                dbc.Col([
                    dbc.Row(
                        html.Div(
                            html.H2('Accident Probability'),
                            style={'text-align': 'center'}
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(dcc.Graph(figure=pie3)),
                        dbc.Col(dash_table.DataTable(
                            data=fleet_data.to_dict('records'),
                            # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                            columns=[{'name': i, 'id': i} for i in fleet_data.loc[:, ['vid', 'vehicle_class']]],
                            style_cell={'textAlign': 'left'},
                            style_cell_conditional=[

                            ]), ),
                    ]),
                ], width=True),

            ]),



            # Row 3 - Truck / Driver information

            # Overstepping speed limit table
            html.Div(
                dash_table.DataTable(
                    data=fleet_data.to_dict('records'),
                    # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                    columns=[{'name': i, 'id': i} for i in fleet_data.loc[:, ['vid', 'vehicle_class']]],
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[

                    ]),
                style={'width': '20%', 'display': 'inline-block'}),

            # Oldest Vehicles table
            html.Div(
                dash_table.DataTable(
                    data=fleet_data.to_dict('records'),
                    # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                    columns=[{'name': i, 'id': i} for i in fleet_data.loc[:, ['vid', 'vehicle_class']]],
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[

                    ]),
                style={'width': '20%', 'display': 'inline-block'}),

            # Excessive speeding table
            html.Div(
                dash_table.DataTable(
                    data=fleet_data.to_dict('records'),
                    # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                    columns=[{'name': i, 'id': i} for i in fleet_data.loc[:, ['vid', 'vehicle_class']]],
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[

                    ]),
                style={'width': '20%', 'display': 'inline-block'}),

            # Excessive acceleration table
            html.Div(
                dash_table.DataTable(
                    data=fleet_data.to_dict('records'),
                    # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                    columns=[{'name': i, 'id': i} for i in fleet_data.loc[:, ['vid', 'vehicle_class']]],
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[

                    ]),
                style={'width': '20%', 'display': 'inline-block'}),

            # Excessive breaking table
            html.Div(
                dash_table.DataTable(
                    data=fleet_data.to_dict('records'),
                    # columns=[{'id': c, 'name': c} for c in fleet_data.columns],
                    columns=[{'name': i, 'id': i} for i in fleet_data.loc[:, ['vid', 'vehicle_class']]],
                    style_cell={'textAlign': 'left'},
                    style_cell_conditional=[

                    ]),
                style={'width': '20%', 'display': 'inline-block'}),

        ]),

        # Maintenance Calendar View
        dcc.Tab(label='Maintenance Calendar', children=[
            dcc.Graph(figure=plt)

        ]),

        # Fleet location map view
        dcc.Tab(label='Realtime Map', children=[

            dcc.Graph(figure=fig),

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

        ]),
    ])
])
