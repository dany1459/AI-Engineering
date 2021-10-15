import pandas as pd
import ast
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import streamlit as st
# import plotly.express as px


def min_max_normalization(df_min_max):
    df_min_max = 1 + (df_min_max - df_min_max.min()) / (df_min_max.max() - df_min_max.min()) * 9
    return round(df_min_max, 2)

def mean_normalization(df_min_max):
    df_min_max = 1 + (df_min_max - df_min_max.mean()) / (df_min_max.max() - df_min_max.min()) * 9
    return round(df_min_max, 2)

def check_author(df, author, no_of_author):
    df = df.loc[df.author == author]
    df.sort_values(by=['minmax_norm_ratings'], ascending=[False])
    return df.head(no_of_author)

# Plot Authors and their total awards
def make_plot(df, x_label, y_label, title, st, kind):
    plt.style.use('ggplot')
    plt.rc('font', size=15)
    
    if kind != 'pie':
        fig, ax = plt.subplots(figsize=(12,10))
        ax = df.plot(kind=kind)
        ax.set_ylabel(y_label)
        ax.set_xlabel(x_label)
    else:
        pie_labels = df.index.values
        pie_data=df.values
        fig, ax = plt.subplots(figsize=(8,5))
        ax.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', shadow=False)
        ax.axis('equal')

    ax.set_title(title+'\n')
    st.pyplot(fig)


def text_by_image(df,option,count=100,id=all):
    # if id is all:
    #     text = ' '.join([str(d) for d in df])
    # else:
    #     text = df[id]
    text = df['description'][df.title == option].values[0]

    # Create and generate a word cloud image:
    wordcloud = WordCloud(max_font_size=50, max_words=count, background_color="white").generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.write(fig)

### Get genre and places total counts and mean average ratings

def tranform_places_genres(df):

    genres_rating = {}
    genres_counts = {}

    places_rating = {}
    places_counts = {}

    genres,places,minmax_norm_ratings = df.genres, df.places, df.minmax_norm_ratings

    for id in range(len(minmax_norm_ratings)):
        clean_genre = ast.literal_eval(genres[id])
        clean_places = ast.literal_eval(places[id])
        if len(clean_genre) != 0:
            for ng in clean_genre:
                for i in ng.split('>'):
                    genr = i.strip()
                    if genr in genres_rating:
                        genres_rating[genr].append(minmax_norm_ratings[id])
                    else:
                        genres_rating[genr] = [minmax_norm_ratings[id]]
                    if genr in genres_counts:
                        genres_counts[genr] += 1
                    else:
                        genres_counts[genr] = 1
        #for places
        if len(clean_places) != 0:
            for cp in clean_places:
                plac = cp.strip()
                if plac in places_rating:
                    places_rating[plac].append(minmax_norm_ratings[id])
                else:
                    places_rating[plac] = [minmax_norm_ratings[id]]
                if plac in places_counts:
                    places_counts[plac] += 1
                else:
                    places_counts[plac] = 1

    #genres
    for g in genres_rating.keys():
        genres_rating[g] = np.round(np.mean(genres_rating[g]),decimals=3)

    dic_genres_rating = dict(zip(genres_rating.keys(), genres_rating.values()))
    df_genres_rating = pd.DataFrame.from_dict(dic_genres_rating, orient='index',\
        columns=['minmax_norm_ratings']).sort_values(by='minmax_norm_ratings',ascending=False)
    

    dic_genres_counts = dict(zip(genres_counts.keys(), genres_counts.values()))
    df_genres_counts = pd.DataFrame.from_dict(dic_genres_counts, orient='index',\
        columns=['total_counts']).sort_values(by='total_counts',ascending=False)

    #places
    for g in places_rating.keys():
        places_rating[g] = np.round(np.mean(places_rating[g]),decimals=3)

    dic_places_rating = dict(zip(places_rating.keys(), places_rating.values()))
    df_places_rating = pd.DataFrame.from_dict(dic_places_rating, orient='index',\
        columns=['minmax_norm_ratings']).sort_values(by='minmax_norm_ratings',ascending=False)

    dic_places_counts = dict(zip(places_counts.keys(), places_counts.values()))
    df_places_counts = pd.DataFrame.from_dict(dic_places_counts, orient='index',\
        columns=['total_counts']).sort_values(by='total_counts',ascending=False)

    return df_genres_rating, df_genres_counts, df_places_rating, df_places_counts
# mean_ratings