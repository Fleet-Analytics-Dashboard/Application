import plotly.express as px
from dash.exceptions import PreventUpdate
import collections
from dateutil.relativedelta import *
from dash.dependencies import Input, Output
from datetime import datetime, timedelta

from apps import downtimes, home, vehicles_overview
from apps.downtimes import *
from apps.home import *

# get data from database
# conn = connect()
# sql = "select * from vehicle_data;"
# df_vehicle_data = pd.read_sql_query(sql, conn)
# sql = "select * from driving_data;"
# fleet_data = pd.read_sql_query(sql, conn)
# sql = "select * from driver_names;"
# dfnames = pd.read_sql_query(sql, conn)
# conn = None

# get data from csv files
df_vehicle_data = pd.read_csv('csv_data_files/vehicle_data.csv')
fleet_data = pd.read_csv('csv_data_files/driving_data.csv')
dfnames = pd.read_csv('csv_data_files/names.csv')

# Rounded data
fleet_data_rounded = fleet_data.round(decimals=2)

df_vehicle = df_vehicle_data[['vid','licence_plate', 'vehicle_class',   'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type']].copy()
df_vehicle = pd.merge(df_vehicle, fleet_data, how='left', on='vid')
df_vehicle = df_vehicle[['vid', 'vehicle_class', 'licence_plate', 'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type', 'pid']]

df_vehicle_class = df_vehicle_data[['vehicle_class', 'vid', 'fuel_type', 'vocation', 'vehicle_type']].copy()
df_vehicle_class = df_vehicle_class.drop_duplicates(subset=None, keep='first', inplace=False)

df_group_vehicle_class = df_vehicle_class.groupby(['vehicle_class', 'vocation', 'vehicle_type'])['vid'].count().reset_index()
df_group_vehicle_class.columns = (["Vehicle Class", 'Transport Goal', 'Typ', "Amount"])

df_driver = pd.merge(df_vehicle, dfnames, how='left', on='pid').copy()
df_driver = df_driver.drop(columns=['ip_address'])
df_driver = df_driver.drop_duplicates(subset=None, keep='first', inplace=False)


df_group_driver = df_driver.groupby(['licence_plate', 'last_name'])['pid'].count().reset_index()
df_group_driver.columns = (['License Plate', 'Name', 'Amount'])

external_scripts = [
    {'src': 'https://code.jquery.com/jquery-3.3.1.min.js'},
    {'src': 'https://code.jquery.com/ui/1.12.1/jquery-ui.min.js'}
]

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_scripts=external_scripts,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
                )

# colors theme
colors = ['rgb(66,234,221)', 'rgb(7,130,130)', 'rgb(171,209,201)', 'rgb(151,179,208)', 'rgb(118,82,139)',
          'rgb(173,239,209)', 'rgb(96,96,96)', 'rgb(214,65,97)']

# navigation
app.layout = html.Div([

    dcc.Location(id='url', refresh=False),

    html.Div(
        [
            html.Span([
                html.A([
                    html.Img(src=app.get_asset_url('fleetboard_logo.jpg'), style={'height': '36px'}),
                    html.Span('Fleetboard', className='logo-text'),
                ], className='logo-link align-self-center', href='/'),

                html.Span(dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="/", id='-link')),
                        dbc.NavItem(dbc.NavLink("Downtimes", href="/downtimes", id='downtimes-link')),
                        dbc.NavItem(
                            dbc.NavLink("Vehicle Overview", href="/vehicles-overview", id='vehicles-overview-link')),
                    ],
                    pills=True,
                    className='nav-menu',
                    id='navbar',
                ),
                )
            ], className="logo-and-nav"),

            # Date Picker
            html.Span(
                [
                    dcc.DatePickerRange(
                        id='controlling-date-picker-range',
                        min_date_allowed=datetime(1995, 8, 5),
                        max_date_allowed=datetime(2020, 6, 19),
                        initial_visible_month=datetime(2020, 6, 5),
                        end_date=datetime(2020, 6, 5).date()
                    ),
                    html.Span(id='output-container-date-picker-range')
                ], className='data-picker',
            ),
        ],
        className='header align-self-center justify-content-between'
    ),

    # page content from respective site will be loaded via this id
    html.Div(id='page-content'),
])

server = app.server


# routing based on navigation
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/downtimes':
        return downtimes.layout
    elif pathname == '/vehicles-overview':
        return vehicles_overview.layout
    else:
        return '404'


#####Callback navigation active page########


@app.callback(Output('-link', 'active'), [Input('url', 'pathname')])
def set_page_1_active(pathname):
    if pathname == '/':
        active = True
        return active


@app.callback(Output('downtimes-link', 'active'), [Input('url', 'pathname')])
def set_page_1_active(pathname):
    if pathname == '/downtimes':
        active = True
        return active


@app.callback(Output('vehicles-overview-link', 'active'), [Input('url', 'pathname')])
def set_page_1_active(pathname):
    if pathname == '/vehicles-overview':
        active = True
        return active


# Overview view


# Overview table to map filter

@app.callback(
    Output('map', 'figure'),
    [Input('vehicle-table-overview', 'data')])
