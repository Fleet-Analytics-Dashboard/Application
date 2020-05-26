import dash_core_components as dcc
import dash_html_components as html

page_3_layout = html.Div([
    html.H1('Downtimes'),
    html.Br(),
    dcc.Link('Go to to overview', href='/'),
    html.Br(),
    dcc.Link('Go to to controlling view ', href='/page-2'),
    html.Br(),
    dcc.Link('Go to downtimes view', href='/page-3'),
    html.Br(),
    dcc.Link('Go to vehicles tables view', href='/page-4'),
    html.Br(),
    html.Br(),
    html.Div(id='page-3-content'),
    dcc.RadioItems(
        id='page-3-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    )])
