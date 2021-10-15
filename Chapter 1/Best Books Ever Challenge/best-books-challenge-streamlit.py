import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
# import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast
import copy
import datetime

from streamlit_helpers import *

#import data
data_original = pd.read_csv('best-books-final.csv')

# Add column of min_max rating normalization
minmax_norm_ratings = min_max_normalization(data_original['avg_rating'])
data_original['minmax_norm_ratings'] = minmax_norm_ratings

# Add column of mean normalization
mean_norm_ratings = mean_normalization(data_original['avg_rating'])
data_original['mean_norm_ratings'] = mean_norm_ratings

# Add column for number of awards
data = data_original.copy()
data = data.replace({'awards': {np.nan: 0}})

d = []
for i in data.index:
    if data.loc[i, "awards"] == 0:
        d.append(0)
    else:
        d.append( len( ast.literal_eval(data.loc[i, "awards"]) ) )
data['awards_length'] = d

data['series'] = data['series'].replace({True,False}, {'Series', 'Non-Series'})



#set css styling  
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 90%;
        padding-top: 5rem;
        padding-right: 5rem;
        padding-left: 5rem;
        padding-bottom: 5rem;
    }}
    .sidebar .sidebar-content{{
        max-width:100%;
        display: block;
        margin-left: auto;
        margin-right: auto;
    	margin-bottom:100px;
    }}
    img{{
    	max-width:60%;
        display: block;
        margin-left: auto;
        margin-right: auto;
    	margin-bottom:100px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

#sidebar and headers
logo = Image.open("books-generic_1468008c.jpg")
st.sidebar.image(logo,use_column_width='auto')
st.sidebar.markdown("# Best Books of all Time\n### -A Study By-")
st.sidebar.markdown("# Anthony Nwachukwu\n# Dan Adrian Dobre\n")



# title
st.title("A Study on the Top 5,000+ Books of all Time")



# display all/some data
st.subheader("Play around with the data, have some fun")
# ,'awards_length'
disp_options = ['url','title','author','num_reviews','num_ratings','avg_rating','num_pages','original_publish_year','series','genres','awards','places','description','book_index','minmax_norm_ratings','mean_norm_ratings']
disp_options2 = ['title','author','avg_rating','num_pages','original_publish_year','series','genres']
disp_options3 = ['title','author','minmax_norm_ratings','mean_norm_ratings']

data = data.replace({'places': {np.nan: '[]'}})
# data = data.replace({'genres': {True: 'Series', False:'Non Series'}})

data = data.replace({'original_publish_year': {np.nan: 0}})
data = data.replace({'num_pages': {np.nan: 0}})
now = datetime.datetime.now()
now_year = now.year
data['original_publish_year'] = data['original_publish_year'] .apply(lambda x: int(x) if x <= now_year else 0)
data['num_pages'] = data['num_pages'] .apply(lambda x: int(x))

display_data = data[disp_options2]

select_list = st.selectbox('What details would you like to search for?',('All','Title','Author','Original Publish Year','Series','Genres'),key='All')

if select_list == 'All':
    st.write(display_data)
else:
    select_list = '_'.join(select_list.lower().split())
    selected_option = st.selectbox('Select '+select_list.replace('_',' '), display_data[select_list].sort_values(ascending=True).unique())
    displayed_data = display_data[display_data[select_list] == selected_option]
    st.write(displayed_data)


#Analysis and Plots

# plot 1
st.subheader("Frequently occurring words in the summary")
display_data_description = copy.deepcopy(data)
no_words = st.slider('Number of words', 1, 100, 30)
book_option = st.selectbox('Select title', display_data_description['title'].sort_values().unique(), key='PLK')

word_display_data_description = text_by_image(display_data_description,book_option,no_words,30)



# plot 2: Plot Authors and their mean average ratings

st.subheader("Authors with quality publications")

select_list_author_rating = st.selectbox('Select the plot',('Bar','Pie','Line','Horizontal Bar'),key='Pie')
charts_author_rating = {'Bar':'bar','Pie':'pie','Line':'line','Horizontal Bar':'barh'}

no_of_authors_author_rating = st.slider('Select number of authors', 1, 50, 10, key='NV')
data_author_rating = data.groupby('author')['minmax_norm_ratings'].mean().sort_values(ascending=False).head(no_of_authors_author_rating)

y_label_author_rating = "Rating"
x_label_author_rating = "Author"
title_author_rating = f"Top {no_of_authors_author_rating} Authors by their Average Rating"

author_awards_author_rating = make_plot(data_author_rating, x_label_author_rating, y_label_author_rating,\
     title_author_rating, st, kind=charts_author_rating[select_list_author_rating])



# plot 3: Plot Authors and their total awards

st.subheader("Most successful authors")

select_list = st.selectbox('Select the plot',('Bar','Pie','Line','Horizontal Bar'),key='Horizontal Bar')
charts = {'Bar':'bar','Pie':'pie','Line':'line','Horizontal Bar':'barh'}

no_of_authors = st.slider('Select number of authors', 1, 50, 20, key='YH')
author_awards = data.groupby('author')['awards_length'].sum().sort_values(ascending=False).head(no_of_authors)

y_label = "Total Number of Awards"
x_label = "Authors"
title = f"{no_of_authors} Authors with the Most Awards"

author_awards = make_plot(author_awards, x_label, y_label, title, st, kind=charts[select_list])



#plot 4
st.subheader("Years with more quality in publications")

select_list = st.selectbox('Select the plot',('Bar','Pie','Line','Horizontal Bar'),key='Line')
charts = {'Bar':'bar','Pie':'pie','Line':'line','Horizontal Bar':'barh'}
min_year = int(sorted([i for i in data.original_publish_year if i > 0])[0])

min_year = st.number_input('From', min_value=1, max_value=now_year, value=1400, step=1)
max_year = st.number_input('To', min_value=min_year+1, max_value=now_year, value=1600, step=1)

year_rating = data.groupby(['original_publish_year'], as_index=False)['minmax_norm_ratings'].mean().sort_values(by='minmax_norm_ratings', ascending=False)
year_rating = year_rating.loc[(year_rating['original_publish_year'] >= int(min_year)) & (year_rating['original_publish_year'] <= int(max_year))]
year_rating.set_index('original_publish_year', inplace=True)
year_rating = year_rating['minmax_norm_ratings']

y_label = "Average Rating"
x_label = "Publishing Year"
title = "Publishing Year by Average Rating"

year_ratings = make_plot(year_rating, x_label, y_label, title, st, kind=charts[select_list])


# # plot 6
st.subheader("Are series more loved than non-series books?")
select_list = st.selectbox('Select the plot',('Pies','Bar'),key='Pies')
charts = {'Pies':'pie','Bar':'bar'}
series_ratings = data.groupby('series')['minmax_norm_ratings'].mean().sort_values( ascending=True)
y_label = "Rating"
x_label = "Books"
title = "Comparison by the Average Rating"
series_ratings = make_plot(series_ratings, x_label, y_label, title, st, kind=charts[select_list])



# # plot 7
st.subheader("Are non-series more common than series books?")
select_list = st.selectbox('Select the plot',('Pie','Bar'),key='Pie')
charts = {'Bar':'bar','Pie':'pie'}
series_counts = data.groupby('series').size().sort_values( ascending=False)
y_label = "Total number"
x_label = "Books"
title = "Total Number of Books"
series_ratings = make_plot(series_counts, x_label, y_label, title, st, kind=charts[select_list])


#for next plots
df_genres_rating, df_genres_counts, df_places_rating, df_places_counts = tranform_places_genres(data)

# # plot 8 ###
st.subheader("How does book volume change over the years")

df_year = data.original_publish_year

d=data[['original_publish_year','num_pages']].groupby(by='original_publish_year').sum().sort_values('original_publish_year')

select_list = st.selectbox('Select the plot',('Line Plot','Bar','Pie','Horizontal Bar'),key='Lines Plot')
charts = {'Bar':'bar','Pie':'pie','Line Plot':'line','Horizontal Bar':'barh'}

start = st.number_input('From', min_value=1, max_value=now_year, value=1500, step=1)
time_interval = st.number_input('Year Interval', min_value=1, max_value=now_year-1, value=50, step=1)
last = st.number_input('To', min_value=start+1, max_value=now_year, value=2000, step=1)

df_year_pages = d.groupby(pd.cut(d.index, np.arange(start-time_interval, last+time_interval, time_interval))).sum()
y_label = "Total Number of Pages"
x_label = "Years"
title = "Number of Pages by Year"
make_plot(df_year_pages['num_pages'], x_label, y_label, title, st, kind=charts[select_list])



# # plot 9 Plot Genres and their mean average ratings
st.subheader("Genres most loved by readers")
select_list = st.selectbox('Select the plot',('Horizontal Bar','Bar','Pie','Lines'),key='Horizontal Bar')
charts = {'Bar':'bar','Pie':'pie','Lines':'line','Horizontal Bar':'barh'}
no_of_genres = st.slider('Select number of genres', 1, 25, 10, key='IU')
y_label = "Genres"
x_label = "Average Rating"
title = f"Top {no_of_genres} Genre by Average Rating"
genres_rating = make_plot(df_genres_rating['minmax_norm_ratings'].head(no_of_genres), x_label, y_label, title, st, kind=charts[select_list])



# # plot 10 Plot Genres and their total counts
st.subheader("Most common genres")
select_list = st.selectbox('Select the plot',('Pie chart','Horizontal Bar','Bar Chart','Lines'),key='Pie chart')
charts = {'Bar Chart':'bar','Pie chart':'pie','Lines':'line','Horizontal Bar':'barh'}
no_of_counts = st.slider('Select number of genres to display', 1, 25, 10,key='AS')
y_label = "Genre"
x_label = "Number of Occurances"
title = f'Top {no_of_counts} Genres'
genres_rating = make_plot(df_genres_counts['total_counts'].head(no_of_counts), x_label, y_label, title, st, kind=charts[select_list])



# # plot 11 Plot Places and their mean average ratings
st.subheader("Locations compared by the average rating of the books they feature in")
select_list = st.selectbox('Select the plot',('Horizontal Bar','Bar Chart','Pie chart','Lines'),key='Bar chart')
charts = {'Bar Chart':'bar','Pie chart':'pie','Lines':'line','Horizontal Bar':'barh'}
no_of_places1= st.slider('Select number of locations', 1, 25, 10, key='RT')
y_label = "Locations"
x_label = "Average Rating"
title = f"Top {no_of_places1} Locations"
places_rating = make_plot(df_places_rating['minmax_norm_ratings'].head(no_of_places1), x_label, y_label, title, st, kind=charts[select_list])



# # plot 12 Plot Places and their mean average ratings
st.subheader("Where does the action of most books take place?")
select_list = st.selectbox('Select the plot',('Horizontal Bars','Bar Charts','Pie charts','Lines','Horizontal Bars'),key='Bar charts')
charts = {'Bar Charts':'bar','Pie charts':'pie','Lines':'line','Horizontal Bars':'barh'}
no_of_places2 = st.slider('Select number of locations', 1, 25, 10,key='ER')
y_label = "Locations"
x_label = "Number of Occurances"
title = f"Top {no_of_places2} Most Popular Locations"
places_counts= make_plot(df_places_counts['total_counts'].head(no_of_places2), x_label, y_label, title, st, kind=charts[select_list])



# streamlit run best-books-challenge-streamlit.py