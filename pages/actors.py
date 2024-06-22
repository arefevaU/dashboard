from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import data as df

def page_layout():
    layout = html.Div([
        html.H2('Режиссеры и актеры', style = {'margin-bottom':'2rem', 'text-align':'center'}),
        html.Div([
            dcc.Graph(
                id='top_directors',
                figure=px.bar(df.df_exploded['director'].value_counts().head(10), 
                              x=df.df_exploded['director'].value_counts().head(10).values, 
                              y=df.df_exploded['director'].value_counts().head(10).index, orientation='h',
                              title='Топ режиссеров по количеству контента'),
                              style={'border':'solid 1.5px', 'border-radius':'10px', 'margin-bottom':'1rem', 'padding':'10px 10px 10px 10px'}, config={'displayModeBar': False}
            ),
            dcc.Graph(
                id='top_cast',
                figure=px.bar(df.df_exploded['cast'].value_counts().head(10), 
                              x=df.df_exploded['cast'].value_counts().head(10).values, 
                              y=df.df_exploded['cast'].value_counts().head(10).index, orientation='h',
                              title='Топ актеров по количеству контента'),
                              style={'border':'solid 1.5px', 'border-radius':'10px', 'margin-bottom':'1rem', 'padding':'10px 10px 10px 10px'}, config={'displayModeBar': False}
            )
        ])
    ], style = {'margin-left':'2rem'}),
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