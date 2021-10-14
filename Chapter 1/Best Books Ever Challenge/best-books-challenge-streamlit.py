import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast
import copy

from streamlit_helpers import *

#import data
data_original = pd.read_csv(r'C:\Users\Igor\Documents\GitHub\Groupwork-Best-Books-Ever-Challenge\best-books.csv')

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
    img{{
    	max-width:60%;
        display: block;
        margin-left: 100px;
        margin-right: auto;
    	margin-bottom:40px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )



#sidebar and headers
logo = Image.open("logo.png")
st.sidebar.image(logo, width=100)
st.sidebar.markdown("# Best Books of all Time")
st.sidebar.markdown("### Anthony Nwachukwu\n### Dan Adrian\n")



# title
st.title("A Study on the Top 5000+ Books of all Time\n\n")



# display all/some data
st.subheader("Interacting with the data")
# ,'awards_length'
disp_options = ['url','title','author','num_reviews','num_ratings','avg_rating','num_pages','original_publish_year','series','genres','awards','places','description','book_index','minmax_norm_ratings','mean_norm_ratings']
disp_options2 = ['url','title','author','avg_rating','num_pages','original_publish_year','series','genres','description']
disp_options3 = ['title','author','minmax_norm_ratings','mean_norm_ratings']
display_data = data[disp_options2]

select_list = st.selectbox('What detail would you like to search for?',('All','Title','Author','Original Publish Year','Series','Genres'),key='All')

if select_list == 'All':
    st.write(display_data)
else:
    select_list = '_'.join(select_list.lower().split())
    selected_option = st.selectbox('Select '+select_list.replace('_',' '), display_data[select_list].sort_values(ascending=False).unique())
    displayed_data = display_data[display_data[select_list] == selected_option]
    st.write(displayed_data)


#Analysis and Plots

# plot 1
st.subheader("Frequent Occurring Words in the Description")
display_data_plot1 = copy.deepcopy(data)
no_words = st.slider('Number of words', 1, 100, 30)
book_option = st.selectbox('Select title', display_data_plot1['title'].sort_values().unique())

text_by_image(display_data_plot1,book_option,no_words,30)



# plot 2
st.subheader("Select Author and Check their Ratings")
display_data_plot2 = display_data.copy()
#Sort by min_max rating of an author // top 2 books
author_option = st.selectbox('Select author', display_data_plot2['author'].unique())
no_of_titles = st.slider('Number of books', 1, 20, 5)
author_Rating = check_author(data[disp_options3], author_option, no_of_titles)
st.write(author_Rating)



# plot 3
st.subheader("Most Successful Authors")

# Plot Authors and their total awards
no_of_authors = st.slider('Select number of authors', 1, 20, 5)
author_awards = data.groupby('author')['awards_length'].sum().sort_values(ascending=False)

author_awards2 = np.array(author_awards.keys())
author_awards3 = np.array(author_awards.values)
author_awards2 = author_awards2[:no_of_authors]
author_awards3 = author_awards3[:no_of_authors]
d = dict(zip(author_awards2,author_awards3))
d = pd.DataFrame(list(d.items()),columns=['Author','Total awards'])
st.write(d)

# author_awards = author_awards.sort_values(by=[''], ascending=False)
# st.bar_chart(author_awards2, height=300,)

# author_awards = data.groupby('author')['awards_length'].sum().sort_values( ascending=False)
# dic_author_awards = dict(zip(author_awards.index, author_awards.values))

# df_author_awards = pd.DataFrame.from_dict(dic_author_awards, orient='index')

# y_label = "total award"
# x_label = "author"
# title = "Authors by Awards"
# df_data = data
# author_awards = make_plot(df_data,x_label, y_label, title, no_of_authors)
# st.pyplot(author_awards)



# # plot 4
st.subheader("Sort by publishing year and get their mean average ratings")

year_ratings = data.groupby('original_publish_year')['minmax_norm_ratings'].mean().sort_values( ascending=False)
no_of_years = st.slider('Select number of years you would like to', 1, 20, 5)

st.bar_chart(year_ratings.head(no_of_years), height=500)


# # plot 5
st.subheader("Sort by author and check who has highest average rating")




# # plot 6
st.subheader("Check if book series are rated better than non series books")



# # plot 7
st.subheader("Check if book series are more ratings than non series books")



# # plot 8
st.subheader("Number of Pages and Year")



# # plot 9
# st.subheader("")



# # plot 10
# st.subheader("")



# # plot 11
# st.subheader("")




# streamlit run best-books-challenge-streamlit.py