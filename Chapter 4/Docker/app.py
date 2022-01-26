import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

movies = soup.find_all('td', class_="titleColumn")

for movie in movies:
    print(movie.find('a').text)
