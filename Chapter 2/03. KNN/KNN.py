import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from time import time

def timed():
    return time()

class KNN:
    def __init__(self, k):
        self.k = k

    def __euclidean_distances(self, v1, v2):
        return np.linalg.norm(v1-v2)

    def fit(self, x, y):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x,y, test_size=0.2, random_state=0)
        return self

    def predict(self, X):

        start = timed()

        labels = []

        for i in X:
            distances = []
            for j in self.x_train:
                d = self.__euclidean_distances(i,j)
                distances.append(d)

            df = pd.DataFrame({'distances':distances, 'labels':self.y_train})
            
            l = df.sort_values('distances').head(self.k).groupby('labels').count().sort_values('distances', ascending=False).index[0]
            labels.append(l)

        self.labels = np.array(labels)

        end = timed()
        print('Time elapsed: {:.2f} seconds.'.format(end-start))
        
        return self.labels
