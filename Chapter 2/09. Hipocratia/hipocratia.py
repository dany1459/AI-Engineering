import numpy    as np
import pandas   as pd

from sklearn.preprocessing   import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.experimental    import enable_hist_gradient_boosting
from sklearn.ensemble        import HistGradientBoostingClassifier

np.random.seed(0)

# load data
df = pd.read_csv('./09. Hipocratia/heart.csv')

# enhance data - numerical categories only
def data_enhancement(data):
    
    gen_data = data.copy()
    
    for i in data['cp'].unique():
        chest_pain_type =  gen_data[gen_data['cp'] == i]
        age = chest_pain_type['age'].std()
        trtbps = chest_pain_type['trtbps'].std()
        chol = chest_pain_type['chol'].std()
        thalachh = chest_pain_type['thalachh'].std()
        
        for j in gen_data[gen_data['cp'] == i].index:
            if np.random.randint(2) == 1:
                gen_data['age'].values[j] += age/10
            else:
                gen_data['age'].values[j] -= age/10
                
            if np.random.randint(2) == 1:
                gen_data['trtbps'].values[j] += trtbps/10
            else:
                gen_data['trtbps'].values[j] -= trtbps/10
                
            if np.random.randint(2) == 1:
                gen_data['chol'].values[j] += chol/10
            else:
                gen_data['chol'].values[j] -= chol/10

            if np.random.randint(2) == 1:
                gen_data['thalachh'].values[j] += thalachh/10
            else:
                gen_data['thalachh'].values[j] -= thalachh/10

    return gen_data


def train():
    # save generated data
    gen = data_enhancement(df)

    # set features and labels
    y = df['output']
    x = df.drop(['output', 'oldpeak', 'slp', 'thall'], axis=1)

    # split the training and test sets
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=0)

    # add 25% of the new generated values
    extra_sample = gen.sample(gen.shape[0] // 4)
    x_train = pd.concat([x_train, extra_sample.drop(['output', 'oldpeak', 'slp', 'thall'], axis=1)])
    y_train = pd.concat([y_train, extra_sample['output']])

    # scale the data
    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_val = scaler.transform(x_val)

    # instantiate the best model
    model = HistGradientBoostingClassifier(verbose=False)

    # train the model
    model.fit(x_train, y_train)

    return model
