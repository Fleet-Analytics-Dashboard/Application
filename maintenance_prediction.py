#Todo - add maintenance summ to dataframe
from data_cleaning import new, v_df, pd


def calculate_maintenance(dist, decel):
    # Maintenance interval is estimated 46.600 miles
    # calculate depending on deceleration threshold of -13 ft per second squared
    if decel <= -13:
        result = ((dist/46600)*100)+abs(decel*0.0008)
    else:
        result = (dist/46600)*100

    return result


# iterate over Dataframe and calculate maintenance for each entry
lst = []
for index, row in new.iterrows():
    lst.append(calculate_maintenance(row['distance_total'], row['max_deceleration_ft_per_second_squared']))
new['maintenance_increase'] = lst

sum_lst = []
for index, row in v_df.iterrows():
    v_sum = new.loc[new['vid'] == row['vid']]
    sum_lst.append(v_sum['maintenance_increase'].sum(axis=0))

print(sum_lst)
