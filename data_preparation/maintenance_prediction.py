import pandas as pd


def get_sensor_data(d_df):
    # take realistic variables and define a threshold for malfunction recognised by a sesor

    # 'maximum_rolling_power_density_demand' for tire sensor and 310 as threshold
    d_df['tire_sensor'] = 0
    d_df.loc[d_df['maximum_rolling_power_density_demand'] >= 310, ['tire_sensor']] = 1

    # 'maximum_kinetic_power_density_demand' for engine sensor and 60
    d_df['engine_sensor'] = 0
    d_df.loc[d_df['maximum_kinetic_power_density_demand'] >= 60, ['engine_sensor']] = 1

    # 'max_deceleration_event_duration' for break sensor and 1000 as threshold
    d_df['break_sensor'] = 0
    d_df.loc[d_df['max_deceleration_event_duration'] >= 1200, ['break_sensor']] = 1

    # define a maintenance need that alerts maintenance if 2 or more sensors show a problem
    d_df['maintenance_need'] = 0
    d_df.loc[(d_df['break_sensor']+d_df['engine_sensor']+d_df['tire_sensor']) >= 2, ['maintenance_need']] = 1

    return d_df


def predict_maintenance(d_df, v_df):

    return d_df


# def calculate_maintenance(dist, decel):
#     # Maintenance interval is estimated 46.600 miles
#     # calculate depending on deceleration threshold of -13 ft per second squared
#     if decel <= -13:
#         result = ((dist/46600)*100)+abs(decel*0.0008)
#     else:
#         result = (dist/46600)*100
#
#     return result
#
#
# def maintenance_increase(df):
#     lst = []
#     # iterate over Dataframe and calculate maintenance for each entry
#     for index, row in df.iterrows():
#         lst.append(calculate_maintenance(row['distance_total'], row['max_deceleration_ft_per_second_squared']))
#     df['maintenance_increase'] = lst
#
#     return df
#
#
# def sum_vehicle_maintenance(df, vehicle_df):
#     sum_dic = {}
#     # ad maintenance increas for each row to dict where the key represents the vid
#     for index, row in df.iterrows():
#         if int(row['vid']) in sum_dic.keys():
#             sum_dic[int(row['vid'])] += row['maintenance_increase']
#         else:
#             sum_dic[int(row['vid'])] = row['maintenance_increase']
#     # ad a column with the value that needs to be added
#     vehicle_df['maintenance_add'] = vehicle_df['vid'].map(sum_dic)
#     vehicle_df['maintenance'] = vehicle_df['maintenance'] + vehicle_df['maintenance_add']
#     vehicle_df = vehicle_df.drop('maintenance_add', axis=1)
#
#     return vehicle_df