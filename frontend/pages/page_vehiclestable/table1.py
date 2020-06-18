import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import dash

#data
fleet_data = pd.read_csv('../../../batch-data/cleaned-data-for-fleet-dna.csv')
df_vehicle_table1 = fleet_data[['vid', 'vehicle_class', 'vocation', 'vehicel_type', 'drivetrain_type', 'fuel_type' ,'day_id', 'driving_data_duration_hrs_no_zero', 'max_speed', 'driving_average_speed_no_zero', 'seconds_at_speed_zero', 'driving_time_seconds', 'percent_time_at_speed_zero', 'total_number_of_acceleration_events', 'total_number_of_deceleration_events', 'acceleration_events_per_mile', 'deceleration_events_per_mile', 'average_acceleration_event_duration', 'average_deceleration_event_duration', 'max_elevation', 'min_elevation', 'mean_elevation', 'delta_elevation', 'total_elevation_gained', 'total_elevation_lost', 'average_descending_rate']].copy()
df_vehicle_table2 = fleet_data[['vid']].copy()

#rounded data
df_vehicle_table1 = df_vehicle_table1.round(decimals=2)


tab_1_layout = html.Div([
    html.H1('Page 1'),
    html.Div(dash_table.DataTable(
            id='table-1',
            data=fleet_data.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df_vehicle_table1.loc[:]
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
    html.Div(
        id='table-paging-with-graph-container',
        className="five columns"
    )
]),


#filter table 1

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part


                return name, operator_type[0].strip(), value

    return [None] * 3


