#Todo -
import pandas as pd

def calculate_maintenance(dist, decel):
    # Maintenance interval is estimated 46.600 miles
    # calculate depending on deceleration threshold of -13 ft per second squared
    if decel <= -13:
        result = ((dist/46600)*100)+abs(decel*0.0008)
    else:
        result = (dist/46600)*100

    return result


def maintenance_increase(df):
    lst = []
    # iterate over Dataframe and calculate maintenance for each entry
    for index, row in df.iterrows():
        lst.append(calculate_maintenance(row['distance_total'], row['max_deceleration_ft_per_second_squared']))
    df['maintenance_increase'] = lst

    return df


def sum_vehicle_maintenance(df, vehicle_df):
    sum_dic = {}
    # ad maintenance increas for each row to dict where the key represents the vid
    for index, row in df.iterrows():
        if int(row['vid']) in sum_dic.keys():
            sum_dic[int(row['vid'])] += row['maintenance_increase']
        else:
            sum_dic[int(row['vid'])] = row['maintenance_increase']
    # ad a column with the value that needs to be added
    vehicle_df['maintenance_add'] = vehicle_df['vid'].map(sum_dic)
    vehicle_df['maintenance'] = vehicle_df['maintenance'] + vehicle_df['maintenance_add']
    vehicle_df = vehicle_df.drop('maintenance_add', axis=1)

    return vehicle_df


def predict_maintenance(d_df, v_df):

    return d_df
