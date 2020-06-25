import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from app import app
import dash_core_components as dcc

fleet_data = pd.read_csv('cleaned-data-for-fleet-dna_v3.csv')
#rounded data
fleet_data_rounded = fleet_data.round(decimals=2)

df_vehicle_table1 = fleet_data[['vid', 'vehicle_class', 'vocation', 'vehicel_type', 'drivetrain_type', 'fuel_type' ,'day_id', 'driving_data_duration_hrs_no_zero', 'max_speed', 'driving_average_speed_no_zero', 'seconds_at_speed_zero', 'driving_time_seconds', 'percent_time_at_speed_zero', 'total_number_of_acceleration_events', 'total_number_of_deceleration_events', 'acceleration_events_per_mile', 'deceleration_events_per_mile', 'average_acceleration_event_duration', 'average_deceleration_event_duration', 'max_elevation', 'min_elevation', 'mean_elevation', 'delta_elevation', 'total_elevation_gained', 'total_elevation_lost', 'average_descending_rate']].copy()
df_vehicle_table2 = fleet_data[['vid']].copy()

df_vehicle_table1['id'] = df_vehicle_table1['vid']
df_vehicle_table1.set_index('vid', inplace=True, drop=False)

layout = html.Div(children=[
    html.H1(children='Vehicles Tables'),

    html.Div(children='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut '
                      'labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco '
                      'laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in '
                      'voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat '
                      'non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'),
    html.Div(dash_table.DataTable(
                    id='datatable-interactivity',
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True} for i in df_vehicle_table1.columns
                    ],
                    data=df_vehicle_table1.to_dict('records'),
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                    page_size=10,
                    style_table={'overflowX': 'scroll'}

    ),
    ),
    html.Div(id='datatable-interactivity-container'),

    html.Div(dash_table.DataTable(
                    id='datatable-interactivity',
                    columns=[
                        {"name": i, "id": i, "deletable": True, "selectable": True} for i in df_vehicle_table2.columns
                    ],
                    data=df_vehicle_table2.to_dict('records'),
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                    page_size=10,
                    style_table={'overflowX': 'scroll'}
    ),

    ),
]),


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-row-ids-container', 'children'),
    [Input('datatable-row-ids', 'derived_virtual_row_ids'),
     Input('datatable-row-ids', 'selected_row_ids'),
     Input('datatable-row-ids', 'active_cell')])
def update_graphs(row_ids, selected_row_ids, active_cell):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.

    selected_id_set = set(selected_row_ids or [])

    if row_ids is None:
        dff = df_vehicle_table1
        # pandas Series works enough like a list for this to be OK
        row_ids = df_vehicle_table1['vid']
    else:
        dff = df_vehicle_table1.loc[row_ids]

    active_row_id = active_cell['row_id'] if active_cell else None

    colors = ['#FF69B4' if id == active_row_id
              else '#7FDBFF' if id in selected_id_set
    else '#0074D9'
              for id in row_ids]

    return [
        dcc.Graph(
            id='vid' + '--row-ids',
            figure={
                'data': [
                    {
                        'x': dff['vid'],
                        'y': dff['vid'],
                        'type': 'bar',
                        'marker': {'color': colors},
                    }
                ],
                'layout': {
                    'xaxis': {'automargin': True},
                    'yaxis': {
                        'automargin': True,
                        'title': {'text': column}
                    },
                    'height': 250,
                    'margin': {'t': 10, 'l': 10, 'r': 10},
                },
            },
        )

    ]
