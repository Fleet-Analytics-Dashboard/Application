# Todo:
#   - Replace 'clas_id', 'voc_id', 'type_id', 'drive_id' and 'fuel_id' with representing strings from PDF Document

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
new['maximum_kinetic_power_density_demand'] = df['maximum_kinetic_power_density_demand'].copy()
new['total_kinetic_power_density_demand'] = df['total_kinetic_power_density_demand'].copy()
new['average_kinetic_power_density_demand'] = df['average_kinetic_power_density_demand'].copy()
new['maximum_kinetic_power_density_regen'] = df['maximum_kinetic_power_density_regen'].copy()
new['total_kinetic_power_density_regen'] = df['total_kinetic_power_density_regen'].copy()
new['average_kinetic_power_density_regen'] = df['average_kinetic_power_density_regen'].copy()
new['maximum_potential_power_density_demand'] = df['maximum_potential_power_density_demand'].copy()
new['total_potential_power_density_demand'] = df['total_potential_power_density_demand'].copy()
new['average_potential_power_density_demand'] = df['average_potential_power_density_demand'].copy()
new['maximum_potential_power_density_regen'] = df['maximum_potential_power_density_regen'].copy()
new['total_potential_power_density_regen'] = df['total_potential_power_density_regen'].copy()
new['average_potential_power_density_regen'] = df['average_potential_power_density_regen'].copy()
new['maximum_aerodynamic_power_density_demand'] = df['maximum_aerodynamic_power_density_demand'].copy()
new['total_aerodynamic_power_density_demand'] = df['total_aerodynamic_power_density_demand'].copy()
new['average_aerodynamic_power_density_demand'] = df['average_aerodynamic_power_density_demand'].copy()
new['maximum_aerodynamic_power_density_regen'] = df['maximum_aerodynamic_power_density_regen'].copy()
new['total_aerodynamic_power_density_regen'] = df['total_aerodynamic_power_density_regen'].copy()
new['average_aerodynamic_power_density_regen'] = df['average_aerodynamic_power_density_regen'].copy()
new['maximum_rolling_power_density_demand'] = df['maximum_rolling_power_density_demand'].copy()
new['total_rolling_power_density_demand'] = df['total_rolling_power_density_demand'].copy()
new['average_rolling_power_density_demand'] = df['average_rolling_power_density_demand'].copy()
new['maximum_rolling_power_density_regen'] = df['maximum_rolling_power_density_regen'].copy()
new['total_rolling_power_density_regen'] = df['total_rolling_power_density_regen'].copy()
new['average_rolling_power_density_regen'] = df['average_rolling_power_density_regen'].copy()
new['characteristic_acceleration_standard'] = df['ca_standard'].copy()
new['characteristic_deceleration_standard'] = df['cd_standard'].copy()
new['aerodynamic_speed_standard'] = df['as_standard'].copy()
new['kinetic_intensity_standard'] = df['ki_standard'].copy()

# add all relevant columns from category 'Road Data' (original column 294-272)
new['group_ttl_total_points'] = df['group_ttl_ttl'].copy()
new['group_ttl_distance'] = df['group_ttl_distance'].copy()
new['matched_ttl_distance'] = df['matched_ttl_distance'].copy()
new['matched_ttl_total_points'] = df['matched_ttl_ttl'].copy()
new['non_matched_ttl_total_points'] = df['non_matched_ttl_ttl'].copy()
new['non_matched_ttl_distance'] = df['non_matched_ttl_distance'].copy()

new['func_1_ttl'] = df['func_1_ttl'].copy()
new['func_1_distance'] = df['func_1_distance'].copy()
new['func_2_ttl'] = df['func_2_ttl'].copy()
new['func_2_distance'] = df['func_2_distance'].copy()
new['func_3_ttl'] = df['func_3_ttl'].copy()
new['func_3_distance'] = df['func_3_distance'].copy()
new['func_4_ttl'] = df['func_4_ttl'].copy()
new['func_4_distance'] = df['func_4_distance'].copy()
new['func_5_ttl'] = df['func_5_ttl'].copy()
new['func_5_distance'] = df['func_5_distance'].copy()

new['spd_cat_1_ttl'] = df['spd_cat_1_ttl'].copy()
new['spd_cat_1_distance'] = df['spd_cat_1_distance'].copy()
new['spd_cat_2_ttl'] = df['spd_cat_2_ttl'].copy()
new['spd_cat_2_distance'] = df['spd_cat_2_distance'].copy()
new['spd_cat_3_ttl'] = df['spd_cat_3_ttl'].copy()
new['spd_cat_3_distance'] = df['spd_cat_3_distance'].copy()
new['spd_cat_4_ttl'] = df['spd_cat_4_ttl'].copy()
new['spd_cat_4_distance'] = df['spd_cat_4_distance'].copy()
new['spd_cat_5_ttl'] = df['spd_cat_5_ttl'].copy()
new['spd_cat_5_distance'] = df['spd_cat_5_distance'].copy()
new['spd_cat_6_ttl'] = df['spd_cat_6_ttl'].copy()
new['spd_cat_6_distance'] = df['spd_cat_6_distance'].copy()
new['spd_cat_7_ttl'] = df['spd_cat_7_ttl'].copy()
new['spd_cat_7_distance'] = df['spd_cat_7_distance'].copy()
new['spd_cat_8_ttl'] = df['spd_cat_8_ttl'].copy()
new['spd_cat_8_distance'] = df['spd_cat_8_distance'].copy()

# save new df as new csv-file in same folder
new.to_csv('Batch-data/cleaned-data-for-fleet-dna.csv')