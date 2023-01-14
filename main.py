import time
from scraper_basic import scraper_basic
from scraper_advanced import scraper_advanced


if __name__ == '__main__':
    start = time.time()

    # Put the link of the videos page of the channel
    scraper_basic("https://www.youtube.com/@sochbymm/videos")
    # scraper_advanced("https://www.youtube.com/@sochbymm/videos")

    end = time.time()
    print(f"\n\nTotal time for the program to execute: {round(end - start, 2)}s")
