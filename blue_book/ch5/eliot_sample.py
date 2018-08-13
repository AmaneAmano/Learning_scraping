import json
import sys

from eliot import Message, start_action, to_file, write_traceback
import requests

# log output is standard output
to_file(sys.stdout)

PAGE_URL_LIST = [
    "http://eliot.readthedocs.io/en/1.2.0/",
    "http://eliot.readthedocs.io/en/1.2.0/generating/index.html",
    "https://example.com/notfound"
]


def fetch_pages():
    # fetch page contents
    with start_action(action_type="fetch_pages"):
        page_contents = {}
        for page_url in PAGE_URL_LIST:
            with start_action(action_type="dounload", url=page_url):
                try:
                    r = requests.get(page_url, timeout=30)
                    r.raise_for_status()
                except requests.exceptions.RequestException as e:
                    write_traceback()
                    continue
                page_contents[page_url] = r.text
        return page_contents


if __name__ == "__main__":
    page_contents = fetch_pages()
    with open("page_contents.json", "w", encoding="utf-8") as f_page_contents:
        json.dump(page_contents, f_page_contents, ensure_ascii=False)

    Message.log(message_type="info", msg="Saved crawling data")

