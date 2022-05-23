import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

DATA_PATH = r'C:\Users\Igor\Documents\GitHub\football-app\website\data\epl.csv'
df = pd.read_csv(DATA_PATH)
df = df.drop(columns=['Unnamed: 0']) 
x = df.drop(['FTR'], axis=1)
y = df['FTR']

cols = ['HTHG', 'HTAG', 'HTP', 'ATP', 'HomeTeamLP', 'AwayTeamLP', 'DiffPts', 'DiffLP']
scaler = StandardScaler().fit(x.loc[:, cols])
x.loc[:, cols] = scaler.transform(x.loc[:, cols])

x = pd.get_dummies(data=x, columns=['HomeTeam', 'AwayTeam'])
# print(x.head())
encoder = LabelEncoder()
y = encoder.fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=20, random_state=0, stratify=y)

clf = GradientBoostingClassifier()
clf.fit(x_train, y_train)

pickle.dump(clf, open('model.pkl', 'wb'))
pickle.dump(scaler, open('scaler.pkl', 'wb'))
