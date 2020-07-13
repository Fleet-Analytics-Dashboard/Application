import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table as dt

from apps import vehiclestables, downtimes, controlling, overview
from apps.vehiclestables import df_group_vehicle_class, df_vehicle, df_driver
from apps.downtimes import vehicle_data

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
def make_table(data, output):
    return html.Div(
        [
            dt.DataTable(
                id=output,
                data=data.to_dict('rows'),
                columns=[{'id': c, 'name': c} for c in data.columns],
                selected_rows=[],
                style_cell={'padding': '5px',
                            'whiteSpace': 'no-wrap',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 100,
                            'height': 30,
                            'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'color': 'black'

                },

            ),
        ], className="seven columns", style={'margin-top': '35',
                                             'margin-left': '15',
                                             'border': '1px solid #C6CCD5'}
    )


##########Make downtime table##################

def make_table_downtime(data, output):
    return html.Div(
        [
            dt.DataTable(
                id=output,
                data=data.to_dict('rows'),
                columns=[{'vid': c, 'vehicle_status': c} for c in data.columns],
                selected_rows=[],
                style_cell={'padding': '5px',
                            'whiteSpace': 'no-wrap',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 100,
                            'height': 30,
                            'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'color': 'black'

                },

            ),
        ],
    )


def make_chart(df, x, y, label='Author', size='Size'):
    graph = []
    if size == '':
        s = 15
    else:
        s = df[size]
    graph.append(go.Scatter(
        x=df[x],
        y=df[y],
        mode='markers',
        text=['{}: {}'.format(label, a) for a in df[label]],
        opacity=0.7,
        marker={
            'size': s,
            'line': {'width': 0.5, 'color': 'white'}
        },
        name='X'
    ))

    return graph


# Callbacks and functions
@app.callback(dash.dependencies.Output('memory', 'data'),
              [dash.dependencies.Input('table', 'selected_cells'),
               dash.dependencies.Input('table', 'derived_virtual_data')],
              [dash.dependencies.State('memory', 'data')])
def tab(sel, table, state):
    # to initialize variables when it is None
    if state is None:
        state = {}
    if table is None:
        state['data'] = df_group_vehicle_class.to_dict('records')
        table = [{}]
    else:
        state['data'] = table  # save current table value afer it gets initialized

    # store information of selected rows to retrieve them when back button is clicked
    # information is stored in json format
    #
    if sel:
        if 'vid' in table[0].keys():
            state['vid'] = table[0]['vid']
        if 'vehicle_class' in table[0].keys() and table is not None:
            state['vehicle_class'] = table[0]['vehicle_class']

    return state


@app.callback(
    dash.dependencies.Output('table-box', 'children'),
    [dash.dependencies.Input('filter_x', 'value'),
     dash.dependencies.Input('filter_y', 'value'),
     dash.dependencies.Input('button_chart', 'n_clicks_timestamp'),
     dash.dependencies.Input('back_button', 'n_clicks_timestamp'),
     dash.dependencies.Input('table', 'selected_cells')],
    [dash.dependencies.State('memory', 'data')])
def update_image_src(fx, fy, button, back, selected_cell, current_table):
    if fx == '':
        res = df_group_vehicle_class
    else:
        res = df_vehicle[df_vehicle['vid'] == fx]

    if selected_cell:
        print(current_table)
        if 'Klasse' in current_table['data'][0].keys():
            res = df_vehicle[
                df_vehicle['vehicle_class'] == current_table['data'][list(selected_cell)[0]['row']]['Klasse']]
        if 'pid' in current_table['data'][0].keys():
            res = df_driver[df_driver['pp'] == current_table['data'][list(selected_cell)[0]['row']]['pid']]

    return make_table(res, 'table')


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('filter_x', 'value'),
     dash.dependencies.Input('filter_y', 'value'),
     dash.dependencies.Input('button_chart', 'n_clicks_timestamp'),
     dash.dependencies.Input('back_button', 'n_clicks_timestamp'),
     dash.dependencies.Input('table', 'selected_cells')])
def update_graph(fx, fy, back, selected_cell, current_table):
    if fx == '':
        return {
            'data': [{
                'x': df_group_vehicle_class['Klasse'],
                'y': df_group_vehicle_class['anzahl']
            }]
        }


################### Callback downtimes table####################
# @app.callback(
#     dash.dependencies.Output('downtime_table', 'children'),
#     [dash.dependencies.Input('searchbox_downtime_table', 'value'),
#      ])
#
# def update_downtime_table(value):
#     return
#
#
# @app.callback(
#     Output('downtime_table', 'rows'),
#     [Input('searchbox_downtime_table', 'value'),
#      ])
# def update_selected_row_indices(value):
#     map_aux = vehicle_data.copy()
#
#     # Type filter
#     map_aux = map_aux[map_aux['Type'].isin(value)]
#
#     data = map_aux.to_dict('records')
#     return data

# server
if __name__ == '__main__':
    app.run_server(debug=True)
