import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import sqlite3


# Read database into a DataFrame
with sqlite3.connect('../db/baseball.db') as conn:
    df = pd.read_sql_query('SELECT * FROM baseball_stats', conn)
    standings_df = pd.read_sql_query('SELECT * FROM team_standings', conn)

# Define list options
players = df['Player'].unique()
teams = df['Team'].unique()
leagues = df['League'].unique()
years = df['Year'].unique()

standings_teams = standings_df['Team'].unique()
standings_leagues = standings_df['League'].unique()
standings_years = standings_df['Year'].unique()

player_averages = df.groupby(['Player', 'Statistic'], as_index=False)['Statistic_Value'].mean()
player_averages = player_averages.rename(columns={'Statistic_Value': 'Average_Statistic_Value'})

team_averages = df.groupby(['Team', 'Statistic'], as_index=False)['Statistic_Value'].mean()
team_averages = team_averages.rename(columns={'Statistic_Value': 'Average_Statistic_Value'})


# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Baseball Statistics Dashboard"),

    html.H2("Player Stats"),
    
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

    html.H2("Team Averages"),

    html.Div([
        dcc.Dropdown(
            id='team-dropdown',
            options=[team for team in teams],
            value=teams[0],
            multi=False,
            searchable=True
        )
    ]),

    dcc.Graph(id='team-graph'),

    html.H2("Team Standings"),

    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=[year for year in standings_years],
            value=standings_years[0],
            multi=False,
            searchable=True
        ),

        dcc.RadioItems(
            id='league-radio',
            options=[league for league in standings_leagues],
            value=leagues[0],
            labelStyle={'display': 'block'}
        ),

        dcc.Graph(id='team-performance-graph'),
    ])
])


# Callback for dynamic updates
@app.callback(
    Output('player-graph', 'figure'),
    Input('player-dropdown', 'value'),
)

def update_graph(player):
    # Filter DataFrame based on selections
    filtered_df = player_averages[player_averages['Player'] == player]

    # Create figures
    player_figure = px.bar(filtered_df, x='Statistic', y='Average_Statistic_Value', title=f'Averages for {player}')

    # Narrow the bar if fewer than 3 stats
    if len(filtered_df) < 3:
        player_figure.update_traces(width=.25)

    # Label angle for readability
    player_figure.update_xaxes(tickangle=45)

    return player_figure

@app.callback(
    Output('team-graph', 'figure'),
    Input('team-dropdown', 'value')
)

def update_team_graph(team):
    # Filter
    filtered_df = team_averages[team_averages['Team'] == team]

    # Create figure
    team_figure = px.bar(filtered_df, x='Statistic', y='Average_Statistic_Value', title=f'Averages for {team}')
    team_figure.update_xaxes(tickangle=45)

    return team_figure

@app.callback(
    Output('team-performance-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('league-radio', 'value')]
)

def update_team_performance(year, league):
    # Filter
    filtered_df = standings_df[(standings_df['Year'] == year) & (standings_df['League'] == league)]

    if filtered_df.empty:
        return {
            'data': [],
            'layout': {
                'title': 'No data available for the selected year and league'
            }
        }
    
    # Create chart
    fig = px.bar(
        filtered_df,
        x='Team',
        y=['Wins', 'Losses', 'Ties'],
        title=f'Team Standings for {year} {league}'       
    )
    fig.update_xaxes(tickangle=45)

    return fig


# Start the Dash app
if __name__ == '__main__':
    app.run(debug=True)
