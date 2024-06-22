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
    html.H3('Общая статистика', style = {'margin-bottom':'2rem', 'text-align':'center'}),
    
    dbc.Row([
        html.Div([
            html.Div([
                html.H3('Количество фильмов', style = {'padding': '5px 5px 5px 5px', 'background-color':'grey'}),
                html.P(df.movies_count, style = {'padding': '5px 5px 5px 5px'})
            ], style = {'margin-right': '50%', 'border':'solid 2px', 'border-radius': '10px'}),
            html.Div([
                html.H3('Количество сериалов', style = {'padding': '5px 5px 5px 5px', 'background-color':'grey'}),
                html.P(df.shows_count, style = {'padding': '5px 5px 5px 5px'})
            ], style = {'margin-right': '50%', 'border':'solid 2px', 'border-radius': '10px'}),
        ], className='card-container')
    ]),
    
    
    html.Div([
        html.H2('График добавлений контента по месяцам/годам'),
        dcc.Graph(
            figure=px.bar(df.df.groupby(['year_added', 'month_added']).size().reset_index(name='count'), 
                          x='year_added', y='count', color='month_added', 
                          title='Добавления контента по месяцам/годам')
        )
    ]),
    ])
    return layout

layout= dbc.Container([
    dbc.Row([
        html.Div(id = 'page1')
    ])
])

@callback(
    Output('page1', 'children'),
    Input('page1', 'id')
)
def update_page1(id):
    return page_layout()
