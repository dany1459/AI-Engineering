import pandas as pd
import ast
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px





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
def make_plot(df, x_label, y_label, title, st, n=all):
    # plt.style.use('ggplot')
    if n is all:
        n = df.shape[0]
    fig, ax = plt.subplots(figsize=(12,10))

    x = list(df.head(n).keys().values)
    y = list(df.head(n).values)

    ax.bar(x,y,legend=None,figsize=(12,5))
    ax.ylabel(y_label)
    ax.xlabel(x_label)
    ax.title(title)
    st.pyplot(fig)
    
    # plt.xticks(rotation=50)

def plot_pages_year(df,start,end,interval,n=all,kind='bar'):
    df_year_pages = df.groupby(pd.cut(df.index, np.arange(start-interval, end+interval, interval))).sum()
    y_label = "average rating"
    x_label = "number of reviews"
    title = "Number of Pages by Year"
    make_plot(df_year_pages,x_label, y_label, title, n=n, kind=kind)

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