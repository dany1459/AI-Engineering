# All imports here
import numpy    as np
from numpy.testing._private.utils import decorate_methods
import pandas   as pd
import seaborn  as sb
import matplotlib.pyplot as plt
import sklearn  as skl
import time

from sklearn import pipeline      # Pipeline
from sklearn import preprocessing # OrdinalEncoder, LabelEncoder
from sklearn import impute
from sklearn import compose
from sklearn import model_selection # train_test_split
from sklearn import metrics         # accuracy_score, balanced_accuracy_score, plot_confusion_matrix
from sklearn import set_config

from sklearn.tree          import DecisionTreeRegressor
from sklearn.ensemble      import RandomForestRegressor
from sklearn.ensemble      import ExtraTreesRegressor
from sklearn.ensemble      import AdaBoostRegressor
from sklearn.ensemble      import GradientBoostingRegressor
from xgboost               import XGBRegressor
from lightgbm              import LGBMRegressor
from catboost              import CatBoostRegressor

# Load the data
data = pd.read_csv(r'C:\Users\Igor\Documents\GitHub\AI-Engineering\Chapter 2\11. Data Enhancement\data\london_merged.csv')

# Set random seed
np.random.seed(0)

# target = data['cnt']
# data = data.drop(['cnt'], axis=1)

# Print data shape
# print(target.shape)
# print(data.shape)

# Take a look at nulls 0 nulls
# print(target.isnull().sum())
# print(data.isnull().sum())

# create 3 new features
# Hour timestamp contains the year, the month and the hour, we will create different columns for each one

data['year'] = data['timestamp'].apply(lambda row: row[:4])
data['month'] = data['timestamp'].apply(lambda row: row.split('-')[2][:2] )
data['hour'] = data['timestamp'].apply(lambda row: row.split(':')[0][-2:] )
'''
print(data['year'])
print(data['month'])
print(data['hour'])
'''
data.drop('timestamp', axis=1, inplace=True)
#print(data.shape)

# Add a feature for apparent temperature ('feels like' temp)
data['pressure'] = data.apply(lambda row: row['hum']/100*6.105* 1**(17.27*row['t1']/(237.7+row['t1'])), axis=1) # Necessary for calculating the apparent temperature
data['apparent_temp'] = data.apply(lambda row: row['t1']+0.33*row['pressure']-0.7*row['wind_speed']-4 ,axis=1)





def data_enhancement(data):
    
    gen_data = data.copy()
    
    for season in data['season'].unique():
        seasonal_data =  gen_data[gen_data['season'] == season]
        hum_std = seasonal_data['hum'].std()
        wind_speed_std = seasonal_data['wind_speed'].std()
        t1_std = seasonal_data['t1'].std()
        t2_std = seasonal_data['t2'].std()
        t2_std = seasonal_data['apparent_temp'].std()
        
        for i in gen_data[gen_data['season'] == season].index:
            if np.random.randint(2) == 1:
                gen_data['hum'].values[i] += hum_std/10
            else:
                gen_data['hum'].values[i] -= hum_std/10
                
            if np.random.randint(2) == 1:
                gen_data['wind_speed'].values[i] += wind_speed_std/10
            else:
                gen_data['wind_speed'].values[i] -= wind_speed_std/10
                
            if np.random.randint(2) == 1:
                gen_data['t1'].values[i] += t1_std/10
            else:
                gen_data['t1'].values[i] -= t1_std/10
                
            if np.random.randint(2) == 1:
                gen_data['t2'].values[i] += t2_std/10
            else:
                gen_data['t2'].values[i] -= t2_std/10
                
            if np.random.randint(2) == 1:
                gen_data['apparent_temp'].values[i] += t2_std/10
            else:
                gen_data['apparent_temp'].values[i] -= t2_std/10

    return gen_data

gen = data_enhancement(data)
#print(gen.shape)

print(data.head(3))
print(gen.head(3))





# Set x and y, and split them
y = data['cnt']
x = data.drop(['cnt'], axis=1)

# Cat & Num variables to be used later
cat_vars = ['season','is_weekend','is_holiday','year','month','weather_code']
num_vars = ['t1','t2','hum','wind_speed','apparent_temp']

x_train, x_val, y_train, y_val = model_selection.train_test_split(x, y,
                                                                test_size=0.2,
                                                                random_state=0  # Recommended for reproducibility
                                                            )





# ADD the generated data
extra_sample = gen.sample(gen.shape[0] // 3)
x_train = pd.concat([x_train, extra_sample.drop(['cnt'], axis=1 ) ])
y_train = pd.concat([y_train, extra_sample['cnt'] ])

# Apply a transform featurewise to make the data more Gaussian-like -> labels only
transformer = preprocessing.PowerTransformer()
y_train = transformer.fit_transform(y_train.values.reshape(-1,1))
y_val = transformer.transform(y_val.values.reshape(-1,1))

# Define pipelines - preprocess num and cat cols
num_4_treeModels = pipeline.Pipeline(steps=[
    ('imputer', impute.SimpleImputer(strategy='constant', fill_value=-9999)),
])

cat_4_treeModels = pipeline.Pipeline(steps=[
    ('imputer', impute.SimpleImputer(strategy='constant', fill_value='missing')),
    ('ordinal', preprocessing.OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value = -1))
])

tree_prepro = compose.ColumnTransformer(transformers=[
    ('num', num_4_treeModels, num_vars),
    ('cat', cat_4_treeModels, cat_vars),
], remainder='drop') # Drop other vars not specified in num_vars or cat_vars





# Create a dictionary with some models
tree_classifiers = {
  "Decision Tree": DecisionTreeRegressor(),
  "Extra Trees":   ExtraTreesRegressor(n_estimators=100, verbose=False),
  "Random Forest": RandomForestRegressor(n_estimators=100, verbose=False),
  "AdaBoost":      AdaBoostRegressor(n_estimators=100),
  "Skl GBM":       GradientBoostingRegressor(n_estimators=100, verbose=False),
  "XGBoost":       XGBRegressor(n_estimators=100),
  "LightGBM":      LGBMRegressor(n_estimators=100),
  "CatBoost":      CatBoostRegressor(n_estimators=100, verbose=False),
}

# Put each model in a pipeline
tree_classifiers = {name: pipeline.make_pipeline(tree_prepro, model) for name, model in tree_classifiers.items()}

# Empty DataFrame where we will store the results
results = pd.DataFrame({'Model': [], 'MSE': [], 'MAE': [], " % error": [], 'Time': []})

# Define the range
rang = abs(y_train.max()) + abs(y_train.min())





# Train all models in a for loop and store the results
for model_name, model in tree_classifiers.items():
    
    start_time = time.time()
    model.fit(x_train, y_train)
    total_time = time.time() - start_time
        
    pred = model.predict(x_val)
    
    results = results.append({"Model":    model_name,
                              "MSE": metrics.mean_squared_error(y_val, pred),
                              "MAE": metrics.mean_absolute_error(y_val, pred),
                              " % error": metrics.mean_squared_error(y_val, pred) / rang,
                              "Time":     total_time},
                              ignore_index=True)

results_ord = results.sort_values(by=['MSE'], ascending=True, ignore_index=True)
results_ord.index += 1 
results_ord.style.bar(subset=['MSE', 'MAE'], vmin=0, vmax=100, color='#5fba7d')





# Print and check results
print(results_ord)

print(y_train.max())
print(y_train.min())
print(y_val[3])
print(tree_classifiers['Random Forest'].predict(x_val)[3])
