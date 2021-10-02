import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://forecast.weather.gov/MapClick.php?x=276&y=148&site=lox&zmx=&zmy=&map_x=276&map_y=148#.YVR4F0hR2Uk'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

div = soup.find_all('div', id='seven-day-forecast-container')

days = []
temp_high = []
temp_low = []
description = []

for i in div:
    p1 = i.find_all('li', class_="forecast-tombstone")
    for j in p1:
        days.append(j.find('p', class_='period-name').text)
        description.append(j.find('p', class_='short-desc').text)
        temp_high.append(j.find('p', class_='temp temp-high'))
        temp_low.append(j.find('p', class_='temp temp-low'))

weather = { 'Day': days,
            'High temperature': temp_high,
            'Low temperature': temp_low,
            'Description': description}

# current_date = datetime.today().strftime('%Y-%m-%d')
df = pd.DataFrame(weather)
df.to_csv('D:\Stuff\CODING\weather.csv')
print(df)