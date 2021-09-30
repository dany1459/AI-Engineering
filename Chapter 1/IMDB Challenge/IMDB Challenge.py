from selenium import webdriver
import pandas as pd
from dateutil.parser import parse
import datetime
import numpy as np

my_driver = "chromedriver.exe"

op = webdriver.ChromeOptions()
op.add_argument('headless')

url = 'https://www.imdb.com/search/title/?genres=action&groups=top_1000&sort=user_rating,desc&view=simple'
driver = webdriver.Chrome(my_driver,options=op)
driver.implicitly_wait(3)
driver.get(url)
content =  driver.find_elements_by_class_name('lister-item')

#collect in dictionary
content_dict = {'title':[],'rating':[],'total_votes':[],'release_date':[],'duration':[],'description':[],'genres':[],'casts':[],'director':[]}

#for each item do:
for tem_i in range(len(content)):

    print("====item: "+str(tem_i)+"===")

    #back to base url
    url = 'https://www.imdb.com/search/title/?genres=action&groups=top_1000&sort=user_rating,desc&view=simple'
    driver = webdriver.Chrome(my_driver,options=op)
    driver.implicitly_wait(1)
    driver.get(url)

    #title
    title_year =  content[tem_i].find_element_by_class_name('col-title')
    title = title_year.find_element_by_tag_name('a')
    title = title.text
    content_dict['title'].append( title )

    #rating
    rating =  content[tem_i].find_element_by_class_name('col-imdb-rating')
    rating = rating.find_element_by_tag_name('strong')
    rating = rating.get_attribute("title")
    content_dict['rating'].append( rating.split()[0] )
    content_dict['total_votes'].append( rating.split()[3] )

    #Follow the link of movie i
    image =  content[tem_i].find_element_by_class_name('lister-item-image')
    image_a = image.find_element_by_tag_name('a')
    url = image_a.get_attribute("href")

    driver = webdriver.Chrome(my_driver,options=op)
    driver.implicitly_wait(1)
    driver.get(url)

    #general_info
    general_info = driver.find_element_by_xpath('.//div[@class="TitleMainBelowTheFoldGroup__TitleMainPrimaryGroup-sc-1vpywau-1 btXiqv ipc-page-grid__item ipc-page-grid__item--span-2"]')


    #release date
    release_date = general_info.find_element_by_xpath('.//section[@data-testid="Details"]')
    release_date = release_date.find_element_by_xpath('.//div[@data-testid="title-details-section"]')
    release_date = release_date.find_element_by_xpath('.//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')
    content_dict['release_date'].append( release_date.text.split('(')[0] )

    #duration
    duration = general_info.find_element_by_xpath('.//section[@data-testid="TechSpecs"]')
    duration = duration.find_element_by_xpath('.//div[@data-testid="title-techspecs-section"]')
    duration = duration.find_element_by_xpath('.//li[@data-testid="title-techspec_runtime"]')
    duration = duration.find_element_by_xpath('.//li[@class="ipc-inline-list__item"]')
    content_dict['duration'].append( duration.text )

    #description
    description = general_info.find_element_by_xpath('.//section[@data-testid="Storyline"]')
    description = description.find_element_by_xpath('.//div[@class="Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty"]')
    description = description.find_element_by_xpath('.//div[@data-testid="storyline-plot-summary"]')
    description = description.find_element_by_xpath('.//div[@class="ipc-html-content ipc-html-content--base"]')
    content_dict['description'].append( description.text )

    #genre
    genre = general_info.find_element_by_xpath('.//section[@data-testid="Storyline"]')
    genre = genre.find_element_by_xpath('.//div[@class="Storyline__StorylineWrapper-sc-1b58ttw-0 iywpty"]')
    genre = genre.find_element_by_xpath('.//li[@data-testid="storyline-genres"]')
    genre = genre.find_elements_by_xpath('.//li[@class="ipc-inline-list__item"]')
    genres = [i.text for i in genre]
    content_dict['genres'].append( genres )

    #cast
    cast = general_info.find_element_by_xpath('.//section[@data-testid="title-cast"]')
    cast = cast.find_element_by_xpath('.//div[@class="ipc-shoveler title-cast__grid"]')
    cast = cast.find_element_by_xpath('.//div[@class="ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid"]')
    cast = cast.find_elements_by_xpath('.//div[@data-testid="title-cast-item"]')
    casts = [i.find_element_by_xpath('.//a[@data-testid="title-cast-item__actor"]').text for i in cast]
    content_dict['casts'].append( casts )

    #director
    director = general_info.find_element_by_xpath('.//section[@data-testid="title-cast"]')
    director = director.find_element_by_xpath('.//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all StyledComponents__CastMetaDataList-y9ygcu-10 cbPPkN ipc-metadata-list--base"]')
    director = director.find_elements_by_tag_name('li')[0]
    director = director.find_element_by_xpath('.//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')
    content_dict['director'].append( director.text )

print(content_dict.keys())


labels = [np.arange(1, len(content_dict['Movie'])+1)]
df = pd.DataFrame(content_dict, index=labels)




successful_directors = df.groupby('Director').size()

top_ten = df.sort_values(by=['Rating', 'Gross'], ascending=[False, True]).head(10)
release_director = df.sort_values(by=['Release Date', 'Director'], ascending=[False, True])
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
most_common_actors = Counter.most_common(10)

print(most_common_actors)


df.to_csv('D:\Stuff\CODING\IMDB Challenge\movies_data.csv')