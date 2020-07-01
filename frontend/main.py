import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from frontend.pages import page_overview, page_controlling, page_downtimes
from frontend.pages.page_vehiclestable import page_vehiclestables

app = dash.Dash()

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Routing
## Page overview
@app.callback(dash.dependencies.Output('overview-content', 'children'),
              [dash.dependencies.Input('overview-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


## Page controlling view
@app.callback(Output('controlling-content', 'children'),
              [Input('controlling-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


## Page downtimes view
@app.callback(Output('downtimes-content', 'children'),
              [Input('downtimes-radios', 'value')])
def page_3_radios(value):
    return 'You have selected "{}"'.format(value)


## Page vehicles tables view
@app.callback(Output('vehicles-tables-content', 'children'),
              [Input('vehicles-tables-radios', 'value')])
def page_4_radios(value):
    return 'You have selected "{}"'.format(value)


# Index Page callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return page_overview.page_layout
    elif pathname == '/controlling':
        return page_controlling.page_layout
    elif pathname == '/downtimes':
        return page_downtimes.page_layout
    elif pathname == '/vehicles-tables':
        return page_vehiclestables.page_layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
