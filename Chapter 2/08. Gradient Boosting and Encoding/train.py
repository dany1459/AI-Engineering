import data_handler as dh
from joblib import dump
import pickle

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

def train():
    path = (r"C:\Users\Igor\Documents\GitHub\AI-Engineering\Chapter 2\08. Gradient Boosting and Encoding\insurance.csv")

    x_train, x_test, y_train, y_test, ct = dh.get_data(path)

    rfc = RandomForestClassifier(verbose=False)
    xgb = XGBRegressor()
    cat = CatBoostRegressor(verbose=False)
  
    rfc.fit(x_train, y_train)
    xgb.fit(x_train, y_train)
    cat.fit(x_train, y_train)

    # return pickle.dump(rfc, open('model_RFC.sav', 'wb'))
    return rfc, xgb, cat, ct
