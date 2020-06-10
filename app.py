import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from apps import vehiclestables, downtimes, controlling, overview

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    html.H1('Navigation'),
    html.Br(),
    dcc.Link('Overview', href='/'),
    html.Br(),
    dcc.Link('Controlling ', href='/controlling'),
    html.Br(),
    dcc.Link('Downtimes', href='/downtimes'),
    html.Br(),
    dcc.Link('Vehicles tables', href='/vehicles-tables'),
    html.Br(),
    html.Br(),
    # page content from respective site will be loaded via this id
    html.Div(id='page-content')
])

server = app.server

# Routing: index page callback
@app.callback(Output('page-content', 'children'),
                   [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return overview.overview_layout
    elif pathname == '/controlling':
        return controlling.controlling_layout
    elif pathname == '/downtimes':
        return downtimes.donwtimes_layout
    elif pathname == '/vehicles-tables':
        return vehiclestables.vehiclestabes_layout
    else:
        return '404'


# server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8080)
