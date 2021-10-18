from numpy import testing
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv(r'C:\Users\Igor\Documents\GitHub\AI-Engineering\Chapter 2\01. Intro to ML\Part 1\data\diabetes.csv')
X = df.drop('Outcome', axis=1)
y = df.Outcome
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# model.classes_

predictions = model.predict(X_test)
print(predictions)
print(y_test)

#### compare and check results

score = accuracy_score(y_test, predictions)
print(score) # should get around 74%
# y.value_counts()

#### SCALING THE DATA

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train.loc[:, :] = scaler.fit_transform(X_train)
X_test.loc[:, :] = scaler.transform(X_test)

model_standard = DecisionTreeClassifier()
model_standard.fit(X_train, y_train)
predictions = model_standard.predict(X_test)

score_standard = accuracy_score(y_test, predictions)
print(score_standard) # should get around 76%