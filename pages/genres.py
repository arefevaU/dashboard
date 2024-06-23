from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import data as df

def page_layout():
    layout = html.Div([
            html.H3('Анализ по жанрам и категориям', style = {'margin-bottom':'2rem', 'text-align':'center'}),
            html.Div([
                dcc.Graph(
                    id='genre_distribution_movies',
                    figure=px.pie(df.genre_counts_movies, values='count', names='listed_in', 
                                title='Распределение фильмов по жанрам'), style={'padding':'10px 10px 10px 10px'}, config={'displayModeBar': False}
                ),
                
            ], style={'border':'solid 1.5px', 'border-radius':'10px', 'margin-bottom':'1rem'}),
            html.Div([
                dcc.Graph(
                    id='genre_distribution_shows',
                    figure=px.pie(df.genre_counts_shows, values='count', names='listed_in', 
                                title='Распределение шоу по категориям'), style={'padding':'10px 10px 10px 10px'}, config={'displayModeBar': False}
                )
            ], style={'border':'solid 1.5px', 'border-radius':'10px'})
        ], style = {'margin-left':'2rem'}),
    return layout

layout = dbc.Container([
    html.Div(id='page2')
])

@callback(
    Output('page2', 'children'),
    Input('page2', 'id')
)
def update_genres(id):
    return page_layout()