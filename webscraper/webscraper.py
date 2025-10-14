from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get('https://www.baseball-almanac.com/yearmenu.shtml')

    table_results = []

    table = driver.find_element(By.CLASS_NAME, 'ba-table')

    table_links = table.find_elements(By.CSS_SELECTOR, 'a')

    for link in table_links:
        values = {}
        values['title'] = link.get_attribute('title')
        values['link'] = link.get_attribute('href')

        # Click on link and save data

           


except Exception as e:
    print("Could not find website.")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()