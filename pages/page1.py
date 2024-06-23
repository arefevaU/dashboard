from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import data as df

def page_layout():
    layout = html.Div([
    html.H3('Общая статистика', style = {'margin-bottom':'2rem', 'text-align':'center'}),
    
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H3('Фильмы', style = {'padding': '5px 5px 5px 5px'}),
                html.P(df.movies_count, style = {'padding': '5px 5px 5px 5px', 'font-size':'28px', 'color':'black', 'font-weight':'bold', 'text-align':'right'})
            ],width=3, style={'border':'solid 1.5px', 'border-radius':'10px', 'margin-right':'1rem'}),
            dbc.Col([
                html.H3('ТВ-шоу', style = {'padding': '5px 5px 5px 5px'}),
                html.P(df.shows_count, style = {'padding': '5px 5px 5px 5px', 'font-size':'28px', 'color':'black', 'font-weight':'bold', 'text-align':'right'})
            ],width=3, style={'border':'solid 1.5px', 'border-radius':'10px'}),
        ], className='card-container')
    ], style={'margin':'0rem 0rem 1rem 1rem'}),
    
    html.Div([
        html.H3('Добавление контента по месяцам и годам', style = {'margin-bottom':'2rem', 'text-align':'center', 'padding-top':'20px'}),
        dcc.Graph(
            figure=px.bar(df.df.groupby(['year_added', 'month_added']).size().reset_index(name='count'), 
                          x='year_added', y='count', color='month_added', labels={'year_added': '', 'count': '', 'month_added': ''}), 
                          config={'displayModeBar': False},
                          style={'padding':'0px 0px 10px 0px'}
        )
    ], style={'border':'solid 1.5px', 'border-radius':'10px'}), 
    ], style={'margin-left':'2rem'})
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
