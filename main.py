import requests
from bs4 import BeautifulSoup

MOVIE_URL = "https://movies.yahoo.co.jp/movie/362714/review/"

soup = BeautifulSoup(requests.get(MOVIE_URL).content, "lxml")

print(soup.select(''))