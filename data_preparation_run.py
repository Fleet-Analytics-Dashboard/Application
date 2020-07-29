import pandas as pd
import numpy as np
import xgboost as xgb
import data_preparation.data_cleaning as data_cleaning
import data_preparation.maintenance_prediction as m_prediction
import data_preparation.simulation as simulation
from database_connection import return_engine, connect

# connect to database and write raw data into dataframe
# conn = connect()
# sql = "select * from raw_data_fleet_dna;"
# df = pd.read_sql_query(sql, conn)
# conn = None

# import NREL-Fleet-DNA-Data.csv as dataframe 'df' if Database is gone
df = pd.read_csv('csv_data_files/composite-data-for-fleet-dna-csv-1.csv')
driver_names = pd.read_csv('csv_data_files/names.csv')

# ------------ include data_cleanig.py ---------------------------------
# generate two tables for vehicle and driving data
driving_data = data_cleaning.cleaning(df)
vehicle_data = data_cleaning.seperate_vehicle_data(driving_data)

# remove vehicle data from driving_data
driving_data = driving_data.drop(['vehicle_class', 'vocation', 'vehicle_type', 'fuel_type', 'drivetrain_type'], axis=1)

# ------------ include simulation.py -----------------------------------
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

# simulate vehicle consumption and fuel cost per drive
driving_data = simulation.fuel_cost(vehicle_data, driving_data)

# simulate cost per vehicle
vehicle_cost_data = simulation.cost_per_vehicle(vehicle_data, driving_data)

# drop the month out of driving_data to avoid problems when training XGBoost
driving_data = driving_data.drop('month', axis=1)

# generate a licence plate for each vehicel
vehicle_data = simulation.generate_licence_plate(vehicle_data)

# generate a accident probability per vehicle
vehicle_data = simulation.accident_probability(vehicle_data)

# ------------ include maintenance_prediction.py -----------------------
# Prepare Data by simulating sensor data from real variables
driving_data = m_prediction.get_sensor_data(driving_data)

# prepare data for training the model
x, y, x_pred = m_prediction.data_preparation(driving_data)

# convert to DMatrix for XGBoost
data_dmatrix = xgb.DMatrix(data=x, label=y)

# train a xgb modell for classifiction
# returns cv_table (route mean square error) and vehicle_data with probability for maintenance need
cv_table, vehicle_data, xg_class = m_prediction.predict_maintenance(x, y, data_dmatrix, vehicle_data, x_pred)

# ------------ return changes to database ------------------------------
# create new Database Tables from Dataframes
# engine = return_engine()
# driving_data.to_sql('driving_data', con=engine, if_exists='replace')
# vehicle_data.to_sql('vehicle_data', con=engine, if_exists='replace')
# vehicle_cost_data.to_sql('vehicle_cost_data', con=engine, if_exists='replace')
# cv_table.to_sql('10_fold_cross_validation_maintenance', con=engine, if_exists='replace')
# driver_names.to_sql('driver_names', con=engine, if_exists='replace')
# engine = None

# generate new csv Files from new dataframes
vehicle_data.to_csv('csv_data_files/vehicle_data.csv')
driving_data.to_csv('csv_data_files/driving_data.csv')
vehicle_cost_data.to_csv('csv_data_files/vehicle_cost_data.csv')
cv_table.to_csv('csv_data_files/10_fold_cross_validation_maintenance.csv')
