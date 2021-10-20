import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import time

def timed():
    return time.time()

class KNN:
    def __init__(self, n):
        self.n = n

    def euclidean_distances(self, v1, v2):
        return np.linalg.norm(v1-v2)

    def fit(self, x, y):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x,y, test_size=0.2, random_state=0)
        return self

    def predict(self):
        start = timed()
        labels = []

        for i in self.x_test:
            distances = []
            for j in self.x_train:
                d = self.euclidean_distances(i,j)
                distances.append(d)

            df = pd.DataFrame({'distances':distances, 'labels':self.y_train})
            
            l = df.sort_values('distances').head(self.n).groupby('labels').count().sort_values('distances', ascending=False).index[0]
            labels.append(l)

        stop = timed()
        self.time_spent = stop - start
        self.labels = np.array(labels)
        return self.labels
