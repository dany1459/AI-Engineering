import pandas as pd
import numpy as np


successful_directors = df.groupby('director').size()

# content_dict = {'title':[],'rating':[],'total_votes':[],'release_date':[],'duration':[],'description':[],'genres':[],'casts':[],'director':[]}

top_ten = df.sort_values(by=['rating', 'title'], ascending=[False, True]).head(10)
release_director = df.sort_values(by=['release_date', 'director'], ascending=[False, True])
rating_filming = df.sort_values(by=['rating', 'director'], ascending=[False, True])


mean_rating = df['rating'].mean()

# MOST POPULAR ACTORS
flat_list = []
for sublist in df['casts']:
    for item in sublist:
        flat_list.append(item)
print(flat_list)

def most_common(lst):
    return max(set(lst), key=lst.count)

from collections import Counter
split_list = str(flat_list).split()
Counter = Counter(split_list)
most_common_actors = Counter.most_common(10)

print(most_common_actors)


# df.to_csv('D:\movies_data.csv')