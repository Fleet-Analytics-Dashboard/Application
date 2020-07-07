from data_cleaning import new, pd
import numpy as np

# Seed the random function to get reproduceable Results
np.random.seed(1)

# Separate Vehicle Information from the rest of the dataset to normalise table
v_df = new[['vid', 'vehicle_class', 'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type']].copy()
new.drop(['vehicle_class', 'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type'], axis=1)

# drop duplicates in v_df
v_df = v_df.drop_duplicates(keep='first', ignore_index=True).sort_values('vid')

# Simulate Fuel, Insurance, Maintainance Cost per Vehicle
# Fuel Cost needs a estimated consumption first
# Simulate consumption depending on Vehicle Class, Drivetrain, Fuel Type


# Simulate Vehicle Age per Vehicle
# estimate vehicle build between 2000 and 2018
v_df['vehicle_age'] = np.random.randint(2000, 2018, size=len(v_df))
