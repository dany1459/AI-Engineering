import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
import data_handler as dh
import train as tr

model = tr.train()

while True:

    age = int(input("How old are you? \n"))
    sex = int(input("What is your sex? Type in 'male' or 'female' \n"))
    bmi = float(input("What is your BMI? \n"))
    children = int(input("How many children do you have? \n"))
    smoker = str(input("Do you smoke? Type in 'yes' or 'no'\n"))
    region = str(input("Where are you from? Type in one of: 'northeast', 'northwest', southeast', southwest'\n"))


    new_data = pd.DataFrame({'age':age, 'sex':sex, 'bmi':bmi, 'children':children, 'smoker':smoker, 'region':region})
    new_data_transformed = model.ct.transform(new_data)
    # new_data_scaled = model.mm_scaler.transform(new_data_transformed)

    preds = np.array([ clf.predict(new_data) for clf in model[:4] ])
    print(preds.mean())
    # print(accuracy_score(preds, dh.y_test))
    
    print(new_data.head())
