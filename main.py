import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate
import collections
from plotly import graph_objs as go

from apps import vehiclestables, downtimes, controlling, home
from apps.downtimes import df_vehicle_data, df_maintenance_status
from apps.vehiclestables import df_group_vehicle_class, df_vehicle, df_driver, df_group_driver
from apps.controlling import *

conn = connect()
sql = "select * from vehicle_data;"
df_vehicle_data = pd.read_sql_query(sql, conn)
conn = None

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
            html.A([
                html.Img(src=app.get_asset_url('fleetboard_logo.jpg'), style={'height': '36px'}),
                html.Span('Fleetboard', className='logo-text'),
            ], className='align-self-center', href='/'),

            dbc.Nav(
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
        ],
        className='header align-self-center'
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
        return controlling.layout
    elif pathname == '/downtimes':
        return downtimes.layout
    elif pathname == '/vehicles-overview':
        return home.layout
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


# @app.callback(
#     Output('map-container', 'figure'),
#     [Input('vehicle-table-overview', 'data')])
# def create_downtimes_table(selected_status):
#     if selected_status is not None:
#         filtered_df = df_vehicle_data[df_vehicle_data["licence_plate"].isin(selected_status)]
#         data = filtered_df.to_dict("records")
#     return data


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
        figure = px.bar(df_group_vehicle_class, x="Vehicle Typ", y="Amount",
                        hover_data=['Transport Goal'], color='Transport Goal')

    if selected_column == 'vic_type':
        figure = px.bar(df_group_vehicle_class, x="Vehicle Typ", y="Amount",
                        hover_data=['Typ'], color='Typ')

    if selected_column == 'person':
        figure = px.bar(df_group_driver, x="Name", y="Amount",
                        hover_data=['License Plate'], color='License Plate')
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
        'data': [y for y in aggregation.values()]
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


# server
if __name__ == '__main__':
    app.run_server(debug=True)
