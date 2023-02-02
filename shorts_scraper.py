from selenium_setup import driver
from scroll_to_bottom import scroll_to_bottom
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def shorts_scraper(url, channel_name):

    driver.get(url)

    scroll_to_bottom()

    links = []
    data_list = []

    # Get every link on the page
    for link in BeautifulSoup(driver.page_source, parser="lxml", parse_only=SoupStrainer('a')):
        if link.has_attr('href'):

            # Add to list if link is for a video
            if "/shorts/" in link['href']:
                links.append(link['href'])

    # Deleting duplicate values
    links = [*set(links)]

    print(f"There are {len(links)} shorts on this channel.")

    for link in links:
        # Open a new window
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://www.youtube.com" + link)
        print("https://www.youtube.com" + link)

        # Wait till the short is loaded
        WebDriverWait(driver, 30).until(
            ec.presence_of_element_located((By.ID, "button-shape")))

        # Click the three dots
        more_actions_button = driver.find_element(By.CSS_SELECTOR, "#button-shape > button")
        more_actions_button.click()

        try:
            # Wait till the description button loads
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "#items > ytd-menu-service-item-renderer.style-scope.ytd-menu-popup-renderer.iron-selected > tp-yt-paper-item > yt-formatted-string")))

            # Click the description button
            desc_button = driver.find_element(By.CSS_SELECTOR, "#items > ytd-menu-service-item-renderer.style-scope.ytd-menu-popup-renderer.iron-selected > tp-yt-paper-item > yt-formatted-string")
            desc_button.click()

            # Wait till the description page loads
            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "#factoids > ytd-factoid-renderer:nth-child(1) > div > yt-formatted-string.factoid-value.style-scope.ytd-factoid-renderer")))

            # Start scraping the data
            soup = BeautifulSoup(driver.page_source, 'lxml')

            title = soup.select_one("#shorts-title > yt-formatted-string").text.strip()
            likes = soup.select_one("#factoids > ytd-factoid-renderer:nth-child(1) > div > yt-formatted-string.factoid-value.style-scope.ytd-factoid-renderer").text.strip()
            views = soup.select_one("#factoids > ytd-factoid-renderer:nth-child(2) > div > yt-formatted-string.factoid-value.style-scope.ytd-factoid-renderer").text.strip()
            date_month = soup.select_one("#factoids > ytd-factoid-renderer:nth-child(3) > div > yt-formatted-string.factoid-value.style-scope.ytd-factoid-renderer").text.strip()
            year = soup.select_one("#factoids > ytd-factoid-renderer:nth-child(3) > div > yt-formatted-string.factoid-label.style-scope.ytd-factoid-renderer").text.strip()
            # hashtags = soup.select_one("#description > yt-formatted-string > a:nth-child(4)").text.strip()

            data_dict = {
                "Title": title,
                "Likes": likes,
                "Views": views,
                "Date_Month": date_month,
                "Year": year,
                # "Hashtags": hashtags,
            }
            data_list.append(data_dict)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except TimeoutException:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue

    # Convert data to pandas df and store it in a csv file
    shorts_data = pd.DataFrame(data_list)
    shorts_data.to_csv(f"data/{channel_name}_shorts_data_{date.today()}.csv",
                       index=False)

    driver.quit()
