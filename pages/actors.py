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
        html.H2('Режиссеры и актеры'),
        html.Div([
            dcc.Graph(
                id='top_directors',
                figure=px.bar(df.df_exploded['director'].value_counts().head(10), 
                              x=df.df_exploded['director'].value_counts().head(10).values, 
                              y=df.df_exploded['director'].value_counts().head(10).index, orientation='h', 
                              title='Топ режиссеров по количеству контента')
            ),
            dcc.Graph(
                id='top_cast',
                figure=px.bar(df.df_exploded['cast'].value_counts().head(10), 
                              x=df.df_exploded['cast'].value_counts().head(10).values, 
                              y=df.df_exploded['cast'].value_counts().head(10).index, orientation='h', 
                              title='Топ актеров по количеству контента')
            )
        ])
    ]),
    return layout

layout = dbc.Container([
    html.Div(id='page4')
])

@callback(
    Output('page4', 'children'),
    Input('page4', 'id')
)
def update_actors(id):
    return page_layout()