def create_downtimes_table(selected_status):
    if selected_status is not None:
        filtered_df = df_vehicle_data[df_vehicle_data.isin(selected_status)]
        # data = filtered_df.to_dict("records")

        fleet_lat = filtered_df.position_latitude
        fleet_lon = filtered_df.position_longitude
        fleet_vid = filtered_df.vid
        fleet_status = filtered_df.vehicle_status

        fig = go.Figure(
            px.scatter_mapbox(filtered_df, text="licence_plate", lat=fleet_lat, lon=fleet_lon,
                              color="vehicle_status",
                              custom_data=['licence_plate'], color_continuous_scale=px.colors.cyclical.IceFire,
                              size_max=20, zoom=10))

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            autosize=True,
            clickmode='event+select',
            legend=dict(
                x=0,
                y=1,
                font=dict(
                    family="Courier",
                    size=12,
                    color="black"
                ),
                bgcolor="LightSteelBlue",
                bordercolor="Black",
                borderwidth=2
            ),
            hovermode='closest',
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiamFrb2JzY2hhYWwiLCJhIjoiY2tiMWVqYnYwMDEyNDJ5bWF3YWhnMTFnNCJ9.KitYnq2a645C15FwvFdqAw',
                bearing=0,
                center=dict(
                    lat=38.92,
                    lon=-100.07
                ),
                pitch=0,
                zoom=5,
                # style='mapbox://styles/jakobschaal/ckb1ekfv005681iqlj9tery0v',
                style='mapbox://styles/jakobschaal/ckcv9t67c097q1imzfqprsks9',
            ),
        )

    return fig



# Table function


@app.callback(
    Output('vehicle-table2', 'data'),
    [Input('vocation-dropdown-table', 'value')])
def create_table(selected_vocation):
    if selected_vocation is not None:
        filtered_df = df_driver[df_driver["vocation"].isin(selected_vocation)]
        data = filtered_df.to_dict("records")
    return data


@app.callback(
    Output('graph', 'figure'),
    [Input('graph-filter', 'value')])
def create_graph(selected_column):
    if selected_column == 'Voc':
        figure = px.bar(df_group_vehicle_class, x="Vehicle Class", y="Amount",
                        hover_data=['Transport Goal'], color='Transport Goal')

    if selected_column == 'vic_type':
        figure = px.bar(df_group_vehicle_class, x="Vehicle Class", y="Amount",
                        hover_data=['Typ'], color='Typ')

    if selected_column == 'person':
        figure = px.bar(df_group_driver, x="Name", y='Amount', hover_data=['License Plate'], color='License Plate')
        # figure.update_yaxes(title_text="Amount")
        # figure.update_xaxes(title_text="Name")

    return figure


####Callback radio buttons downtimes-table###########

@app.callback(
    Output('downtime_table', 'data'),
    [Input('page-downtimes-radios-1', 'value')])
def create_downtimes_table(selected_status):
    if selected_status is None:
        data = selected_status.to_dict("records")

    else:
        filtered_df = df_vehicle_data[df_vehicle_data["vehicle_status"].isin(selected_status)]
        data = filtered_df.to_dict("records")

    return data


####Callback costs dropdown controlling-table###########
@app.callback(
    Output('id-dropdown', 'options'),
    [Input('dropdown-category', 'value')]
)
def update_dropdown(option):
    return [{'label': i, 'value': i} for i in dropdown_options[option]]


#### Callback filter costs chart by vehicle id############
@app.callback(Output('memory-output', 'data'),
              [Input('id-dropdown', 'value')])
def filter_id(id_selected):
    if not id_selected:
        return df_cost_data.to_dict('records')
    filtered = df_cost_data.query('vid in @id_selected')
    return filtered.to_dict('records')


@app.callback(
    Output('costs-chart', 'figure'),
    [Input('memory-output', 'data'),
     Input('memory-field', 'value')])
def on_data_set_graph(data, field):
    if data is None:
        raise PreventUpdate

    aggregation = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )

    for row in data:
        a = aggregation[row['vid']]
        a['name'] = row['vid']
        a['mode'] = 'lines+markers'

        a['x'].append(row['month'])
        a['y'].append(row[field])

    return {
        'data': [y for y in aggregation.values()],
    }


####Callback checkboxes controlling-table###########

@app.callback(
    Output('table-for-capacity', 'data'),
    [Input('page-controlling-radios-3', 'value')])
def create_capacity_table(selected_status):
    if selected_status is None:
        data = selected_status.to_dict("records")

    else:
        filtered_df = df_vehicle_data[df_vehicle_data["vehicle_status"].isin(selected_status)]
        data = filtered_df.to_dict("records")

    return data


####Callback radio buttons maintenance-status-table###########

@app.callback(
    Output('maintenance_table', 'data'),
    [Input('page-downtimes-radios-2', 'value')])
def create_maintenance_table(selected_status):
    if selected_status is None:
        data = selected_status.to_dict("records")

    else:
        filtered_df = df_maintenance_status[df_maintenance_status["scheduled_maintenance"].isin(selected_status)]
        data = filtered_df.to_dict("records")

    return data


