import sqlite3
import pandas as pd


def import_to_db():

    df = pd.read_csv('../csv/baseball_stats.csv')

    df.info()

    american_league_df = df[df['League'] == 'American League']

    national_league_df = df[df['League'] == 'National League']

    players_df = df['Player', 'Team'].drop_duplicates().reset_index(drop=True)

    stats_df = df['Type', 'Statistic'].drop_duplicates().reset_index(drop=True)


    with sqlite3.connect('../db/baseball.db') as conn:

        df.to_sql('baseball_stats', if_exists='replace')

        players_df.to_sql('players', if_exists='replace')
        stats_df.to_sql('statistics', if_exists='replace')

        american_league_df.to_sql('american_league', if_exists='replace')
        national_league_df.to_sql('national_league', if_exists='replace')


