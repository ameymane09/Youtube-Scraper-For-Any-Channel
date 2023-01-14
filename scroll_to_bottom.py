from selenium_setup import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
SCROLL_PAUSE_TIME = 3


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
