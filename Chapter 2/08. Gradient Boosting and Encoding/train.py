import data_handler as dh
from joblib import dump
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from xgboost import XGBRegressor
from catboost import CatBoostRegressor

def train():
    path = (r"C:\Users\Igor\Documents\GitHub\AI-Engineering\Chapter 2\08. Gradient Boosting and Encoding\insurance.csv")

    x_train, x_test, y_train, y_test, ct = dh.get_data(path)

    rfc = RandomForestClassifier(n_estimators=50, max_depth=7, n_jobs=3, verbose=False)
    gbc = GradientBoostingClassifier(learning_rate=0.05, n_estimators=200, verbose=False)
    xgb = XGBRegressor()
    cat = CatBoostRegressor()

  
    rfc.fit(x_train, y_train)
    # gbc.fit(x_train, y_train)
    # xgb.fit(x_train, y_train)
    # cat.fit(x_train, y_train)

    # dump(rfc, 'model_rfc')
    return rfc, ct#, gbc, ct#, xgb, cat, ct

train()

# dump(rfc, 'model_rfc')
