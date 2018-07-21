"""
Get detail data of user's repositories using GitHub REST API v3
More information about Github REST API v3 is here https://developer.github.com/v3/
"""
import os
import json
import codecs

from dotenv import load_dotenv
import requests

# Prepare api keys
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY')


def create_endpoint(developer_name):
    """
    Create the endpoint to user's repos.
    :param developer_name: developer name of repos. owner.
    :return: endpoint url
    """
    if not developer_name:
        raise ValueError("Owner name is empty")
    else:
        return f"https://api.github.com/users/{developer_name}/repos"


def call_api(endpoint):
    """
    Call GitHub REST API v3. List user's repositories.
    More information about GitHub REST API v3 User's Repos is here https://developer.github.com/v3/repos/
    :param endpoint: endpoint url. https://api.github.com/users/:username/repos
        Example
        https://api.github.com/users/crimnut02/repos
    :return: response json type
    """
    headers = {'Authorization': f'token {GITHUB_API_KEY}', 'Accept': "application/vnd.github.mercy-preview+json"}
    return requests.get(endpoint, headers=headers).json()


def extract_repos_detail(repositories):
    """
    Extract detail data about repositories.
    Data items:
        Repository name
        Repository full name
        Description
        URL to repository
        Homepage url
        Main language
        Languages used in repository
        Stars count
        Forks
        Forks count
        Topics(tags)
        License
    :param repositories: repository list. get from call_api()
    :return: dictionary type. Key is repository name. Each Value has above data items.
    """
    output = dict()

    for repo in repositories:
        name = repo['name']
        output[name] = {'name': name, 'full_name': repo['full_name'], 'description': repo['description'],
                        'repo_url': repo['html_url'], 'homepage_url': repo['homepage'],
                        'main_language': repo['language'], 'languages_url': repo['languages_url'],
                        'stars_count': repo['stargazers_count'],
                        'forks': repo['forks'], 'forks_count': repo['forks_count'],
                        'topics': repo['topics'], 'license': repo['license']}
    return output


def write_json(dist, obj):
    """
    Write data about repository from GitHub API to json file.
    :param dist: path to json file (relative path)
    :param obj: dictionary type data. get from extract_repo_detail()
    :return: none
    """
    with codecs.open(dist, "w", "utf-8") as f:
        # Open with codecs and set ensure_ascii=False, Japanese will be output correctly.
        json.dump(obj, f, ensure_ascii=False, indent=4)


def load_json(path):
    with codecs.open(path, "r", "utf-8") as f:
        json_data = json.load(f)
    return json_data


if __name__ == "__main__":
    DIST = './data/repos_detail.json'
    PATH = './data/github_trend.json'

    OWNER = "facebook"
    url = create_endpoint(OWNER)
    repos = call_api(url)
    result = extract_repos_detail(repos)
    write_json(dist=DIST, obj=result)