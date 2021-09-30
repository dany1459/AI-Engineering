import pandas as pd
import numpy as np


# df = pd.read_csv('')

data = {'Movie': ['f1','f2','f3','f4','f5','f6','f7','f8','f9','f10'],
        'Genre': ['Action'],
        'Duration': [122,144,123,152,163,182,111,101,98,124],
        'Description': ['bla','gdgdf','gdf','ghfdkh','rewi','iuyfds','tnkwen','bfkj','tyew','nvn'],
        'Release Date': [2020,1955,1987,1989,2002, 2010,2011,1995,1977,1989],
        'Director': ['Jim','ge','tre','rew','qwer','asd','dfg','tyu','iop','tyr'],
        'Actors': [['John', 'is', 'the'],['son', 'of', 'John'],['second', 'Second', 'son'],['of', 'John', 'second'], ['is', 'William', 'second'],['John', 'is', 'the'],['son', 'of', 'John'],['second', 'Second', 'son'],['of', 'John', 'second'],['is', 'William', 'second']],
        'Rating': [9,6,7,7,4,9,7,5,7,10],
        'Gross': [11,22,33,44,55,66,77,88,99,101]
        }

# data = {'Movie': [],
#         'Genre': [],
#         'Duration': [],
#         'Description': [],
#         'Release Date': [],
#         'Director': [],
#         'Actors': [],
#         'Rating': [],
#         'Filming Duration': [],
#         'Gross': []
#         }

# df = pd.DataFrame(data, columns=['Movie','Genre','Duration','Description','Release Date','Director','Actors','Rating','Filming Duration','Gross'])
# print(df)

labels = [np.arange(1, len(data['Movie'])+1)]
df = pd.DataFrame(data, index=labels)

successful_directors = df.groupby('Director').size()

top_ten = df.sort_values(by=['Rating', 'Gross'], ascending=[False, True]).head(10)
release_director = df.sort_values(by=['Release Date', 'Director'], ascending=[False, True])#.head(10) maybe showing only top 10s is easier on the eye, for all of these
rating_filming = df.sort_values(by=['Rating', 'Director'], ascending=[False, True])

mean_gross = df['Gross'].mean()
mean_rating = df['Rating'].mean()
worst_success = df[(df['Gross'] >= mean_gross) & (df['Rating'] < mean_rating)]
most_appreciated = df[(df['Rating'] >= mean_rating) & (df['Gross'] < mean_gross)]

# MOST POPULAR ACTORS
flat_list = []
for sublist in df['Actors']:
    for item in sublist:
        flat_list.append(item)
print(flat_list)

def most_common(lst):
    return max(set(lst), key=lst.count)

from collections import Counter
split_list = str(flat_list).split()
Counter = Counter(split_list)
most_common_actors = Counter.most_common(5)

print(most_common_actors)


# df.to_csv('D:\Stuff\CODING\IMDB Challenge\movies_data.csv')