import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from plotly import graph_objs as go


from apps import vehiclestables, downtimes, controlling, overview
from apps.vehiclestables import df_group_vehicle_class, df_vehicle, df_driver, df_group_driver


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# navigation
app.layout = html.Div([

    dcc.Location(id='url', refresh=False),
    html.H1('Fleetboard'),

    # TODO fix active=True
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Overview", href="/")),
            dbc.NavItem(dbc.NavLink("Controlling", href="/controlling")),
            dbc.NavItem(dbc.NavLink("Downtimes", href="/downtimes")),
            dbc.NavItem(dbc.NavLink("Vehicle Tables", href="/vehicles-tables")),
        ],
        pills=True,
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
        return overview.layout
    elif pathname == '/controlling':
        return controlling.layout
    elif pathname == '/downtimes':
        return downtimes.layout
    elif pathname == '/vehicles-tables':
        return vehiclestables.layout
    else:
        return '404'


# Table function


@app.callback(
    Output('vehicle-table2', 'data'),
    [Input('vocation-dropdown-table', 'value')])
def create_table(selected_vocation):

    if selected_vocation is not None:
         filtered_df = df_driver[df_driver["vocation"].isin(selected_vocation)]
         data=filtered_df.to_dict("records")

    return data


@app.callback(
    Output('graph', 'figure'),
    [Input('graph-filter', 'value')])
def create_graph(selected_column):

    if selected_column == 'Voc':
        figure = px.bar(df_group_vehicle_class, x="Klasse", y="anzahl",
                        hover_data=['Vocation'], color='Vocation')

    if selected_column == 'vic_type':
        figure = px.bar(df_group_vehicle_class, x="Klasse", y="anzahl",
                        hover_data=['Typ'], color='Typ')

    if selected_column == 'person':
        figure = px.bar(df_group_driver, x="Name", y="anzahl",
                        hover_data=['Nummer'], color='Nummer')

    return figure

# server
if __name__ == '__main__':
    app.run_server(debug=True)
