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
        html.H2('Страны производства'),
        html.Div([
            dcc.Graph(
                id='country_distribution',
                figure=px.choropleth(df.df_exploded.groupby('country')['show_id'].nunique().reset_index(name='count'), 
                                    locations='country', locationmode='country names', color='count', 
                                    title='Тепловая карта стран по количеству контента', 
                                    color_continuous_scale='viridis', range_color=[0, df.df_exploded['show_id'].nunique()])
            )
        ])
    ]),
    return layout

layout = dbc.Container([
    html.Div(id='page3')
])

@callback(
    Output('page3', 'children'),
    Input('page3', 'id')
)
def update_country(id):
    return page_layout()