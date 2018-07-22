import re

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_animal_names"

soup = BeautifulSoup(requests.get(url=URL).content, "lxml")

def is_tag_a_and_parent_td(tag):
    return tag.name == "a" and tag.parent.name == "td"

result = []

for tag in soup.find_all(is_tag_a_and_parent_td):
    result.append(tag.string)

print(result)