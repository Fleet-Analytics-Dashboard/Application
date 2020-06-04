import dash_core_components as dcc
import dash_html_components as html
from app import app
from frontend.pages import page_overview, page_controlling, page_downtimes, page_vehiclestables

index_page = html.Div([
    dcc.Link('Go to page overview', href='/pages/page_controlling'),
    html.Br(),
    dcc.Link('Go to page controlling', href='/pages/page_controlling'),
    html.Br(),
    dcc.Link('Go to page downtimes', href='/pages/page_controlling'),
    html.Br(),
    dcc.Link('Go to page vehicles table', href='/pages/page_controlling'),
])