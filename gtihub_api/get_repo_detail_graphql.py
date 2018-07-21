"""
Get detail data of github repository using GitHub GraphQL API v4
More information about Github GraphQL API v4 is here https://developer.github.com/v4/
"""
import os
from dotenv import load_dotenv
import requests

# Prepare api keys and endpoint
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY')
ENDPOINT = 'https://api.github.com/graphql'


def execute_query(api_key, query_string, endpoint='https://api.github.com/graphql'):
    """
    Execute query to GitHub GraphQL API.
    :param api_key: GitHub api key. You can use personal access token.
    :param query_string:  the GitHub GraphQL query consists of a multi-line string.
    :param endpoint: GitHub GraphAL endpoint. default setting.
    :return: json type response
    """
    headers = {'Authorization': f'token {api_key}'}
    response = requests.post(endpoint, json={'query': query_string}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def create_query_to_repo(owner_name, repo_name):
    """
    Create query to repository.
    :param owner_name: repository owner name
    :param repo_name: repository name
    :return: query
    """
    query = f"""
    query {{
      repository(owner: {owner_name}, name: {repo_name}){{
        name,
        nameWithOwner,
        description,
        createdAt,
        forkCount,
        homepageUrl
        }}
    }}
    """
    return query


query = create_query_to_repo(owner_name="crimnut02", repo_name="aframe-mmd")

json_data = execute_query(GITHUB_API_KEY, query, ENDPOINT)

print(json_data)

