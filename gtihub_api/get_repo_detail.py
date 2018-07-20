import emoji
import os
from dotenv import load_dotenv
import requests

# Prepare api keys and endpoint
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
GITHUB_API_KEY = os.environ.get('GITHUB_API_KEY')
ENDPOINT = 'https://api.github.com/graphql'


def execute_query(api_key, query, endpoint='https://api.github.com/graphql'):
    """
    Execute query to GitHub GraphQL API.
    :param api_key: git hub api key. you can use personal access token.
    :param query:  the graphl query consists of a multi-line string.
    :param endpoint: github graphql endpoint. default setting.
    :return: json type response
    """
    headers = {'Authorization': f'token {api_key}'}
    response = requests.post(endpoint, json={'query': query}, headers=headers)
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
    {{
      repository(owner: {owner_name}, name: {repo_name}){{
        name,
        nameWithOwner,
        description,
        createdAt,
        forkCount,
        homepageUrl,
        }}
    }}
    """
    return query


query = create_query_to_repo(owner_name="vuejs", repo_name="vue")

json_data = execute_query(GITHUB_API_KEY, query, ENDPOINT)

print(json_data)

