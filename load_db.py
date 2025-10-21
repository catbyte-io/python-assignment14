import sqlite3
import pandas as pd


def import_to_db():

    df = pd.read_csv('./csv/baseball_stats.csv')
    df.info()

    standings_df = pd.read_csv('./csv/team_standings.csv')
    standings_df.info()


    with sqlite3.connect('./db/baseball.db') as conn:

        df.to_sql('baseball_stats', conn, if_exists='replace', index=False)

        standings_df.to_sql('team_standings', conn, if_exists='replace', index=False)


if __name__ == '__main__':
    import_to_db()
