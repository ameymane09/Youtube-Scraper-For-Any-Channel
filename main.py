import time
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
SCROLL_PAUSE_TIME = 3


def selenium_setup():
    global driver
    options = webdriver.ChromeOptions()

    # To stop YouTube from detecting Selenium use and blocking us For more info,
    # visit: https://newbedev.com/selenium-webdriver-modifying-navigator-webdriver-flag-to-prevent-selenium-detection
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def scroll_to_bottom():
    html = driver.find_element(By.TAG_NAME, 'html')

    # Get current scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        html.send_keys(Keys.END)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height


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
            "Uploded": views_and_date[1].text,
        }
        data_list.append(data_dict)

    # Convert data to pandas df and download csv file
    data = pd.DataFrame(data_list)
    data.to_csv(f"Soch_channel_video_data_{date.today()}.csv")


def scraper_advanced(url):
    """Get the full data for every video on the channel including its title, views, exact upload date, number of
    comments and first paragraph of the description. """

    driver.get(url)

    scroll_to_bottom()

    links = []
    data_list = []

    # Get every link on the page
    for link in BeautifulSoup(driver.page_source, parser="lxml", parse_only=SoupStrainer('a')):
        if link.has_attr('href'):

            # Add to list if link is for a video
            if "/watch?v=" in link['href']:
                links.append(link['href'])

    # Deleting duplicate values
    links = [*set(links)]

    for link in links:
        # Open a new window
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://www.youtube.com" + link)

        # Wait till the webpage is loaded
        WebDriverWait(driver, 30).until(
            ec.presence_of_element_located((By.ID, "above-the-fold")))

        show_more_button = driver.find_element(By.CSS_SELECTOR, "#expand")
        show_more_button.click()

        # Wait till the description page has expanded
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#collapse")))

        # Move to the bottom of the description to unhide comments section
        html = driver.find_element(By.TAG_NAME, 'html')
        while True:
            html.send_keys(Keys.END)

            # Only break the loop once the comments section is visible
            try:
                driver.find_element(By.XPATH,
                                    '//*[@id="count"]/yt-formatted-string/span[1]').get_attribute("textContent")
            except NoSuchElementException:
                continue
            else:
                break

        soup = BeautifulSoup(driver.page_source, 'lxml')

        title = soup.select_one("#title > h1 > yt-formatted-string").text.strip()
        views = soup.select_one("#info > span:nth-child(1)").text.strip()
        date_uploaded = soup.select_one("#info > span:nth-child(3)").text.strip()
        likes = soup.select_one("#segmented-like-button > ytd-toggle-button-renderer > yt-button-shape > button > div.cbox.yt-spec-button-shape-next--button-text-content > span").text.strip()
        comments = soup.select_one("#count > yt-formatted-string > span:nth-child(1)").text.strip()

        # For age restricted video, description is not available. Hence, skip it.
        try:
            description = soup.select_one("#description-inline-expander > yt-formatted-string > span:nth-child(3)").text.strip()
        except AttributeError:
            description = "Age Restricted Video"

        data_dict = {
            "Title": title,
            "Views": views,
            "Upload Date": date_uploaded,
            "Likes": likes,
            "No. of Comments": comments,
            "Description": description,
        }
        data_list.append(data_dict)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # Convert data to pandas df and store it in a csv file
    video_data = pd.DataFrame(data_list)
    video_data.to_csv(f"Soch_Youtube_Video_Data_{date.today()}.csv")

    driver.quit()


if __name__ == '__main__':
    start = time.time()

    selenium_setup()
    # Put the link of the videos page of the channel
    # scraper_basic("https://www.youtube.com/@sochbymm/videos")
    scraper_advanced("https://www.youtube.com/@sochbymm/videos")

    end = time.time()
    print(f"\n\nTotal time for the program to execute: {round(end - start, 2)}s")



