import time

import requests

page_url_list = [
    "http://example.com/1.page",
    "http://example.com/2.page",
    "http://example.com/3.page"
]

for page_url in page_url_list:
    res = requests.get(page_url, timeout=30)
    print(f"PageURL: {page_url}, HTTPstatus: {res.status_code}, ProcessingTime: {res.elapsed.total_seconds()}")
    time.sleep(1)