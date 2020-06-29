import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
from apps import vehiclestables, downtimes, controlling, overview


application = flask.Flask(__name__)
application = dash.Dash(__name__, server=application, url_base_pathname='/', suppress_callback_exceptions=True)

# navigation
application.layout = html.Div([
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


# routing based on navigation
@application.callback(Output('page-content', 'children'),
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


# This is used when running locally only
if __name__ == '__main__':
    application.run_server(debug=True, port=8080)
