import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from frontend.pages import overview, controlling, downtimes, vehiclestables

app = dash.Dash()

app.config.suppress_callback_exceptions = True

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

# Routing: index page callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return overview.page_layout
    elif pathname == '/controlling':
        return controlling.page_layout
    elif pathname == '/downtimes':
        return downtimes.page_layout
    elif pathname == '/vehicles-tables':
        return vehiclestables.page_layout
    else:
        return '404'

# Server
if __name__ == '__main__':
    app.run_server(debug=True)
