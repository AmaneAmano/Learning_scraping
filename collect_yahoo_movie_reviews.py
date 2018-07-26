import re

import requests
from bs4 import BeautifulSoup

BASE_URL = u"https://movies.yahoo.co.jp/movie/未来のミライ/362741/review/"


def get_total_review_count(base_ulr):
    soup = BeautifulSoup(requests.get(base_ulr).content, "lxml")

    def detect_total_review_count(tag):
        return tag.name == "small" and tag.parent['class'] == ["label"] and not tag.string == "〜"

    return int(re.search(r"([0-9]+)", soup.find(detect_total_review_count).string).group())


def get_review_urls(page_url):
    soup = BeautifulSoup(requests.get(page_url).content, "lxml")

    review_urls = []
    links = soup.find_all("a", class_="listview__element--right-icon")
    for link in links:
        link = link.get('href')
        link = link[:link.find("?")]
        review_urls.append(f"https://movies.yahoo.co.jp{link}")

    return review_urls

