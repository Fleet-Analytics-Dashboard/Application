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


def data_preparation(d_df):
    # sort day_id descending so that we can easily extract the last day of each vehicle later
    d_df = d_df.sort_values('day_id', ascending=False)

    # create array with all vid
    vid_all = d_df['vid'].unique()

    # encode all cathegorical values with one hot encoding
    # variables to encode: 'vid', 'pid'
    d_df['vid'] = pd.Categorical(d_df['vid'])
    d_df['pid'] = pd.Categorical(d_df['pid'])
    d_df = pd.get_dummies(d_df, ['vid', 'pid'])

    # extract prediction variables from dataframe and store in x_pred
    i = 0
    x_pred = pd.DataFrame()
    for index, row in d_df.iterrows():
        if i < len(vid_all):
            if row['vid_'+str(vid_all[i])] == 1:
                x_pred = x_pred.append(row)
                d_df = d_df.drop(index, axis=0)
                i += 1

    # Separate the target variable maintenance_need from the rest of the variables
    x = d_df.drop('maintenance_need', axis=1)
    x_pred = x_pred.drop('maintenance_need', axis=1)
    y = d_df['maintenance_need']

    # resort columns of x_pred to prevend feature_names mismatch when predicting with xgb
    cols = x.columns.tolist()
    x_pred = x_pred[cols]

    return x, y, x_pred


def predict_maintenance(x, y, dmatrix, v_df, x_pred):
    # use 10 fold cross validation to check if our modell ist sutable for the job
    params = {"objective": "binary:logistic", 'colsample_bytree': 0.3, 'learning_rate': 0.1,
              'max_depth': 5, 'alpha': 10}

    cv_results = xgb.cv(dtrain=dmatrix, params=params, nfold=10,
                        num_boost_round=50, early_stopping_rounds=10, metrics="rmse", as_pandas=True, seed=123)

    # instantiate an XGBoost classifier object
    xg_class = xgb.XGBClassifier(params=params, n_estimators=10)

    # train the xgboost classifier with all our Data except x_pred
    xg_class.fit(x, y)

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

    return cv_results, v_df, xg_class
