import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


def get_sensor_data(d_df):
    # take realistic variables and define a threshold for malfunction recognised by a sesor

    # 'maximum_rolling_power_density_demand' for tire sensor and 310 as threshold
    d_df['tire_sensor'] = 0
    d_df.loc[d_df['maximum_rolling_power_density_demand'] >= 310, ['tire_sensor']] = 1

    # 'maximum_kinetic_power_density_demand' for engine sensor and 60
    d_df['engine_sensor'] = 0
    d_df.loc[d_df['maximum_kinetic_power_density_demand'] >= 60, ['engine_sensor']] = 1

    # 'max_deceleration_event_duration' for break sensor and 1000 as threshold
    d_df['break_sensor'] = 0
    d_df.loc[d_df['max_deceleration_event_duration'] >= 1200, ['break_sensor']] = 1

    # define a maintenance need that alerts maintenance if 2 or more sensors show a problem
    d_df['maintenance_need'] = 0
    d_df.loc[(d_df['break_sensor'] + d_df['engine_sensor'] + d_df['tire_sensor']) >= 2, ['maintenance_need']] = 1

    return d_df


def prepare_prediction_data(d_df):
    # we want to extract the last day_id of each vehicle to predict the final status of each vehicle
    # we can achieve this by sorting the data for day_id descending first and then drop all duplicates in vid
    pred = d_df.copy()
    pred = pred.sort_values('day_id', ascending=False).drop_duplicates('vid', keep='first')
    pred = pred.sort_values('vid', ascending=True)
    pred = pred.drop('maintenance_need', axis=1)

    # apply one hot encoding
    pred['vid'] = pd.Categorical(pred['vid'])
    pred['pid'] = pd.Categorical(pred['pid'])
    pred = pd.get_dummies(pred, ['vid', 'pid'])

    return pred


def data_preparation(d_df):
    # encode all cathegorical values with one hot encoding
    # variables to encode: 'vid', 'pid'
    d_df['vid'] = pd.Categorical(d_df['vid'])
    d_df['pid'] = pd.Categorical(d_df['pid'])
    d_df = pd.get_dummies(d_df, ['vid', 'pid'])

    # Separate the target variable maintenance_need from the rest of the variables
    x = d_df.drop('maintenance_need', axis=1)
    y = d_df['maintenance_need']

    return x, y


def predict_maintenance(x, y, v_df, x_pred):
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    # instantiate an XGBoost classifier object
    xg_class = xgb.XGBClassifier(objective='binary:logistic', colsample_bytree=0.3, learning_rate=0.1, max_depth=5,
                                 alpha=10, n_estimators=10)

    # train the xgboost classifier
    xg_class.fit(X_train, y_train)

    # predict values for the tast date and calculate rmse for validation of the model
    preds = xg_class.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))

    # predict probabilities for last vehicle day and ad it to vehicle data
    pred_prob = xg_class.predict_proba(x_pred)

    v_df['predicted_maintenance_probability'] = pred_prob[:, 1]

    # add left weeks till maintenance based on probabilities
    v_df['predicted_weeks_until_maintenance'] = 30
    v_df.loc[v_df['predicted_maintenance_probability'] >= 0.50, 'predicted_weeks_until_maintenance'] = 1
    v_df.loc[(v_df['predicted_maintenance_probability'] >= 0.40) & (
                v_df['predicted_maintenance_probability'] <= 0.50), 'predicted_weeks_until_maintenance'] = 2
    v_df.loc[(v_df['predicted_maintenance_probability'] >= 0.35) & (
                v_df['predicted_maintenance_probability'] <= 0.40), 'predicted_weeks_until_maintenance'] = 3
    v_df.loc[(v_df['predicted_maintenance_probability'] >= 0.30) & (
                v_df['predicted_maintenance_probability'] <= 0.35), 'predicted_weeks_until_maintenance'] = 4

    return rmse, v_df
