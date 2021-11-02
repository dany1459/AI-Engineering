import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder

def get_data(path):

    data = pd.read_csv(path)

    y = data.values[:,-1]
    y = y.astype('int')

    x_train, x_test, y_train, y_test = train_test_split(data.values[:,:-1], y, test_size=0.2, random_state = 0)

    ct = ColumnTransformer([
        ( 'ordinal', 
        OrdinalEncoder(handle_unknown= 'use_encoded_value', unknown_value = -1), 
        [1,4,5] ),
        ('non_transformed','passthrough',[0,2,3]) 
        ])

    x_train = ct.fit_transform(x_train)
    x_test = ct.transform(x_test)

    return x_train, x_test, y_train, y_test, ct
