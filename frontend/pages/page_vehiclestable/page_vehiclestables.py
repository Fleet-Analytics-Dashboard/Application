import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
from page_vehiclestable import table1


app = dash.Dash()

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.H1('Dash Tabs component demo'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])



tab_2_layout = html.Div([
    html.H1('Page 2'),
    html.Div(dash_table.DataTable(
            id='table-2',
            data=fleet_data.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df_vehicle_table1.loc[:,['vehicle_class']]
                     ],
            page_current=0,
            page_size=20,
            page_action='custom',

            filter_action='custom',
            filter_query='',

            sort_action='custom',
            sort_mode='multi',
            sort_by=[],

            style_cell={'textAlign': 'left'},
            style_cell_conditional=[

            ]),
            style={'width': '20%', 'display': 'inline-block', 'overflowX': 'scroll'}),
])


#tab callback
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab_1_layout
    elif tab == 'tab-2-example':
        return tab_2_layout



if __name__ == '__main__':
    app.run_server(debug=True, port=8055)