from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import re
import io
import time
import pandas as pd


def main():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        driver.get('https://www.baseball-almanac.com/yearmenu.shtml')

        print("Scraping data. Please wait...")

        # Create headers
        headers = ['League', 'Year', 'Type', 'Statistic', 'Name(s)', 'Team(s)', '#', 'Top 25']

        # Create baseball DataFrame
        baseball_df = pd.DataFrame(columns=headers)

        # Create team standings headers
        headers2 = ['League', 'Year', 'Team | Roster', 'W', 'L', 'T', 'WP', 'GB']

        # Create team standings DataFrame
        team_standings = pd.DataFrame(columns=headers2)

        # Inititalize all the main datasets
        baseball_stats = []

        # Find table with the year links
        table = driver.find_element(By.CLASS_NAME, 'ba-table')

        if table:
            # Find all the link elements in the table
            table_links = table.find_elements(By.CSS_SELECTOR, 'a')

            # List to save table results
            table_results = []

            # Access each link and save to dictionary
            for link in table_links:
                values = {}

                values['link'] = link.get_attribute('href')

                # print(values['link'])

                table_results.append(values)


            # Go through results and make a new get request for each link
            for value in table_results:
                try:
                    driver.get(value['link'])

                    # Get the wrapper element that holds the div
                    wrapper = driver.find_element(By.ID, 'wrapper')

                    # Get the container div that holds the statistic data tables 
                    container = wrapper.find_element(By.XPATH, 'child::div[2]')
                    
                    # Get the leaderboard tables of data
                    ba_tables = container.find_elements(By.CLASS_NAME, 'ba-table')

                    # Get the data for hitting and pitching statistics leaderboards
                    data_tables = ba_tables[0:2]

                    i = 0

                    # For both leaderboard tables, perform the following:
                    for table in data_tables:

                        # Extract the year and league
                        first_row = table.find_elements(By.CSS_SELECTOR, 'tr')[0]
                        title = first_row.text
                        year = title.split()[0]
                        league = ' '.join(title.split()[1:3])

                        # Get the outerHTML of the table elements
                        table_html = table.get_attribute('outerHTML')

                        # Use a string io buffer so HTML can be fed to pd.read_html
                        html_buffer = io.StringIO(table_html)

                        # Make table html into pandas data frame
                        panda_table = pd.read_html(html_buffer, skiprows=[0], header=0)[0]
                        table_df = panda_table[:-2].copy()  # Remove last two rows

                        # Set the league, year, and stat type
                        table_df['League'] = league
                        table_df['Year'] = year

                        if i == 0:
                            table_df['Type'] = 'Hitting'
                        else:
                            table_df['Type'] = 'Pitching'

                        # Concat the new table DataFrame to the main baseball_df 
                        baseball_df = pd.concat([baseball_df, table_df], axis=0, ignore_index=True)

                        # To change the stat type for each page and table
                        i += 1

                    # Get team standings
                    s_table = ba_tables[2]
                    s_table_html = s_table.get_attribute('outerHTML')
                    buffer = io.StringIO(s_table_html)
                    p_table = pd.read_html(buffer, skiprows=[0], header=0)[0]
                    p_df = p_table[:-2].copy()
                    p_df['League'] = league
                    p_df['Year'] = year
                    team_standings = pd.concat([team_standings, p_df], axis=0, ignore_index=True)

                    # Prevent rapid requests
                    time.sleep(2)


                except Exception as e:
                    print(f"Exception: {type(e).__name__} {e}")


            # Perform data cleaning

            # Use the values of the 'Name' column to fill the missing values for the 'Name(s)' column
            baseball_df['Name(s)'] = baseball_df['Name(s)'].fillna(baseball_df['Name'])

            # Do the same for the 'Team' and 'Team(s) columns
            baseball_df['Team(s)'] = baseball_df['Team(s)'].fillna(baseball_df['Team'])

            # Drop the 'Name' and 'Team' columns
            baseball_df = baseball_df.drop(columns=['Name', 'Team'])

            # Rename the columns
            baseball_df = baseball_df.rename(columns={'Name(s)': 'Player', 'Team(s)': 'Team', '#': 'Statistic_Value'})

            # Remove front and end whitespace and quotations from player names
            baseball_df['Player'] = baseball_df['Player'].str.strip().str.strip('"')

            # Remove certain rows with values that are not stats
            baseball_df = baseball_df[baseball_df['Team'] != 'NOT on Top List Had Fewer Than ABs']

            # Clean the 'Statistics' and 'Team' column of anything but letters
            baseball_df['Statistic'] = baseball_df['Statistic'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
            baseball_df['Team'] = baseball_df['Team'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
            
            # Convert statistic values to floats
            baseball_df['Statistic_Value'] = pd.to_numeric(baseball_df['Statistic_Value'], errors='coerce')
            baseball_df['Statistic_Value'] = baseball_df['Statistic_Value'].fillna(value=0)

            # Remove any extra columns picked up along with the Top 25 column
            baseball_df = baseball_df.drop(baseball_df.columns[7:], axis=1)
            
            # Remove rows with none values
            baseball_df = baseball_df.dropna()

            baseball_df.info()

            # Clean team standings DataFrame
            team_standings['W'] = team_standings['W'].fillna(team_standings['Wins'])
            team_standings['L'] = team_standings['L'].fillna(team_standings['Losses'])
            team_standings['T'] = team_standings['T'].fillna(team_standings['Ties'])
            team_standings['Team | Roster'] = team_standings['Team | Roster'].fillna(team_standings['Team [Click for roster]'])

            # Drop columns
            team_standings = team_standings.drop(columns=['Wins', 'Losses', 'Ties', 'Team [Click for roster]'])
            
            # Fix column names
            team_standings = team_standings.rename(columns={'W':'Wins', 'L':'Losses', 'T':'Ties', 'Team | Roster':'Team'})

            # Drop extra columns
            team_standings = team_standings.drop(team_standings.columns[6:], axis=1)

            # Convert to numeric
            columns_to_convert = ['Wins', 'Losses', 'Ties']
            team_standings[columns_to_convert] = team_standings[columns_to_convert].apply(pd.to_numeric, errors='coerce')

            # Drop any non numeric rows
            team_standings = team_standings.dropna(subset=columns_to_convert)
            team_standings[columns_to_convert] = team_standings[columns_to_convert].astype(int)

            # Write the hitting and pitching stats and team standings to a csv file
            baseball_df.to_csv('../csv/baseball_stats.csv', index=False)
            team_standings.to_csv('../csv/team_standings.csv', index=False)

            print("Done scraping data.")

        else:
            print("Table not found")

    except Exception as e:
        print(f"Exception: {type(e).__name__} {e}")

    finally:
        driver.quit()  # Close driver
    

if __name__ == '__main__':
    main()
