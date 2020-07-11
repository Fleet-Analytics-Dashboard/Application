import numpy as np
import pandas as pd

# Simulate Fuel, Insurance, Maintenance Cost per Vehicle
# Fuel Cost will be added per day in the large table but needs a estimated consumption first
# Build consumption groupes with a estimated range of l/100km depending on Vehicle Class, Drivetrain, Fuel Type


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
    df = pd.read_csv('random-locations_latitude-longitude.csv')
    v_df['position_latitude'] = df['latitude'].copy()
    v_df['position_longitude'] = df['longitude'].copy()

    return v_df


def vehicle_status(v_df):
    # generates random vehicle status with set probability for each status
    status = np.random.choice(['accident', 'unused', 'on time', 'delayed'], p=[0.06, 0.2, 0.44, 0.3], size=len(v_df))
    v_df['vehicle_status'] = status
    # add status 'maintenance' for each vehicle with a maintenance value over 95
    v_df.loc[v_df['maintenance'] >= 95, ['vehicle_status']] = 'maintenance'

    return v_df
