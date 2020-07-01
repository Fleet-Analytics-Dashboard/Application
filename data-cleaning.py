import pandas as pd
from database_connection import connect, return_engine

# connect to database and add files to
conn = connect()
sql = "select * from raw_data_fleet_dna;"
df = pd.read_sql_query(sql, conn)
conn = None

# create a new dataframe for vehicle capacity table with all relevant columns

# create new dataframe with all relevant columns and add all the IDs and vehicle information
new = df[['vid', 'did', 'pid', 'class_id', 'voc_id', 'type_id', 'drive_id', 'fuel_id', 'day_id']].copy()

# replace IDs for 'voc_id', 'type_id', 'drive_id', 'fuel_id' with their meaning
# voc_id --> Vocation
new.replace({'voc_id': {1: 'Telecom', 2: 'Beverage Delivery', 3: 'Warehouse Delivery', 4: 'Parcel Delivery',
                        5: 'School Bus', 6: 'Linen Delivery', 7: 'Refuse Pickup', 8: 'Long Haul', 10: 'Mass Transit',
                        11: 'Towing', 12: 'Grocery Delivery', 13: 'Port Drayage', 14: 'Food Delivery', 15: 'Snow Plow',
                        16: 'Utility', 18: 'Local Delivery'}}, inplace=True)
# type_id --> Vehicle Type
new.replace({'type_id': {1: 'Beverage', 2: 'Bucket Truck', 3: 'Cement Mixer', 4: 'City Delivery', 5: 'City Transit Bus',
                         6: 'Conventional Van', 7: 'Crew Size Pickup', 8: 'Dump', 9: 'Fire Truck', 10: 'Fuel',
                         11: 'Full Size Pickup', 12: 'Furniture', 13: 'Heavy Semi Tractor', 14: 'High Profile Semi',
                         15: 'Home Fuel', 16: 'Landscape Utility', 17: 'Medium Semi Tractor', 18: 'Mini Bus',
                         20: 'Mini Pickup', 21: 'Minivan', 23: 'Rack', 24: 'Refrigerated Van', 25: 'Refuse Truck',
                         26: 'School Bus', 27: 'Semi Sleeper', 28: 'Service Van', 29: 'Single Axle Van',
                         30: 'Stake Body', 31: 'Step Van', 32: 'Straight Truck', 33: 'SUV', 34: 'Tour Bus', 35: 'Tow',
                         36: 'Tractor', 37: 'Type C', 38: 'Utility Van', 39: 'Walk In'}}, inplace=True)

# drive_id --> Drivetrain Type
new.replace({'drive_id': {0: 'Conventional', 1: 'Parallel Hybrid', 2: 'Hydraulic Hybrid', 3: 'Series Hybrid',
                          4: 'Hybrid', 5: 'Electric', 6: 'Hybrid Electric'}}, inplace=True)

# fuel_id --> Fuel Type
new.replace({'fuel_id': {0: 'Gasoline', 1: 'Diesel', 2: 'Electricity', 3: 'Compressed Natural Gas'}}, inplace=True)

# rename columns for better understanding
new = new.rename(
    columns={'class_id': 'vehicle_class', 'voc_id': 'vocation', 'type_id': 'vehicel_type',
             'drive_id': 'drivetrain_type', 'fuel_id': 'fuel_type'})


