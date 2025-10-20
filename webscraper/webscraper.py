from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import re
import io
import time
import pandas as pd


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    driver.get('https://www.baseball-almanac.com/yearmenu.shtml')

    # Create headers
    headers = ['League', 'Year', 'Type', 'Statistc', 'Name(s)', 'Team(s)', '#', 'Top 25']

    # Create baseball DataFrame
    baseball_df = pd.DataFrame(columns=headers)

    # Inititalize all the main datasets
    baseball_stats = []

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

            # Get the data for hitting and pitching statistics leaderboards
            data_tables = ba_tables[0:2]

            print("Data table count:")
            print(len(data_tables))

            i = 0

            # For both leaderboard tables, perform the following:
            for table in data_tables:

                table_html = table.get_attribute('outerHTML')

                html_buffer = io.StringIO(table_html)

                panda_table = pd.read_html(html_buffer, skiprows=[0], header=0)[0]
                table_df = panda_table[:-2].copy()

                table_df['League'] = league
                table_df['Year'] = year

                if i == 0:
                    table_df['Type'] = 'Hitting'
                else:
                    table_df['Type'] = 'Pitching'

                print(table_df['Statistic'])

                baseball_df = pd.concat([baseball_df, table_df], axis=0, ignore_index=True)

                baseball_df.info()

                i += 1


            # Prevent rapid requests
            time.sleep(10)


        except Exception as e:
            print(f"Exception: {type(e).__name__} {e}")


    # Write the hitting and pitching stats to a csv file
    baseball_df.to_csv('../csv/baseball_stats.csv', index=False)


except Exception as e:
    print(f"Exception: {type(e).__name__} {e}")

finally:
    driver.quit()  # Close driver
 