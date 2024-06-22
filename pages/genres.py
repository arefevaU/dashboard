import pandas as pd
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO
import dash_bootstrap_components as dbc
import data as df

def page_layout():
    layout = html.Div([
            html.H2('Жанры и категории'),
            html.Div([
                dcc.Graph(
                    id='genre_distribution_movies',
                    figure=px.pie(df.genre_counts_movies, values='count', names='listed_in', 
                                title='Распределение фильмов по жанрам')
                ),
                dcc.Graph(
                    id='genre_distribution_shows',
                    figure=px.pie(df.genre_counts_shows, values='count', names='listed_in', 
                                title='Распределение шоу по категориям')
                )
            ])
        ]),
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