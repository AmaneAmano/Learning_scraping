import json

import requests
from bs4 import BeautifulSoup

r = requests.get("https://pypi.org/rss/updates.xml")
soup = BeautifulSoup(r.content, "xml")

recent_updates = []
tmp = {}
for item in soup.find_all('item'):
    title, version = item.title.text.split(" ")
    tmp['title'] = title
    tmp['version'] = version
    tmp['link'] = item.link.text
    tmp['description'] = item.description.text
    tmp['pubDate'] = item.pubDate.text
    recent_updates.append(tmp.copy())

print(recent_updates)
