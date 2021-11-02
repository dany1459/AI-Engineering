import pandas as pd
import numpy as np
import train as tr

model_rfc, model_xgb, model_cat, ct = tr.train()
model = [model_rfc, model_xgb, model_cat]

while True:

    age = int(input("How old are you? \n"))
    sex = str(input("What is your sex? Type in 'male' or 'female' \n"))
    bmi = float(input("What is your BMI? \n"))
    children = int(input("How many children do you have? \n"))
    smoker = str(input("Do you smoke? Type in 'yes' or 'no' \n"))
    region = str(input("Where are you from? Type in one of: 'northeast', 'northwest', southeast', southwest' \n"))

    new_data = pd.DataFrame({'age':age, 'sex':sex, 'bmi':bmi, 'children':children, 'smoker':smoker, 'region':region}, index=[0])
    new_data_transformed = ct.transform(new_data)

    preds = np.array([clf.predict(new_data_transformed) for clf in model])
    print(f'Random Forest Classifier predicted: {preds[0]}')
    print(f'XGBRegressor predicted: {preds[1]}')
    print(f'CatBoostRegressor predicted: {preds[2]}')
    print(f'On average the prediction is: {preds.mean()}')
