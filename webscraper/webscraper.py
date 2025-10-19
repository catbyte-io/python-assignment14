from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import re
import time
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get('https://www.baseball-almanac.com/yearmenu.shtml')

    # Inititalize all the main datasets
    baseball_stats = []
    team_standings = []

    # Find table with the year links
    table = driver.find_element(By.CLASS_NAME, 'ba-table')

    # Find all the link elements in the table
    table_links = table.find_elements(By.CSS_SELECTOR, 'a')

    # List to save table results
    table_results = []

    # Access each link and click
    for link in table_links:
        values = {}
        values['title'] = link.get_attribute('title')
        values['link'] = link.get_attribute('href')

        # print(values['link'])

        table_results.append(values)


    # Go through results and make a new get request for each link
    for value in table_results:

        try:
            driver.get(value['link'])

            # Get the league
            league = value['title'].split()[-2:]
            league = ' '.join(league)

            # Get the year
            match = re.search(r'(\d{4})', value['title'])
            year = match.group(1)

            # Get the wrapper element that holds the div
            wrapper = driver.find_element(By.ID, 'wrapper')

            # Get the container div that holds the statistic data tables 
            container = wrapper.find_element(By.XPATH, 'child::div[2]')
            
            # Get the leaderboard tables of data
            ba_tables = container.find_elements(By.CLASS_NAME, 'ba-table')

            # Get the data for hitting statistics leaderboard
            data_tables = ba_tables[0:2]

            print("Data Tables")
            print(data_tables)

            for table in data_tables:
                data_rows = table.find_elements(By.CSS_SELECTOR, 'tr')
                print(len(data_rows))

                data_headers = []

                headers = table.find_elements(By.CLASS_NAME, 'banner')
                for header in headers:
                    header_text = header.text
                    data_headers.append(header_text)
            
                data_headers = data_headers[:len(data_headers)//2]

                print("Headers:")
                print(data_headers)

                print(len(data_rows))


                for each in data_rows[2:-2]:  # Skips the title and header rows

                    columns = []
                    
                    td_elements = each.find_elements(By.CSS_SELECTOR, 'td')

                    for one in td_elements:
                        col = one.text
                        columns.append(col)

                    print(columns)

                    row = {}

                    row['league'] = league
                    row['year'] = year
                    row['statistic'] = columns[0]
                    row['name'] = columns[1]
                    row['team'] = columns[2]
                    row['value'] = columns[3]

                        
                    baseball_stats.append(row)


            # Prevent rapid requests
            time.sleep(10)

        except Exception as e:
            print(f"Exception: {type(e).__name__} {e}")


    # Create DataFrame for hitting data leaderboard
    baseball_stats_df = pd.DataFrame(baseball_stats)
    baseball_stats_df.info


except Exception as e:
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()
 