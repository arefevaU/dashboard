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
        html.H2('Возрастные рейтинги и продолжительность'),
        html.Div([
            dcc.Graph(
                id='rating_distribution',
                figure=px.histogram(df.df, x='rating', title='Распределение контента по возрастным рейтингам')
            ),
            dcc.Graph(
                id='movies_duration',
                figure=px.box(df.df[df.df['type'] == 'Movie'], y='duration_int', 
                              title='Средняя продолжительность фильмов')
            ),
            dcc.Graph(
                id='shows_seasons',
                figure=px.box(df.df[df.df['type'] == 'TV Show'], y='duration_int', 
                              title='Среднее количество сезонов сериалов')
            )
        ])
    ]),
    return layout

layout = dbc.Container([
    html.Div(id='page5')
])

@callback(
    Output('page5', 'children'),
    Input('page5', 'id')
)
def update_actors(id):
    return page_layout()