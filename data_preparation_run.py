#Todo - switch from CSV to Database

import pandas as pd
import numpy as np
import data_preparation.data_cleaning as data_cleaning
import data_preparation.simulation as simulation
import data_preparation.maintenance_prediction as m_prediction

from database_connection import connect, return_engine

# connect to database and add files to
# conn = connect()
# sql = "select * from raw_data_fleet_dna;"
# df = pd.read_sql_query(sql, conn)
# conn = None

# import NREL-Fleet-DNA-Data.csv as dataframe 'df'
df = pd.read_csv('composite-data-for-fleet-dna-csv-1.csv')

#------------ include data_cleanig.py ---------------------------------
# generate two tables for vehicle and driving data
driving_data = data_cleaning.cleaning(df)
vehicle_data = data_cleaning.seperate_vehicle_data(driving_data)

# remove vehicle data from driving_data
driving_data = driving_data.drop(['vehicle_class', 'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type'], axis=1)

#------------ include simulation.py -----------------------------------
# Seed the random function to get reproduceable Results
np.random.seed(1)

# simulate random vehicle build year
vehicle_data = simulation.vehicle_build_year(vehicle_data)

# simulate random load capacity depending on vehicle class
vehicle_data = simulation.vehicle_capacity(vehicle_data)

# simulate random maintenance start value
vehicle_data = simulation.maintenance_start_value(vehicle_data)

# simulate vehicle position
vehicle_data = simulation.vehicle_position(vehicle_data)

# simulate vehicle status
vehicle_data = simulation.vehicle_status(vehicle_data)

#------------ include maintenance_prediction.py -----------------------
# add column with increase of maintenance value for each day
driving_data = m_prediction.maintenance_increase(driving_data)

# add maintenance increase to vehicle_data Dataframe
vehicle_data = m_prediction.sum_vehicle_maintenance(driving_data, vehicle_data)

#------------ return changes to database ------------------------------
# create new Database Table from Dataframe
# engine = return_engine()
# new.to_sql('cleaned_data_fleet_dna', con=engine, if_exists='replace')
# v_df.to_sql('vehicle_information', con=engine, if_exists='replace')
# engine = None

