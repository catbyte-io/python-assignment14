# python-assignment14
CTD Assignment 14 Webscraping and Dashboard

This project scrapes data from the Baseball Almanac website
The data includes hitting and pitching leaderboard data along with team standings for each year and league.

## Step 1: Clone the respository
Move into a directory to hold the repository
Enter the following command:
`git clone git@github.com:catbyte-io/python-assignment14.git`

## Step 2: Create a virtual environment and install dependencies
Move into the `python-assignment14` directory
Create a python virtual environment
`python -m venv .venv`
Activate the environment
`source .venv/bin/activate`
Install dependencies
`pip install -r requirments.txt`

## Step 3: Use the webscraper
Move into the `webscraper` directory
`cd webscraper`
Excecute the program
`python webscraper.py`
Wait for webscraping to complete. There should be two csv files created in the `csv` directory: `baseball_stats.csv` and `team_standings.csv`

## Step 4: Load the database
Navigate back to the `python-assignment14` directory
Execute the database loading program
`python load_db.py`
There should be one database file created in the `db` directory: `baseball.db`

## Step 5: Use the dashboard
Navigate into the `dashboard` directory
`cd dashboard`
Run the dashboard program
`python dashboard.py`
View the dashboard app by navigating to 'http://127.0.0.1:8050/' in the web browser.
Use the dropdown menu for the first graph to choose a player to view average stats for.
Use the dropdown menu for the second graph to view the average stats for a specific team.
Use the third dropdown to select a year and use the radio buttons to select a league to view team standings wins vs. losses.

## Step 6: (Optional) Use the database query tool
Navigate back to the `python-assignment14` directory.
Execute the program
`python sql_query.py`
The program shows the available database tables
Enter SQL commands and queries ending with ';'
Type 'exit;' when done.
