from selenium_setup import driver
from scroll_to_bottom import scroll_to_bottom
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


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
    video_data.to_csv(f"data/Soch_Youtube_Video_Data_Advanced_{date.today()}.csv")

    driver.quit()
