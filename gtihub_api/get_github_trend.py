"""
Get repositories listed in GitHub trending(https://github.com/trending).
"""
import re
import codecs
import json

from bs4 import BeautifulSoup
import requests


def create_trend_repository_list():
    """
    Create now trending repository list from https://github.com/trending
    :return: [trend repo list]
    """
    soup = BeautifulSoup(requests.get("https://github.com/trending").content, "lxml")
    return soup.find_all(class_="col-12 d-block width-full py-4 border-bottom")


def extract_repository_data(repository_list):
    """
    Extract repository data(owner name, repository name, url, today stars).
    :param repository_list: now trending repository list from create_trend_repository_list().
    :return: dictionary type
    """
    output = dict()
    today_stars_pattern = r"([0-9]+) stars today"

    if repository_list == []:
        raise Exception("Failed to load repository list. Is repository list void?")
    else:
        for repo in repository_list:
            # create repository url
            repo_url_relative = repo.find("a")["href"]
            repo_url = "https://github.com" + repo_url_relative

            # extract repository owner name and repository name from relative path
            owner, repo_name = repo_url_relative.split("/")[1:]

            # find and get today stars. 'today_stars' var has today stars as int type.
            today_stars = str(repo.find("span", class_="d-inline-block float-sm-right"))
            today_stars = int(re.findall(pattern=today_stars_pattern, string=today_stars)[0])

            output[repo_name] = {"owner": owner, "name": repo_name, "repo_url": repo_url, "today_stars": today_stars}
        return output


def write_json(dist, obj):
        """
        Write dictionary type data to json file.
        :param dist: path to json file (relative path)
        :param obj: dictionary type data
        :return: none
        """
        with codecs.open(dist, "w", "utf-8") as f:
            # Open with codecs and set ensure_ascii=False, Japanese will be output correctly.
            json.dump(obj, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    path = "./data/github_trend.json"

    repo_list = create_trend_repository_list()
    repo_list = extract_repository_data(repo_list)

    write_json(path, repo_list)



