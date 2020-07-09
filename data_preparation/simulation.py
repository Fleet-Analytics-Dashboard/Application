import numpy as np

# Seed the random function to get reproduceable Results
# np.random.seed(1)

# Simulate Fuel, Insurance, Maintainance Cost per Vehicle
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
    # capacity in tonns depending on vehicle Class
    # iterate over dataframe
    lst = []
    result = v_df.copy()
    for index, row in v_df.iterrows():
        if row['vehicle_class'] == 2:
            lst.append(np.random.randint(1500, 3000))
        elif row['vehicle_class'] == 3:
            lst.append(np.random.randint(3000, 6000))
        elif row['vehicle_class'] == 4:
            lst.append(np.random.randint(5000, 7000))
        elif row['vehicle_class'] == 5:
            lst.append(np.random.randint(7000, 9500))
        elif row['vehicle_class'] == 6:
            lst.append(np.random.randint(9500, 13000))
        elif row['vehicle_class'] == 7:
            lst.append(np.random.randint(13000, 19000))
        else:
            lst.append(np.random.randint(19000, 60000))

    # add list as new column to result
    result['load_capacity'] = lst

    return result
