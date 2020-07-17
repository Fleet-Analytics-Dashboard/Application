import numpy as np
import pandas as pd


def fuel_cost(v_df, d_df):
    # Simulate Fuel, Insurance, Maintenance Cost per Vehicle
    # select necessary rows and join dataframes to have vehicle and drive information
    # v_df = v_df[['vid', 'vehicle_class', 'fuel_type', 'drivetrain_type']]
    # d_df = d_df[['vid', 'day_id', 'distance_total']]
    df = pd.merge(d_df[['vid', 'day_id', 'distance_total']], v_df[['vid', 'vehicle_class', 'fuel_type', 'drivetrain_type']], how='left', on='vid')

    # Fuel consumption in miles per gallon
    lst = []
    for index, row in df.iterrows():
        if row['vehicle_class'] == 2:
            lst.append(np.random.uniform(9.1, 12.5))
        elif row['vehicle_class'] == 3:
            lst.append(np.random.uniform(8.5, 11.5))
        elif row['vehicle_class'] == 4:
            lst.append(np.random.uniform(8.1, 10.5))
        elif row['vehicle_class'] == 5:
            lst.append(np.random.uniform(7.2, 9.5))
        elif row['vehicle_class'] == 6:
            lst.append(np.random.uniform(6.5, 8.7))
        elif row['vehicle_class'] == 7:
            lst.append(np.random.uniform(5.7, 7.9))
        else:
            lst.append(np.random.uniform(4.9, 7.1))

    # add lst as new column
    d_df['average_consumption'] = lst

    # calculate fuel cost
    d_df['fuel_cost'] = round((2.39 / d_df['average_consumption'] * d_df['distance_total']), 2)

    return d_df


def cost_per_vehicle(v_df, d_df):
    # create new dataframe for cost per vehicle and include vid as key
    vehicle_cost_data = pd.DataFrame()
    sample = pd.DataFrame()

    vehicle_cost_data['vid'] = v_df['vid'].copy()
    sample['vid'] = v_df['vid'].copy()

    d_df['month'] = 0
    # split driving data into months
    d_df.loc[(d_df['day_id'] > 0) & (d_df['day_id'] <= 4), ['month']] = 'jan'
    d_df.loc[(d_df['day_id'] > 4) & (d_df['day_id'] <= 8), ['month']] = 'feb'
    d_df.loc[(d_df['day_id'] > 8) & (d_df['day_id'] <= 12), ['month']] = 'mar'
    d_df.loc[(d_df['day_id'] > 12) & (d_df['day_id'] <= 16), ['month']] = 'apr'
    d_df.loc[(d_df['day_id'] > 16) & (d_df['day_id'] <= 20), ['month']] = 'may'
    d_df.loc[(d_df['day_id'] > 20) & (d_df['day_id'] <= 30), ['month']] = 'jun'
    d_df.loc[(d_df['day_id'] > 30), ['month']] = 'jul'

    grouped = d_df.groupby(d_df.month)
    jan = grouped.get_group('jan')
    feb = grouped.get_group('feb')
    mar = grouped.get_group('mar')
    apr = grouped.get_group('apr')
    may = grouped.get_group('may')
    jun = grouped.get_group('jun')
    jul = grouped.get_group('jul')

    # crate array with dataframes and seperate one with their names for refference in columns
    arr = [jan, feb, mar, apr, may, jun, jul]
    arr_name = ['01_jan', '02_feb', '03_mar', '04_apr', '05_may', '06_jun', '07_jul']

    # summ up fuel cost per vehicle
    i = 0
    sum = {}
    for month in arr:
        # run through each months dataframe
        for index, row in month.iterrows():
            if int(row['vid']) in sum.keys():
                sum[int(row['vid'])] += row['fuel_cost']
            else:
                sum[int(row['vid'])] = row['fuel_cost']
        # ad a column with the value that needs to be added to sample dataframe
        sample['month'] = arr_name[i]
        sample['fuel_cost_total'] = sample['vid'].map(sum)
        i += 1
        # append sample dataframe to vehicle_cost_data dataframe
        if 'month' in vehicle_cost_data.columns:
            vehicle_cost_data = vehicle_cost_data.append(sample)
        else:
            vehicle_cost_data['month'] = sample['month'].copy()
            vehicle_cost_data['fuel_cost_total'] = sample['fuel_cost_total'].copy()

    # replace nan values in fuel cost with 0 before continuing
    vehicle_cost_data.fillna(0, inplace=True)

    # simulate insurance cost in dollar per vehicle, per month with normal distribution around 4000$
    vehicle_cost_data['insurance_cost'] = np.around(np.random.normal(200, 20, size=len(vehicle_cost_data)), decimals=2)
    vehicle_cost_data['maintenance_cost'] = np.around(
        np.random.normal(1200, 100, size=len(vehicle_cost_data)), decimals=2)
    vehicle_cost_data['total_cost'] = vehicle_cost_data['fuel_cost_total'] + vehicle_cost_data['insurance_cost'] + vehicle_cost_data['maintenance_cost']

    return vehicle_cost_data