####Callback radio buttons accident-probability-table###########

@app.callback(
    Output('table-accident-probability', 'data'),
    [Input('page-downtimes-radios-3', 'value')])
def create_maintenance_table(selected_status):
    if selected_status is None:
        data = selected_status.to_dict("records")

    else:
        filtered_df = df_accident_probability[df_accident_probability["accident_probability"].isin(selected_status)]
        data = filtered_df.to_dict("records")

    return data


####Callback filter maintenance calendar based on license plate####
@app.callback(Output('heatmap', 'figure'),
              [Input('heatmap-dropdown', 'value')])
def create_heat_map(selected_licence_plate):
    today = datetime.today()
    year, week_num, day_of_week = today.isocalendar()
    # d1 represents starting day (yyyy-mm-dd) and d2 end day
    # d1 = today - datetime.date.month

    d1 = today + relativedelta(weeks=-26)

    d2 = today + relativedelta(weeks=+26)

    delta = d2 - d1

    dates_in_year = [d1 + timedelta(i) for i in
                     range(delta.days + 1)]  # gives me a list with datetimes for each day a year
    # weekdays_in_year = [i.weekday() for i in dates_in_year] #gives [0,1,2,3,4,5,6,0,1,2,3,4,5,6,…] (ticktext in xaxis dict translates this to weekdays
    weeknumber_of_dates = [i.strftime("%G cw%V")[2:] for i in
                           dates_in_year]  # gives [1,1,1,1,1,1,1,2,2,2,2,2,2,2,…] name is self-explanatory
    weeknumber_of_dates = list(dict.fromkeys(weeknumber_of_dates))
    # create numpy array for the maintenance dates for each vehicle
    z = np.zeros(shape=(len(df_vehicle_data['vid']), len(weeknumber_of_dates)), dtype=float)

    # mark zells of today
    z[:, 26] = 0.25

    # set status of vehicles which are currently in maintenance to 1
    today_maintenance = df_vehicle_data.index[df_vehicle_data['vehicle_status'] == 'maintenance'].tolist()
    for i in today_maintenance:
        z[i][26] = 1

    # set status for scheduled maintenance
    for index, row in df_vehicle_data.iterrows():
        z[index][26 + int(row['scheduled_maintenance'])] = 1

    # set status for previous maintenance
    np.random.seed(1)
    random_date = np.random.randint(0, 23, size=len(df_vehicle_data.vid))
    index = 0
    for i in random_date:
        z[index][i] = 1
        index += 1

    # set status for scheduled maintenance
    for index, row in df_vehicle_data.iterrows():
        if row.predicted_weeks_until_maintenance < 30:
            z[index][26 + int(row['predicted_weeks_until_maintenance'])] = 0.5

    # text = [str(i) for i in dates_in_year] #gives something like list of strings like ‘2018-01-25’ for each date. Used in data trace to make good hovertext.
    # 4cc417 green #347c17 dark green
    colorscale = [[0, '#eeeeee'], [0.25, '#a1a1a1'], [0.5, 'red'], [1, 'rgb(7, 130, 130)']]
    if selected_licence_plate is None:
        data = [
            go.Heatmap(
                x=weeknumber_of_dates,
                y=df_vehicle_data['licence_plate'],
                z=z,
                # text=text,
                # hoverinfo='text',
                xgap=3,  # this
                ygap=3,  # and this is used to make the grid-like apperance
                showscale=False,
                colorscale=colorscale
            )]
        layout = go.Layout(
            height=4000,
            yaxis=dict(
                showline=False, showgrid=False, zeroline=False,
                # tickmode='array',
                ticktext=df_vehicle_data['licence_plate'],
                # tickvals=[0,1,2,3,4,5,6],
            ),
            xaxis=dict(
                showline=False, showgrid=False, zeroline=False, side='top',
            ),
            # font={'size':'10', 'color':'#9e9e9e'},
            plot_bgcolor=('#fff'),
            margin=dict(t=40),
        )
    else:
        filtered_df = df_vehicle_data[df_vehicle_data['licence_plate'] == selected_licence_plate]

        data = [
            go.Heatmap(
                x=weeknumber_of_dates,
                y=filtered_df['licence_plate'],
                z=z,
                # text=text,
                # hoverinfo='text',
                xgap=3,  # this
                ygap=3,  # and this is used to make the grid-like apperance
                showscale=False,
                colorscale=colorscale
            )]

        layout = go.Layout(
            height=300,
            yaxis=dict(
                showline=False, showgrid=False, zeroline=False,
                # tickmode='array',
                ticktext=df_vehicle_data['licence_plate'],
                # tickvals=[0,1,2,3,4,5,6],
            ),
            xaxis=dict(
                showline=False, showgrid=False, zeroline=False, side='top',
            ),
            # font={'size':'10', 'color':'#9e9e9e'},
            plot_bgcolor=('#fff'),
            margin=dict(t=40),
        )

    fig = go.Figure(data=data, layout=layout)
    return fig

# server
if __name__ == '__main__':
    app.run_server(debug=True)
