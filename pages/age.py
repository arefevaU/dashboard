from dash import dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import data as df

def page_layout():
    layout = html.Div([
        html.H3('Возрастные рейтинги', style = {'margin-bottom':'2rem', 'text-align':'center'}),
        html.Div([
            dcc.Graph(
                id='rating_distribution',
                figure=px.histogram(df.df, x='rating', title='Распределение контента по возрастным рейтингам', labels={'rating':''}),
                style={'border':'solid 1.5px', 'border-radius':'10px', 'margin-bottom':'1rem', 'padding':'10px 10px 10px 10px'}, config={'displayModeBar': False}
            ),
        ])
    ], style = {'margin-left':'2rem'}),
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