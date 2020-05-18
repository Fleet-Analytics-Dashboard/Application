import pandas as pd

# import NREL-Fleet-DNA-Data.csv as dataframe 'df'
df = pd.read_csv('Batch-data/composite-data-for-fleet-dna-csv-1.csv')

# create new dataframe with all relevant columns and add all the IDs and vehicle information
new = df[['vid', 'did', 'pid', 'class_id', 'voc_id', 'type_id', 'drive_id', 'fuel_id', 'day_id']].copy()

# add all relevant columns from category 'Speed' (original column ...-...)

# add all relevant columns from category 'Acceleration and Deceleration' (original column ...-...)

# add all relevant columns from category 'Stops' (original column ...-...)

# add all relevant columns from category 'Elevation' (original column 193-232)
new['max_elevation'] = df['max_elevation'].copy()
new['min_elevation'] = df['min_elevation'].copy()
new['mean_elevation'] = df['mean_elevation'].copy()
new['delta_elevation'] = df['delta_elevation'].copy()
new['total_elevation_gained'] = df['total_elevation_gained'].copy()
new['total_elevation_lost'] = df['total_elevation_lost'].copy()
new['max_climbing_rate'] = df['max_climbing_rate'].copy()
new['average_climbing_rate'] = df['average_climbing_rate'].copy()
new['max_descending_rate'] = df['max_descending_rate'].copy()
new['average_descending_rate'] = df['average_descending_rate'].copy()

# add all relevant columns from category 'Power Density' (original column 234-292)

# add all relevant columns from category 'Road Data' (original column 294-272)

# save new df as new csv-file in same folder
new.to_csv('Batch-data/cleaned-data-for-fleet-dna.csv')