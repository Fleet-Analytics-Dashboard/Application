import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import data_preparation.data_cleaning as data_cleaning
import data_preparation.maintenance_prediction as m_prediction
import data_preparation.simulation as simulation

# connect to database and write raw data into dataframe
# conn = connect()
# sql = "select * from raw_data_fleet_dna;"
# df = pd.read_sql_query(sql, conn)
# conn = None

# import NREL-Fleet-DNA-Data.csv as dataframe 'df' if Database is gone
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

# simulate vehicle consumption and fuel cost per drive
driving_data = simulation.fuel_cost(vehicle_data, driving_data)

# simulate cost per vehicle
vehicle_cost_data = simulation.cost_per_vehicle(vehicle_data, driving_data)

# drop the month out of driving_data to avoid problems when training XGBoost
driving_data = driving_data.drop('month', axis=1)

# generate a licence plate for each vehicel
vehicle_data = simulation.generate_licence_plate(vehicle_data)

#------------ include maintenance_prediction.py -----------------------
# Prepare Data by simulating sesor data from real variables
driving_data = m_prediction.get_sensor_data(driving_data)

# extract prediction data for predicting a final vehicle status later
predict, driving_data = m_prediction.extract_prediction_data(driving_data)

# prepare data for training the model
x, y = m_prediction.data_preparation(driving_data)

# convert to DMatrix for XGBoost
data_dmatrix = xgb.DMatrix(data=x, label=y)

# split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

#
xg_class = xgb.XGBClassifier(objective='binary:logistic', colsample_bytree=0.3, learning_rate=0.1, max_depth=5,
                            alpha=10, n_estimators=10)

xg_class.fit(X_train, y_train)

preds = xg_class.predict(X_test)
pred_prob = xg_class.predict_proba(X_test)

rmse = np.sqrt(mean_squared_error(y_test, preds))
print("RMSE: %f" % rmse)

#------------ return changes to database ------------------------------
# create new Database Tables from Dataframes
# engine = return_engine()
# driving_data.to_sql('driving_data', con=engine, if_exists='replace')
# vehicle_data.to_sql('vehicle_data', con=engine, if_exists='replace')
# vehicle_cost_data.to_sql('vehicle_cost_data', con=engine, if_exists='replace')
# engine = None
#
# # generate new csv Files from new dataframes
# vehicle_data.to_csv('vehicle_data.csv')
# driving_data.to_csv('driving_data.csv')
# vehicle_cost_data.to_csv('vehicle_cost_data.csv')
