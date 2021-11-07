import hipocratia
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing   import StandardScaler

model = hipocratia.train()

while True:

    age = int(input("How old are you? \n"))
    sex = int(input("What is your sex? Type in 'male' or 'female' \n"))
    cp = int(input("Are you experiencing chest pain? Type in:\n'1' for 'typical angina',\n'2' for 'atypical angina',\n'3' for 'non-anginal pain', or\n'4' for 'asymptomatic' \n"))
    trtbps = int(input("What is your resting blood pressure? \n"))
    chol = int(input("What is your colesteral level? \n"))

    fbs = str(input("Is your blood sugar higher than 120 mg/dl? Type in 'yes' or 'no' \n"))
    restecg = int(input("What are your EKG results? Type in:\n'0' for 'normal',\n'1' for 'ST-T wave abnormality', or\n'2' for 'probable or definite left ventricular hypertrophy'\n"))
    thalachh = int(input("What is your maximum heart rate achieved? \n"))
    exng = int(input("Do you suffer from exercise induced angina? Type in 'yes' or 'no' \n"))
    caa = int(input("Number of major blood vessels: type in 1,2,3 or 4 \n"))

    # ct = ColumnTransformer([
    #     ( 'ordinal', 
    #     OrdinalEncoder(handle_unknown= 'use_encoded_value', unknown_value = -1), 
    #     [1,5,8] ),
    #     ('non_transformed','passthrough',[0,2,3,4,6,7,8,9]) 
    #     ])

    new_data = pd.DataFrame({'age':age,'sex':sex,'cp':cp,'trtbps':trtbps,'chol':chol,
                            'fbs':fbs,'restecg':restecg,'thalachh':thalachh,'exng':exng,'caa':caa-1}, index=[0])

    # new_data = ct.fit_transform(new_data)

    # scaler = StandardScaler()
    # new_data = scaler.transform(new_data)

    preds = np.array(model.predict(new_data))
    print(preds)
    