import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler

def get_data(path):

    data = pd.read_csv(path)

    y = data.values[:,-1]
    y = y.astype('int')

    x_train, x_test, y_train, y_test = train_test_split(data.values[:,:-1], y, test_size=0.2, random_state = 0)

    # ct = ColumnTransformer(
    #             [(
    #             'ordinal', 
    #             OrdinalEncoder(handle_unknown= 'use_encoded_value', unknown_value = -1), 
    #             [1,4,5]
    #             )], 
    #             'passthrough')

    ct = ColumnTransformer( [('ordinal', 
        OrdinalEncoder(handle_unknown= 'use_encoded_value', unknown_value = -1), 
        [1,4,5] ),
        ('non_transformed','passthrough',[0,2,3])] )



    x_train = ct.fit_transform(x_train)
    x_test = ct.transform(x_test)

    # print(x_train)
    return x_train, x_test, y_train, y_test, ct
path = (r"C:\Users\Igor\Documents\GitHub\AI-Engineering\Chapter 2\08. Gradient Boosting and Encoding\insurance.csv")
get_data(path)