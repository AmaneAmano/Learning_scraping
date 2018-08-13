import random
import time
from os import path
from urllib import parse

import requests

from celery import Celery
from pydub import AudioSegment

from my_logging import get_my_logger


logger = get_my_logger(__name__)

RANDOM_SLEEP_TIMES = [x * 0.1 for x in range(10, 40, 5)]

ARTIST_NAME = "Maurice RAVEL"
ALBUM_NAME = "The Piano Music of Maurice Ravel from archive.org"

MUSIC_URLS = [
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/01PavanePourUneInfanteDfuntePourPianoMr19.mp3",
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/02JeuxDeauPourPianoMr30.mp3",
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/03SonatinePourPianoMr40-Modr.mp3",
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/04MouvementDeMenuet.mp3",
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/05Anim.mp3"
]

app = Celery('crawler_with_celery_sample', broker='redis://localhost:6370/0')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Tokyo',
    enable_utc=True,
    worker_max_tasks_per_child=1,
    result_expires=60,
    worker_redirect_stdouts=False,
    task_soft_time_limit=180,
    task_routes={
        'crawler_with_celery_sample.download': {
            'queue': 'download',
            'routing_key': 'download',
        },
        'crawler_with_celery_sampl.cut_mp3': {
            'queue': 'media',
            'routing_key': 'media',
        },
    },
)


@app.task(bind=True, max_retries=2, default_retry_delay=10)
def download(self, url, timeout=180):
    try:
        parsed_url = parse.urlparse(url)
        file_name = path.basename(parsed_url.path)

        sleep_time = random.choice(RANDOM_SLEEP_TIMES)

        logger.info(f"[DOWNLOAD START] sleep: {sleep_time} {file_name}")

        time.sleep(sleep_time)

        r = requests.get(url, timeout=timeout)
        with open(file_name, 'wb') as fw:
            fw.write(r.content)

        logger.info(f"[DOWNLOAD FINISHED] {file_name}")

        cut_mp3.delay(file_name)
    except requests.exceptions.RequestException as e:
        logger.error(f"[DOWNLOAD ERROR - RETRY] file: {file_name}, e: {e}")
        raise self.retry(exc=e, url=url)


@app.task
def cut_mp3(file_name):
    logger.info(f"[cut_mp3 START] {filename}")

    music = AudioSegment.from_mp3(file_name)

    head_time = 2 * 1000
    head_part = music[:head_time]
    root_name, ext = path.splitext(file_name)

    file_handler = head_part.export(
        root_name + "_head" + ext,
        format="mp3",
        tags={
            'title': root_name,
            'artist': ARTIST_NAME,
            'album': ALBUM_NAME,
        }
    )
    file_handler.close()
    logger.info(f"[cut_mp3 FINISHED] {file_name}")


if __name__ == "__main__":
    logger.info("[MAIN START]")

    for music_url in MUSIC_URLS:
        download.delay(music_url)

    logger.info("[MAIN FINISHED]")