# add all relevant columns from category 'Speed' (original column 17-123, 287-372)
new['speed_data_duration_hrs_includes_zero'] = df['speed_data_duration_hrs'].copy()
new['driving_data_duration_hrs_no_zero'] = df['driving_data_duration_hrs'].copy()
new['max_speed'] = df['max_speed'].copy()
new['total_average_speed_includes_zero'] = df['total_average_speed'].copy()
new['total_median_speed_includes_zero'] = df['total_median_speed'].copy()
new['driving_average_speed_no_zero'] = df['driving_average_speed'].copy()
new['seconds_at_speed_zero'] = df['zero_seconds'].copy()
new['seconds_at_speed_zero_five'] = df['zero_five_seconds'].copy()
new['seconds_at_speed_seventy_five_plus'] = df['seventy_five_plus_seconds'].copy()
new['driving_time_seconds'] = df['driving_time_seconds'].copy()
new['percent_time_at_speed_zero'] = df['percent_zero'].copy()
new['percent_time_at_speed_zero_five'] = df['percent_zero_five'].copy()
new['percent_time_at_speed_seventy_five_plus'] = df['percent_seventy_five_plus'].copy()
new['percent_distance_at_speed_seventy_five_plus'] = df['percent_distance_seventy_five_plus'].copy()
new['distance_at_speed_zero_five'] = df['distance_zero_five'].copy()
new['distance_at_speed_seventy_five_plus'] = df['distance_seventy_five_plus'].copy()
new['aerodynamic_speed'] = df['aerodynamic_speed'].copy()
new['as_standard'] = df['as_standard'].copy()
new['group_ttl_mean_speed_no_zero'] = df['group_ttl_mean_speed'].copy()
new['group_ttl_std_deviation_speed_no_zero'] = df['group_ttl_std_speed'].copy()
new['group_ttl_zero_speed'] = df['group_ttl_zero_speed'].copy()
new['matched_ttl_mean_speed_no_zero'] = df['matched_ttl_mean_speed'].copy()
new['matched_ttl_std_deviation_speed_no_zero'] = df['matched_ttl_std_speed'].copy()
new['matched_ttl_zero_speed'] = df['matched_ttl_zero_speed'].copy()
new['non_matched_ttl_mean_speed_no_zero'] = df['non_matched_ttl_mean_speed'].copy()
new['non_matched_ttl_std_deviation_speed_no_zero'] = df['non_matched_ttl_std_speed'].copy()
new['non_matched_ttl_zero_speed'] = df['non_matched_ttl_zero_speed'].copy()
new['func_1_mean_speed'] = df['func_1_mean_speed'].copy()
new['func_1_std_speed'] = df['func_1_std_speed'].copy()
new['func_1_zero_speed'] = df['func_1_zero_speed'].copy()
new['func_2_mean_speed'] = df['func_2_mean_speed'].copy()
new['func_2_std_speed'] = df['func_2_std_speed'].copy()
new['func_2_zero_speed'] = df['func_2_zero_speed'].copy()
new['func_3_mean_speed'] = df['func_3_mean_speed'].copy()
new['func_3_std_speed'] = df['func_3_std_speed'].copy()
new['func_3_zero_speed'] = df['func_3_zero_speed'].copy()
new['func_4_mean_speed'] = df['func_4_mean_speed'].copy()
new['func_4_std_speed'] = df['func_4_std_speed'].copy()
new['func_4_zero_speed'] = df['func_4_zero_speed'].copy()
new['func_5_mean_speed'] = df['func_5_mean_speed'].copy()
new['func_5_std_speed'] = df['func_5_std_speed'].copy()
new['func_5_zero_speed'] = df['func_5_zero_speed'].copy()
new['spd_cat_1_mean_speed'] = df['spd_cat_1_mean_speed'].copy()
new['spd_cat_1_std_speed'] = df['spd_cat_1_std_speed'].copy()
new['spd_cat_1_ttl'] = df['spd_cat_1_ttl'].copy()
new['spd_cat_1_zero_speed'] = df['spd_cat_1_zero_speed'].copy()
new['spd_cat_2_mean_speed'] = df['spd_cat_2_mean_speed'].copy()
new['spd_cat_2_std_speed'] = df['spd_cat_2_std_speed'].copy()
new['spd_cat_2_ttl'] = df['spd_cat_2_ttl'].copy()
new['spd_cat_2_zero_speed'] = df['spd_cat_2_zero_speed'].copy()
new['spd_cat_3_mean_speed'] = df['spd_cat_3_mean_speed'].copy()
new['spd_cat_3_std_speed'] = df['spd_cat_3_std_speed'].copy()
new['spd_cat_3_ttl'] = df['spd_cat_3_ttl'].copy()
new['spd_cat_3_zero_speed'] = df['spd_cat_3_zero_speed'].copy()
new['spd_cat_4_mean_speed'] = df['spd_cat_4_mean_speed'].copy()
new['spd_cat_4_std_speed'] = df['spd_cat_4_std_speed'].copy()
new['spd_cat_4_ttl'] = df['spd_cat_4_ttl'].copy()
new['spd_cat_4_zero_speed'] = df['spd_cat_4_zero_speed'].copy()
new['spd_cat_5_mean_speed'] = df['spd_cat_5_mean_speed'].copy()
new['spd_cat_5_std_speed'] = df['spd_cat_5_std_speed'].copy()
new['spd_cat_5_ttl'] = df['spd_cat_5_ttl'].copy()
new['spd_cat_5_zero_speed'] = df['spd_cat_5_zero_speed'].copy()
new['spd_cat_6_mean_speed'] = df['spd_cat_6_mean_speed'].copy()
new['spd_cat_6_std_speed'] = df['spd_cat_6_std_speed'].copy()
new['spd_cat_6_ttl'] = df['spd_cat_6_ttl'].copy()
new['spd_cat_6_zero_speed'] = df['spd_cat_6_zero_speed'].copy()
new['spd_cat_7_mean_speed'] = df['spd_cat_7_mean_speed'].copy()
new['spd_cat_7_std_speed'] = df['spd_cat_7_std_speed'].copy()
new['spd_cat_7_ttl'] = df['spd_cat_7_ttl'].copy()
new['spd_cat_7_zero_speed'] = df['spd_cat_7_zero_speed'].copy()
new['spd_cat_8_mean_speed'] = df['spd_cat_8_mean_speed'].copy()
new['spd_cat_8_std_speed'] = df['spd_cat_8_std_speed'].copy()
new['spd_cat_8_ttl'] = df['spd_cat_8_ttl'].copy()
new['spd_cat_8_zero_speed'] = df['spd_cat_8_zero_speed'].copy()

