import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

import sqlite3


# Read database into a DataFrame
with sqlite3.connect('../db/baseball.db') as conn:
    df = pd.read_sql_query('SELECT * FROM baseball_stats', conn)

df.info()
print("Baseball stats")
print(df.head())

players = df['Player'].unique()
print("Players")
print(players)

player_averages = df.groupby(['Player', 'Statistic'], as_index=False)['Statistic_Value'].mean()
player_averages = player_averages.rename(columns={'Statistic_Value': 'Average_Statistic_Value'})

player_totals = df.groupby(['Player', 'Statistic'], as_index=False)['Statistic_Value'].sum()
player_totals = player_totals.rename(columns={'Statistic_Value': 'Total_Statistic_Value'})

best_hitters = df[df['Type'] == 'Hitting'].sort_values(by='Statistic_Value', ascending=False).head(20)


# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Player Statistics Dashboard"),
    
    html.Div([
        dcc.Dropdown(
            id='player-dropdown',
            options=[player for player in players],
            value=players[1],
            multi=False,
            searchable=True
        ),
    ]),
    
    dcc.Graph(id='player-graph'),
])


# Callback for dynamic updates
@app.callback(
    Output('player-graph', 'figure'),
    Input('player-dropdown', 'value')
)

def update_graph(player):
    # Filter DataFrame based on selections
    filtered_df = player_averages[player_averages['Player'] == player]

    # Create figures
    player_figure = px.bar(filtered_df, x='Statistic', y='Average_Statistic_Value', title=f'Averages for {player}')

    if len(filtered_df) < 3:
        player_figure.update_traces(width=.25)
    return player_figure


# Start the Dash app
if __name__ == '__main__':
    app.run(debug=True)
