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
    # summ up fuel cost per vehicle
    sum = {}
    for index, row in d_df.iterrows():
        if int(row['vid']) in sum.keys():
            sum[int(row['vid'])] += row['fuel_cost']
        else:
            sum[int(row['vid'])] = row['fuel_cost']
    # ad a column with the value that needs to be added
    v_df['fuel_cost_total'] = v_df['vid'].map(sum)

    # simulate insurance cost in dollar per vehicle with normal distribution around 4000$
    v_df['insurance_cost'] = np.around(np.random.normal(4000, 1000, size=len(v_df)), decimals=2)

    # simulate maintenance cost with normal distribution around 15000$
    v_df['maintenance_cost'] = np.around(np.random.normal(15000, 5000, size=len(v_df)), decimals=2)

    # add a column with total cost per Year
    v_df['total_cost'] = v_df['fuel_cost_total'] + v_df['insurance_cost'] + v_df['maintenance_cost']

    return v_df


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
