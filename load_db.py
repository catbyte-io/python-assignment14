import sqlite3
import pandas as pd


def import_to_db():

    df = pd.read_csv('./csv/baseball_stats.csv')

    df.info()

    american_league_df = df[df['League'] == 'American League']

    national_league_df = df[df['League'] == 'National League']

    players_df = df[['Player', 'Team']].drop_duplicates().reset_index(drop=True)

    stats_df = df[['Type', 'Statistic']].drop_duplicates().reset_index(drop=True)


    with sqlite3.connect('./db/baseball.db') as conn:

        df.to_sql('baseball_stats', conn, if_exists='replace', index=False)

        players_df.to_sql('players', conn, if_exists='replace', index=False)
        stats_df.to_sql('statistics', conn, if_exists='replace', index=False)

        american_league_df.to_sql('american_league', conn, if_exists='replace', index=False)
        national_league_df.to_sql('national_league', conn, if_exists='replace', index=False)


if __name__ == '__main__':
    import_to_db()
