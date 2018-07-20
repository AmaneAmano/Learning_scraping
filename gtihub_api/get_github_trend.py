from bs4 import BeautifulSoup
import requests
import re


output = dict()

response = requests.get("https://github.com/trending")

soup = BeautifulSoup(response.content, "lxml")

repo_list = soup.find_all(class_="col-12 d-block width-full py-4 border-bottom")

pattern = r"([0-9]+) stars today"


for repo in repo_list:
    repo_url_relative = repo.find("a")["href"]
    repo_url = "https://github.com" +  repo_url_relative
    owner, repo_name = repo_url_relative.split("/")[1:]

    tmp = str(repo.find("span", class_="d-inline-block float-sm-right"))
    today_stars = int(re.findall(pattern=pattern, string=tmp)[0])
    print(owner, repo_name, repo_url)
    print(today_stars)
    print("=" * 50)