from selenium_setup import driver
from scroll_to_bottom import scroll_to_bottom
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def scraper_basic(url):
    """Get the basic details like Title, Views and when video was uploaded (relative to today) from the videos page
    on the channel. """

    driver.get(url)
    data_list = []

    # Wait till the webpage is loaded
    WebDriverWait(driver, 15).until(
        ec.presence_of_element_located((By.CLASS_NAME, "style-scope ytd-channel-name")))

    scroll_to_bottom()

    soup = BeautifulSoup(driver.page_source, 'lxml')
    video_data = soup.find_all("div", class_="style-scope ytd-rich-grid-media", id="meta")

    # Find data about all the videos on the channel
    for video in video_data:
        title = video.find("yt-formatted-string", id="video-title")
        views_and_date = video.find_all('span', class_="inline-metadata-item style-scope ytd-video-meta-block")

        data_dict = {
            "Title": title.text,
            "Views": views_and_date[0].text,
            "Uploaded": views_and_date[1].text,
        }
        data_list.append(data_dict)

    # Convert data to pandas df and download csv file
    data = pd.DataFrame(data_list)
    data.to_csv(f"data/Soch_channel_video_data_basic_{date.today()}.csv")

    driver.quit()
