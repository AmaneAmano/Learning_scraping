"""
Download music files in parallel
"""
import concurrent.futures
import random
import  time
from collections import namedtuple
from os import path
from urllib import parse

import requests

from my_logging import get_my_logger


logger = get_my_logger(__name__)


# define namedtuple for saving the name and data of music file
Music = namedtuple('music', 'file_name, file_content')
# define the interval for each request
RANDOM_SLEEP_TIMES = [x * 0.1 for x in range(10, 40, 5)]

# target URL list
MUSIC_URLS = [
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/01PavanePourUneInfanteDfuntePourPianoMr19.mp3",
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/02JeuxDeauPourPianoMr30.mp3",
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/03SonatinePourPianoMr40-Modr.mp3",
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/04MouvementDeMenuet.mp3",
    "https://archive.org/download/ThePianoMusicOfMauriceRavel/05Anim.mp3"
]


def download(url, timeout=180):
    # extract mp3 file name from url
    parsed_url = parse.urlparse(url)
    file_name = path.basename(parsed_url.path)

    # choice the intervals of requests randomly
    sleep_time = random.choice(RANDOM_SLEEP_TIMES)

    # log output download start
    logger.info(f"[DOWNLOAD START] sleep: {sleep_time} {file_name}")

    time.sleep(sleep_time)

    # download music file
    r = requests.get(url, timeout=timeout)

    # log output download finish
    logger.info(f"[DOWNLOAD FINISHED] {file_name}")

    return Music(file_name=file_name, file_content=r.content)


if __name__ == "__main__":
    # create executor
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        logger.info("[MAIN START]")

        # execute download() in parallel with executor.submit()
        futures = [executor.submit(download, music_url) for music_url in MUSIC_URLS]

        for future in concurrent.futures.as_completed(futures):
            music = future.result()

            with open("data/" + music.file_name, "wb") as fw:
                fw.write(music.file_content)

        logger.info("[MAIN FINISHED]")
