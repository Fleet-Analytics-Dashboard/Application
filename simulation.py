from data_cleaning import new, v_df, pd
import numpy as np
import xgboost as xgb

# Seed the random function to get reproduceable Results
np.random.seed(1)

# Simulate Fuel, Insurance, Maintainance Cost per Vehicle
# Fuel Cost will be added per day in the large table but needs a estimated consumption first
# Build consumption groupes with a estimated range of l/100km depending on Vehicle Class, Drivetrain, Fuel Type


# Simulate Vehicle Age per Vehicle
# estimate vehicle build between 2000 and 2018
v_df['vehicle_construction_year'] = np.random.randint(2000, 2018, size=len(v_df))

# generate maintenance start value
v_df['maintenance'] = np.random.randint(0, 100, size=len(v_df))

# capacity in tonns depending on vehicle Class
# seperate all vehicle classes and generate random capacytie for them
# cap2 = new[new.vehicle_class == 2]
# cap2['vehicle_load_capacity'] = np.random.randint(2000, 2018, size=len(cap2))
# cap3 = new[new.vehicle_class == 3]
# cap4 = new[new.vehicle_class == 4]
# cap5 = new[new.vehicle_class == 5]
# cap6 = new[new.vehicle_class == 6]
# cap7 = new[new.vehicle_class == 7]
# cap8 = new[new.vehicle_class == 8]
