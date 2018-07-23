import requests
from bs4 import BeautifulSoup

URL = "https://movies.yahoo.co.jp/review/"
BASE_URL = "https://movies.yahoo.co.jp"

soup = BeautifulSoup(requests.get(url=URL).content, "lxml")

links = soup.find_all("a", class_="listview__element--right-icon")

review_urls = []
for link in links:
    review_urls.append(f"{BASE_URL}{link.get('href')}")

results = []
for review_url in review_urls:
    soup = BeautifulSoup(requests.get(url=review_url).content, "lxml")
    results.append(soup.find("p", class_="text-small text-break text-readable p1em").text.strip())

[print(result) for result in results]