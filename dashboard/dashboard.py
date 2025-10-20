import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


df = pd.read_csv('../csv/baseball_stats.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Player Statistics Dashboard"),
    
    html.Div([
        dcc.Dropdown(
            id='player-dropdown',
            options=[{'label': player, 'value': player} for player in df['Player'].unique()],
            value='',  # Default value
            multi=False
        ),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Statistic', 'value': 'Statistic'},
                {'label': 'Type', 'value': 'Type'}
            ],
            value='Statistic_Value',  # Default value
            multi=False
        )
    ]),
    
    dcc.Graph(id='player-graph'),
    dcc.Graph(id='metric-graph')
])

# Callback for dynamic updates
@app.callback(
    [Output('player-graph', 'figure'),
     Output('metric-graph', 'figure')],
    [Input('player-dropdown', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_graphs(selected_player, selected_metric):
    # Filter DataFrame based on selections
    filtered_df = df[df['Player'] == selected_player]

    # Create figures
    player_figure = px.bar(filtered_df, x='Player', y=selected_metric, title=f'{selected_metric} of {selected_player}')
    metric_figure = px.line(df, x='Player', y=selected_metric, title=f'{selected_metric} Comparison')

    return player_figure, metric_figure

# Start the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
