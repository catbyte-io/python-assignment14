from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get('https://www.baseball-almanac.com/yearmenu.shtml')

    table_results = []

    # Find table with the year links
    table = driver.find_element(By.CLASS_NAME, 'ba-table')

    # Find all the link elements in the table
    table_links = table.find_elements(By.CSS_SELECTOR, 'a')


    # Access each link and click
    for link in table_links:
        values = {}
        values['title'] = link.get_attribute('title')
        values['link'] = link.get_attribute('href')

        print(values['link'])

        table_results.append(values)


    for value in table_results:

        try:
            driver.get(value['link'])

            wrapper = driver.find_element(By.ID, 'wrapper')
            print(wrapper.get_attribute('id'))

            container = wrapper.find_element(By.XPATH, 'child::div[2]')
            print(container.get_attribute('class'))

            time.sleep(10)
        except Exception as e:
            print(f"Exception: {type(e).__name__} {e}")

except Exception as e:
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()