def vehicle_build_year(df):
    # Simulate Vehicle Age per Vehicle
    # estimate vehicle build between 2000 and 2018
    df['vehicle_construction_year'] = np.random.randint(2000, 2018, size=len(df))
    return df


def maintenance_start_value(df):
    # generate maintenance start value
    df['maintenance'] = np.random.randint(0, 100, size=len(df))
    return df


def vehicle_capacity(v_df):
    # capacity in pounds depending on vehicle Class
    # iterate over dataframe and generate capacity for each vehicle in lst
    lst = []
    for index, row in v_df.iterrows():
        if row['vehicle_class'] == 2:
            lst.append(np.random.randint(1500, 3000))
        elif row['vehicle_class'] == 3:
            lst.append(np.random.randint(3000, 5500))
        elif row['vehicle_class'] == 4:
            lst.append(np.random.randint(5500, 7000))
        elif row['vehicle_class'] == 5:
            lst.append(np.random.randint(7000, 9500))
        elif row['vehicle_class'] == 6:
            lst.append(np.random.randint(9500, 13000))
        elif row['vehicle_class'] == 7:
            lst.append(np.random.randint(13000, 19000))
        else:
            lst.append(np.random.randint(19000, 60000))

    # add lst as new column
    v_df['load_capacity'] = lst

    return v_df


def vehicle_position(v_df):
    # generate a random Position for each vehicle in the Dataframe
    # generated a list with random locations on http://www.geomidpoint.com/random/
    # all within 200 Mile radius around Washington DC, 224 Datapoints
    df = pd.read_csv('random-locations.csv')
    v_df['position_latitude'] = df['latitude'].copy()
    v_df['position_longitude'] = df['longitude'].copy()

    return v_df


def vehicle_status(v_df):
    # generates random vehicle status with set probability for each status
    status = np.random.choice(['accident', 'unused', 'idle', 'on time', 'delayed'], p=[0.05, 0.1, 0.15, 0.4, 0.3], size=len(v_df))
    v_df['vehicle_status'] = status
    # add status 'maintenance' for each vehicle with a maintenance value over 95
    v_df.loc[v_df['maintenance'] >= 95, ['vehicle_status']] = 'maintenance'
    # ad vehicle status 'idle' for vehicles that have a long time at speed 0

    return v_df


def generate_licence_plate(v_df):
    lst = []
    for i in range(len(v_df)):
        i += 1
        if i <= 9:
            lst.append(('NRL-00'+ str(i)))
        elif i <= 99:
            lst.append(('NRL-0' + str(i)))
        else:
            lst.append(('NRL-' + str(i)))

    v_df['licence_plate'] = lst

    return v_df
