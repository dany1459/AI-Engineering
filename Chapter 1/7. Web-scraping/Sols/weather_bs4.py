import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from datetime import datetime

url = 'https://weather.com/weather/tenday/l/San+Francisco+CA?canonicalCityId=dfdaba8cbe3a4d12a8796e1f7b1ccc7174b4b0a2d5ddb1c8566ae9f154fa638c'

def scraper(url):
    ''' Scraper pulls data from weather.com '''
    
    page = requests.get(url)  # Requests data from url
    soup = BeautifulSoup(page.content, 'html.parser')   #parsing the content using html since we are working with html

    
    table = soup.find('div', class_='DailyForecast--DisclosureList--msYIJ') #Find the table with the weather data
    ind_container = table.find_all('div', class_='DaypartDetails--Content--hJ52O DaypartDetails--contentGrid--1SWty') #Using this as the parent has a button rolw
    
    days = []
    highs = []
    lows = []
    description = []
   

    def celcify(faranheit):
            temp_int = int(faranheit.split('°')[0])
            celcius = round(5*(temp_int-32)/9)
            return celcius

    for container in ind_container:
        day_item = container.find_all('div')[0].find('h3').text.split(" ")[0]
        days.append(day_item)
        
        # High and Low temperatures, they both have the same class, therefore we can index to focus on each
        temp_high = celcify(container.find_all('div',class_='DailyContent--DailyContent--KcPxD')[0].find('div').find('div').get_text())
        print(temp_high)
        highs.append(temp_high)
        temp_low = celcify(container.find_all('div',class_='DailyContent--DailyContent--KcPxD')[1].find('div').find('div').text)
        lows.append(temp_low)

        #Description of the weather
        des = container.find_all('div')[0].find('p').text
        description.append(des)
        
    
    forecast = {
        'days': days,
        "high": highs,
        "low": lows,
        "description":description
    }

    current_date = datetime.today().strftime('%Y-%m-%d')  # generates the date for today, thereby allowing us to use the function anytime

    df = pd.DataFrame(forecast,index=pd.date_range(current_date,periods=len(forecast['days']),freq='D'))
    df.to_csv('weather_data.csv')
    return df    
    
scraper(url)

