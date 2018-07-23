import os

from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv


def call_api(query, oauth, count=50):
    endpoint = "https://api.twitter.com/1.1/search/tweets.json"
    params = {"q": query,
              "lang": "ja",
              "result_type": "recent",
              "count": count}
    return oauth.get(endpoint, params=params).json()


def get_search_results(res):
    values = res['statuses']
    result = []
    for value in values:
        result.append((value['user']['name'], value['text'], value['created_at']))
    return result


if __name__ == "__main__":
    # Prepare api keys and endpoint
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)
    TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    twitter_oauth = OAuth1Session(client_key=TWITTER_CONSUMER_KEY,
                                  client_secret=TWITTER_CONSUMER_SECRET,
                                  resource_owner_key=TWITTER_ACCESS_TOKEN,
                                  resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET)

    q = "カレー 華麗"

    response = call_api(q, twitter_oauth, count=5)
    [print(v) for v in get_search_results(response)]