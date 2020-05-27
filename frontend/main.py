import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from frontend.pages import page_1, page_2, page_3, page_4

app = dash.Dash()

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Routing
## Page overview
@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


## Page controlling view
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


## Page downtimes view
@app.callback(Output('page-3-content', 'children'),
              [Input('page-3-radios', 'value')])
def page_3_radios(value):
    return 'You have selected "{}"'.format(value)


## Page vehicles tables view
@app.callback(Output('page-4-content', 'children'),
              [Input('page-4-radios', 'value')])
def page_4_radios(value):
    return 'You have selected "{}"'.format(value)


# Index Page callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return page_1.page_1_layout
    elif pathname == '/page-2':
        return page_2.page_2_layout
    elif pathname == '/page-3':
        return page_3.page_3_layout
    elif pathname == '/page-4':
        return page_4.page_4_layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
