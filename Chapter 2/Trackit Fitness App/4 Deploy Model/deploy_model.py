import numpy      as np
import pandas     as pd
import joblib
from collections import Counter

test_data = 'dataset_5secondWindow_TEST.csv'
model_path = 'best_model_lgb78.pkl'

class Trackit:

    def __init__(self, data):
        self.data = data

    def __prepo_data(self):

        df = pd.read_csv(self.data)
        
        indices_to_drop = [0, 2, 44, 45, 46, 47, 48, 49, 50, 51, 59, 67, 68, 69]
        df = df.drop(df.columns[indices_to_drop], axis=1)
        df.columns = df.columns.str.replace('android.sensor.', '').str.replace('#', '_')
    
        return df

    def __predictt(self):

        model = joblib.load(model_path)
        x = self.__prepo_data()

        predictions = model.predict(x)

        return predictions

    def get_activities(self):

        trackit = self.__predictt()

        count = Counter(trackit)

        dictt = dict(count)
        total_activities = sum(dictt.values())

        for act in dictt.keys():
            dictt[act] = round((dictt[act] / total_activities) * 100, 2)

        return dictt

    def get_distances(self):

        distance = self.__prepo_data().iloc[:,-4] * 5 * 1.6 / 3.6
        d1 = np.array(distance)
        d2 = np.array(self.__predictt())

        d_final = pd.DataFrame({'Distance': d1, 'Target': d2})
        total_distances = d_final.groupby('Target')['Distance'].sum()
        total_dist = d_final['Distance'].sum().tolist()

        return total_dist, dict(total_distances)

trackit = Trackit(test_data)
activities_perc_by_time = trackit.get_activities()
total_distance, total_distances_classes = trackit.get_distances()

print(activities_perc_by_time)
