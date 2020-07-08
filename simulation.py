from data_cleaning import new, pd
import numpy as np
import xgboost as xgb

# Seed the random function to get reproduceable Results
np.random.seed(1)

# Separate Vehicle Information from the rest of the dataset to normalise table
v_df = new[['vid', 'vehicle_class', 'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type']].copy()
new.drop(['vehicle_class', 'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type'], axis=1)

# drop duplicates in v_df
v_df = v_df.drop_duplicates(keep='first', ignore_index=True).sort_values('vid')

# Simulate Fuel, Insurance, Maintainance Cost per Vehicle
# Fuel Cost will be added per day in the large table but needs a estimated consumption first
# Build consumption groupes with a estimated range of l/100km depending on Vehicle Class, Drivetrain, Fuel Type


# Simulate Vehicle Age per Vehicle
# estimate vehicle build between 2000 and 2018
v_df['vehicle_construction_year'] = np.random.randint(2000, 2018, size=len(v_df))

# capacity in tonns depending on vehicle Class