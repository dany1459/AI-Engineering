# All imports done here
import numpy as np
import pandas as pd
import os
from PIL import Image

import time
import numpy    as np
import pandas   as pd

from sklearn import model_selection
from sklearn import metrics

from sklearn.naive_bayes   import MultinomialNB
from sklearn.svm           import SVC
from sklearn.neighbors     import KNeighborsClassifier
from sklearn.tree          import DecisionTreeClassifier
from sklearn.ensemble      import RandomForestClassifier
from catboost              import CatBoostClassifier
from lightgbm              import LGBMClassifier


# ## Uncomment to create a data frame from png files
# # Define the path for the folder containing all images
# path = "C:/Users/Igor/Documents/GitHub/AI-Engineering/Chapter 2/12. Images/MNIST Digit classifier/trainingSet/"
# directories = os.listdir(path)    # get a list of all subdirectories

# df1 = pd.DataFrame()    # data frame to save the tabular data

# for directory in list(directories):       # loop through the list of directories
#     images = os.listdir(path + directory) # get the path for all 10 image directories
#     arr = np.zeros((len(images), 785))    # create a numpy zeros array to append the values for the images later

#     for i, img in enumerate(images):                     # loop through each image directory
#         image = Image.open(path + directory + '/' + img) # get the path for each image
#         arr2 = np.array(image, dtype=float)              # convert the image to a numpy array
#         arr2 = arr2.flatten()                            # reshape the array into 1 dimension

#         arr[i,:784] = arr2          # replace the zeros array with the image data - except last column
#         arr[i,784] = int(directory) # replace last column with the labels data - 0 to 9

#     df2 = pd.DataFrame(data=arr) # save each iteration of the loop into a data frame
#     df = pd.concat([df1, df2])   # add that iteration to another data frame
#     df1 = df                     # final version of the data frame
    
# df.shape
# ## Uncomment to save to CSV file
# # df.to_csv('C:/Users/Igor/Documents/GitHub/AI-Engineering/Chapter 2/12. Images/training_set.csv', index=False)



# Load the CSV file
training_set = pd.read_csv('C:/Users/Igor/Documents/GitHub/AI-Engineering/Chapter 2/12. Images/training_set.csv')

# split the data
y = training_set.iloc[:,-1]    # labels var
x = training_set.iloc[:,:-1]   # features var

# dictionary containing all the models we want to test
tree_classifiers = {
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(verbose=False),
        "CatBoost": CatBoostClassifier(verbose=False),
        "kNN": KNeighborsClassifier(),
        "SVC": SVC(),
        "MultinomialNB": MultinomialNB(),
        "LightGBM": LGBMClassifier()
}       # add as many as you can afford

# define the stratified Kfold params for the cross validation
skf = model_selection.StratifiedKFold(
        n_splits=3,
        random_state=0,
        shuffle=True
)

# define an empty data frame for the results to be saved in
results = pd.DataFrame({'Model': [], 
                        'Accuracy': [], 
                        'Bal Acc.': [], 
                        'Time': []})



# ## USING CROSS VALIDATION
# for model_name, model in tree_classifiers.items(): # loop through all the models in the dict
    
#     start_time = time.time()                                      # start timer
#     pred = model_selection.cross_val_predict(model, x, y, cv=skf) # train and predict with cross_val_predict
#     total_time = time.time() - start_time                         # time each model
    
#     print(f'Finished {model_name} in {round(total_time/60, 2)} minutes')

#     results = results.append({"Model":  model_name,     # save the results
#                               "Accuracy": metrics.accuracy_score(y, pred)*100,
#                               "Bal Acc.": metrics.balanced_accuracy_score(y, pred)*100,
#                               "Time":     total_time},
#                               ignore_index=True)



# ## WITHOUT CROSS VALIDATION
# Split data into train & test/validation sets
x_train, x_val, y_train, y_val = model_selection.train_test_split(
        x, y,
        test_size=0.3,
        random_state=0,
        stratify=y
)

for model_name, model in tree_classifiers.items():

        start_time = time.time()

        model.fit(x_train, y_train)     # fit each model
        pred = model.predict(x_val)     # predict with each model

        total_time = time.time() - start_time

        print(f'Finished {model_name} in {round(total_time/60, 2)} minutes')

        results = results.append({"Model":  model_name,
                                  "Accuracy": metrics.accuracy_score(y_val, pred)*100,
                                  "Bal Acc.": metrics.balanced_accuracy_score(y_val, pred)*100,
                                  "Time":     total_time}, 
                                  ignore_index=True)

# sort the results by accuracy and print them
results_ord = results.sort_values(by=['Accuracy'], ascending=False, ignore_index=True)

print(results_ord)
