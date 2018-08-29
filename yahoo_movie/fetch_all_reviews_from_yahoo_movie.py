import re
import math
import time
import random
import codecs

import requests
from bs4 import BeautifulSoup


def generate_soup_obj(url, params=None):
    return BeautifulSoup(requests.get(url, params=params).content, "lxml")


def find_total_review_count(movie_url):
    """
    Find a total review count in the target movie.
    :param movie_url: URL of the target movie.
        OK: https://movies.yahoo.co.jp/movie/362714/review/
        NO: https://movies.yahoo.co.jp/movie/未来のミライ/362741/review/
    :return:
    """
    def search_total_review_count_element(target_tag):
        ret = target_tag.name == "small" and\
              target_tag.parent['class'] == ["label"] and \
              not target_tag.string == "〜"
        return ret

    soup = generate_soup_obj(movie_url)
    count_string = soup.find(search_total_review_count_element).string
    return int(re.search(r"([0-9]+)", count_string).group())


def make_review_url_list(movie_url, total_count):
    """
    Make review urls list.
    :param movie_url: Target movie url.
    :param total_count: total review count from find_total_review_count()
    :return: review url list
    """

    result = list()
    pages = math.ceil(total_count / 10)

    for page in range(1, pages+1):
        payload = {"page": page}
        soup = generate_soup_obj(movie_url, params=payload)
        urls = soup.find_all("a", class_="listview__element--right-icon")
        for el in urls:
            url = BASE_URL + el.get("href")
            url = url[:url.index("?")]
            result.append(url)
        time.sleep(random.randint(1, 3))

    return result


def fetch_review_text(review_url, is_string=True):
    """
    Fetch review text.
    :param review_url: Target review url.
    :param is_string: Return value is one line string or not.
    :return: review txt
    """
    soup = generate_soup_obj(review_url)
    element = soup.find("p", class_="text-small text-break text-readable p1em")
    if is_string:
        return element.text.strip()
    else:
        review_string = "".join(list(map(str, element.contents)))
        return review_string.strip().replace("<br/>", "\n")


def write_txt(obj, dist):
    with codecs.open(dist, "w", encoding="utf-8")as fw:
        fw.write("\n".join(obj))


if __name__ == "__main__":
    BASE_URL = "https://movies.yahoo.co.jp"
    MOVIE_URL = "https://movies.yahoo.co.jp/movie/87654/review/"
    DIST = "./sample.txt"

    url_list = make_review_url_list(movie_url=MOVIE_URL,
                                    total_count=find_total_review_count(MOVIE_URL))
    print("Complete making review url list")

    output = []
    for url in url_list:
        text = fetch_review_text(review_url=url, is_string=True)
        output.append(text)
        time.sleep(random.randint(1, 3))
        print(f"Complete: {url}")

    write_txt(output, DIST)