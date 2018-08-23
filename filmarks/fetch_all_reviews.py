import random
import time
import json

import requests
from bs4 import BeautifulSoup


def generate_bs_object(movie_url, page=1):
    """
    Generate a BeautifulSoup object
    :param str movie_url: a target movie url in Filmarks
    :param int page: page_number
    :return:
    """
    r = requests.get(movie_url, params={"page": page})
    return BeautifulSoup(r.content, "lxml")


def fetch_movie_data(movie_url, beautiful_soup_object):
    """
    Fetch movie data
    Items:
    - movie_id: int
    - url: str
    - title: str
    - original title(if any): str
    - release date: str
    - running time: int
    - countries: list of str
    - genres(if any): list of str
    - rating score: float
    - synopsis: str
    - staffs(ex. director, writer, original author): dict of list of str
    - casts: list of str
    :param str movie_url: a target movie url in Filmarks
    :param bs4.BeautifulSoup beautiful_soup_object:
    :return dict:
    """
    soup = beautiful_soup_object

    output = dict(movie_id=int(movie_url.split("/")[-1]),
                  url=movie_url,
                  title="", original_title="",
                  release_date="", countries="", running_time=0,
                  genres=[],
                  rating_score=0.0,
                  synopsis="",
                  staffs={}, casts=[]
                  )
    # Get a title
    output['title'] = soup.select_one("body > div.l-main > div > div.p-content-detail__head > div >"
                            " div.p-content-detail__body > div.p-content-detail__main > h2 > span").text
    # Get an original title
    output['original_title'] = soup.select_one("body > div.l-main > div > div.p-content-detail__head >"
                                     " div > div.p-content-detail__body > div.p-content-detail__main > p").text
    # Get a release date and a running time
    other_info = soup.select("body > div.l-main > div > div.p-content-detail__head > div >"
                             " div.p-content-detail__body > div.p-content-detail__main >"
                             " div.p-content-detail__other-info > h3")

    for info in other_info:
        label, content = info.text.split("：")
        if label == "上映日":
            output['release_date'] = content.replace("年", "-").replace("月", "-").replace("日", "")
        elif label == "上映時間":
            output['running_time'] = int(content.replace("分", ""))

    # Get countries
    countries = soup.select_one("body > div.l-main > div >"
                                " div.p-content-detail__head > div > div.p-content-detail__body >"
                                " div.p-content-detail__main > div.p-content-detail__other-info > ul")
    if countries:
        output['countries'] = [c for c in countries.strings]

    # Get genre(s)
    genres = soup.select_one("body > div.l-main > div > div.p-content-detail__head > div >"
                             " div.p-content-detail__body > div.p-content-detail__main >"
                             " div.p-content-detail__genre > ul")
    if genres:
        output['genres'] = [genre for genre in genres.strings]

    # Get a rating score
    rating_score = soup.select_one("body > div.l-main > div > div.p-content-detail__head >"
                                   " div > div.p-content-detail__body > div.p-content-detail__main >"
                                   " div.p-content-detail-state > div > div > div.c-rating__score").text
    if rating_score == "-":
        output['rating_score'] = 0
    else:
        output['rating_score'] = float(rating_score)

    # Get synopsis text
    synopsis = soup.select("#js-content-detail-synopsis > p:nth-of-type(2)")
    if synopsis:
        output['synopsis'] = synopsis[0].text

    # Get staff names
    staff_dict = dict(director=[], writer=[], orginal_author=[])
    staffs = soup.select("body > div.l-main > div > div.p-content-detail__head >"
                         " div > div.p-content-detail__body > div.p-content-detail__main >"
                         " div.p-content-detail__people-list > div.p-content-detail__people-list-others__wrapper > div")
    for staff in staffs:
        label = staff.find("h3").text
        content = [person.text for person in staff.find_all("a")]
        if label == "監督":
            staff_dict['director'] = content
        elif label == "脚本":
            staff_dict['writer'] = content
        elif label == "原作":
            staff_dict['original_author'] = content
    output['staffs'] = staff_dict

    # Get cast names
    casts = soup.select("#js-content-detail-people-cast > ul")
    if casts:
        output['casts'] = [cast.text for cast in casts[0].find_all("a")]

    return output


def fetch_last_page(beautiful_soup_object):
    """
    Fetch last page number
    :param beautiful_soup_object:
    :return int: If there aren't any reviews, return 0.
    """
    soup = beautiful_soup_object
    last_page = soup.select_one("body > div.l-main > div > div.p-content-detail__foot >"
                                " div.p-main-area.p-timeline > div.c-pagination > a.c-pagination__last")
    if last_page:
        return int(last_page.get('href').split("=")[-1])
    else:
        return 0


def fetch_movie_reviews_per_page(beautiful_soup_object):
    """
    Fetch movie reviews per page. Max 10 reviews.
    :param beautiful_soup_object:
    :return dict:
    """
    output = dict()

    soup = beautiful_soup_object
    reviews = soup.select("body > div.l-main > div > div.p-content-detail__foot >"
                          " div.p-main-area.p-timeline > div > div.p-mark__review")
    for review_id, review in zip(soup.select("#mark_id"), reviews):
        review_id = review_id.get("value")
        review = review.text.replace("\u3000", "")
        output[review_id] = review
    return output


def write_json(obj, movie_id):
    with open(file=f"data/{movie_id}.json", mode="w", encoding="utf-8") as fw:
        json.dump(obj=obj, fp=fw, ensure_ascii=False, indent=4)


def main(url):
    # Fetch_movie_data
    soup = generate_bs_object(movie_url=url)
    last_page = fetch_last_page(beautiful_soup_object=soup)
    movie_data = fetch_movie_data(movie_url=url, beautiful_soup_object=soup)

    movie_id = url.split("/")[-1]

    # When last_page == 0, no reviews have yet been posted.
    if last_page == 0:
        return write_json(dict(movie=movie_data, review={}), movie_id)
    else:
        # Fetch page=1 reviews
        reviews = fetch_movie_reviews_per_page(beautiful_soup_object=soup)
        reviews_container = reviews
        time.sleep(random.randint(1, 3))

        for page in range(2, last_page + 1):
            soup = generate_bs_object(movie_url=url, page=page)
            reviews = fetch_movie_reviews_per_page(beautiful_soup_object=soup)
            reviews_container.update(reviews)
            time.sleep(random.randint(1, 3))

        return write_json(dict(movie=movie_data, review=reviews_container), movie_id)


if __name__ == '__main__':
    url_list = [f"https://filmarks.com/movies/{random.randint(2000, 60000)}" for _ in range(10)]

    for url in url_list:
        print(url)
        main(url)
