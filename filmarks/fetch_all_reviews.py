"""
Fetch all movie reviews from Filmarks(https://filmarks.com/)

TODO: add logging
TODO: parallel processing
"""
import os
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
    output['title'] = soup.select_one("h2 > span").text
    # Get an original title
    output['original_title'] = soup.select_one(".p-content-detail__main > p").text

    # Get a release date and a running time
    other_info = soup.select(".p-content-detail__other-info > h3")

    for info in other_info:
        label, content = info.text.split("：")
        if label == "上映日":
            output['release_date'] = content.replace("年", "-").replace("月", "-").replace("日", "")
        elif label == "上映時間":
            output['running_time'] = int(content.replace("分", ""))

    # Get countries
    countries = soup.select_one(".p-content-detail__other-info > ul")
    if countries:
        output['countries'] = [c for c in countries.strings]

    # Get genre(s)
    genres = soup.select_one(".p-content-detail__genre > ul")
    if genres:
        output['genres'] = [genre for genre in genres.strings]

    # Get a rating score
    rating_score = soup.select_one(".p-content-detail-state > div > div > div.c-rating__score").text
    if rating_score == "-":
        output['rating_score'] = 0
    else:
        output['rating_score'] = float(rating_score)

    # Get synopsis text
    synopsis = soup.select_one("#js-content-detail-synopsis > p:nth-of-type(2)")
    if synopsis:
        output['synopsis'] = synopsis.text

    # Get staff names
    staff_dict = dict(director=[], writer=[],
                      original_author=[], other=[])
    staffs = soup.select(".p-content-detail__people-list-others__wrapper")

    for staff in staffs:
        role = staff.find("h3").text
        content = [person.text for person in staff.find_all("a")]
        if role == "監督":
            staff_dict['director'] = content
        elif role == "脚本":
            staff_dict['writer'] = content
        elif role == "原作":
            staff_dict['original_author'] = content
        else:
            staff_dict['other'] = content
    output['staffs'] = staff_dict

    # Get cast names
    casts = soup.select_one("#js-content-detail-people-cast > ul")
    if casts:
        output['casts'] = [cast.text for cast in casts.find_all("a")]

    return output


def fetch_last_page(beautiful_soup_object):
    """
    Fetch last page number
    :param beautiful_soup_object:
    :return int: If there aren't any reviews, return 0.
    """
    soup = beautiful_soup_object
    last_page = soup.select_one(".c-pagination__last")
    if last_page:
        return int(last_page.get('href').split("=")[-1])
    else:
        return 0


def fetch_movie_reviews_per_page(beautiful_soup_object):
    """
    Fetch movie reviews per page. Max 10 reviews.
    :param beautiful_soup_object:
    :return list of dict:
    """
    output = []
    review = dict(review_id="",
                  review_text="",
                  posted_date="",
                  rating_score=0)

    soup = beautiful_soup_object

    # Get review_id
    review_ids = soup.select("#mark_id")
    # Get text
    review_texts = soup.select(".p-mark__review")
    # Get posted date
    posted_dates = soup.select(".c-media__content > time")
    # Get  rating score
    rating_scores = soup.select(".c-media__content > div > .c-rating__score")
    if review_texts:
        for review_id, review_text, posted_date, rating_score in zip(review_ids, review_texts,
                                                                     posted_dates, rating_scores):
            review_text = review_text.text.replace("\u3000", "")
            review_id = int(review_id.get("value"))
            posted_date = posted_date.get("datetime")
            if rating_score.text == "-":
                review['rating_score'] = 0
            else:
                rating_score = float(rating_score.text)
                review['rating_score'] = rating_score

            review['review_id'] = review_id
            review['review_text'] = review_text
            review['posted_date'] = posted_date
            output.append(review.copy()) # output.append(review)ではすべての要素が同じになるダメ
    return output


def make_filename(title):
    from pykakasi import kakasi, wakati

    import zen2han

    kakasi = kakasi()
    kakasi.setMode("H", "a")
    kakasi.setMode("K", "a")
    kakasi.setMode("J", "a")
    conv = kakasi.getConverter()
    title = conv.do(title).replace(" ", "_")
    return zen2han.zen2han(title)


def make_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)


def write_json(obj, filename):
    with open(file=f"{DIRNAME}/{filename}.json", mode="w", encoding="utf-8") as fw:
        json.dump(obj=obj, fp=fw, ensure_ascii=False, indent=4)


def main(url):
    make_dir(DIRNAME)

    # Fetch_movie_data
    soup = generate_bs_object(movie_url=url)
    last_page = fetch_last_page(beautiful_soup_object=soup)
    movie_data = fetch_movie_data(movie_url=url, beautiful_soup_object=soup)

    # create filename
    if movie_data['original_title']:
        filename = movie_data['original_title'].lower().replace(" ", "_")
    else:
        filename = make_filename(movie_data['title'])

    # Fetch page=1 reviews
    reviews = fetch_movie_reviews_per_page(beautiful_soup_object=soup)
    review_list = reviews.copy()
    time.sleep(random.randint(1, 3))

    review = dict(total_count=0, reviews=[])
    if last_page == 0:
        review['total_count'] = len(review_list)
        review['reviews'] = review_list
        return write_json(dict(movie=movie_data, reviews=review), filename)
    else:

        for page in range(2, last_page + 1):
            soup = generate_bs_object(movie_url=url, page=page)
            reviews = fetch_movie_reviews_per_page(beautiful_soup_object=soup)
            review_list.extend(reviews)
            time.sleep(random.randint(1, 3))

        review['total_count'] = len(review_list)
        review['reviews'] = review_list
        return write_json(dict(movie=movie_data, reviews=review), filename)


if __name__ == '__main__':
    url = "https://filmarks.com/movies/68895"  # sample url
    DIRNAME = "data"
    main(url)