# add all relevant columns from category 'Acceleration and Deceleration' (original column 124-173)
new['total_number_of_acceleration_events'] = df['total_number_of_acceleration_events'].copy()
new['total_number_of_deceleration_events'] = df['total_number_of_deceleration_events'].copy()
new['acceleration_events_per_mile'] = df['acceleration_events_per_mile'].copy()
new['deceleration_events_per_mile'] = df['deceleration_events_per_mile'].copy()
new['max_acceleration_ft_per_second_squared'] = df['max_acceleration_ft_per_second_squared'].copy()
new['max_deceleration_ft_per_second_squared'] = df['max_deceleration_ft_per_second_squared'].copy()
new['average_acceleration_ft_per_second_squared'] = df['average_acceleration_ft_per_second_squared'].copy()
new['average_deceleration_ft_per_second_squared'] = df['average_deceleration_ft_per_second_squared'].copy()
new['average_acceleration_event_duration'] = df['average_acceleration_event_duration'].copy()
new['average_deceleration_event_duration'] = df['average_deceleration_event_duration'].copy()
new['min_acceleration_event_duration'] = df['min_acceleration_event_duration'].copy()
new['min_deceleration_event_duration'] = df['min_deceleration_event_duration'].copy()
new['max_acceleration_event_duration'] = df['max_acceleration_event_duration'].copy()
new['max_deceleration_event_duration'] = df['max_deceleration_event_duration'].copy()

new['cumulative_acceleration_duration'] = df['cumulative_acceleration_duration'].copy()
new['cumulative_deceleration_duration'] = df['cumulative_deceleration_duration'].copy()
new['absolute_time_cumulative_acceleration_duration'] = df['absolute_time_cumulative_acceleration_duration'].copy()
new['absolute_time_cumulative_deceleration_duration'] = df['absolute_time_cumulative_deceleration_duration'].copy()

# add all relevant columns from category 'Stops' (original column 174-192)
new['average_stop_duration'] = df['average_stop_duration'].copy()
new['min_stop_duration'] = df['min_stop_duration'].copy()
new['max_stop_duration'] = df['max_stop_duration'].copy()
new['stops_0_30_seconds'] = df['stops_0_30'].copy()
new['stops_30_60_seconds'] = df['stops_30_60'].copy()
new['stops_60_plus_seconds'] = df['stops_60_plus'].copy()
new['stops_300_plus_seconds'] = df['stops_300_plus'].copy()
new['stops_1800_plus_seconds'] = df['stops_1800_plus'].copy()
new['stops_3600_plus_seconds'] = df['stops_3600_plus'].copy()
new['stops_per_mile'] = df['stops_per_mile'].copy()
new['total_stops'] = df['total_stops'].copy()
#new['non_recorded_time_hrs'] = df['non_recorded_time_hrs'].copy()

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

new['spd_cat_1_distance'] = df['spd_cat_1_distance'].copy()
new['spd_cat_2_distance'] = df['spd_cat_2_distance'].copy()
new['spd_cat_3_distance'] = df['spd_cat_3_distance'].copy()
new['spd_cat_4_distance'] = df['spd_cat_4_distance'].copy()
new['spd_cat_5_distance'] = df['spd_cat_5_distance'].copy()
new['spd_cat_6_distance'] = df['spd_cat_6_distance'].copy()
new['spd_cat_7_distance'] = df['spd_cat_7_distance'].copy()
new['spd_cat_8_distance'] = df['spd_cat_8_distance'].copy()

# replace the NaN values with 0
new.fillna(0, inplace=True)

# create new Database Table from Dataframe
engine = return_engine()
new.to_sql('cleaned_data_fleet_dna', con=engine, if_exists='replace')
engine = None