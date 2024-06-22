import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from wordcloud import WordCloud
import base64
from io import BytesIO
import data as df

# Загрузка данных
df = pd.read_csv('Netflix.csv', sep=',')

# Преобразование date_added в datetime формат
df['date_added'] = pd.to_datetime(df['date_added'])

# Выделение года и месяца из date_added
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month_name()

# Преобразование duration в числовой формат
df['duration_int'] = df['duration'].apply(lambda x: int(x.split(' ')[0]) if isinstance(x, str) else 0)
df.loc[df['type'] == 'Movie', 'duration_type'] = 'min'
df.loc[df['type'] == 'TV Show', 'duration_type'] = 'seasons'

# Подсчет уникальных фильмов и сериалов
movies_count = df[df['type'] == 'Movie']['show_id'].nunique()
shows_count = df[df['type'] == 'TV Show']['show_id'].nunique()

# Функция для разделения и преобразования столбцов
def split_and_explode(df, column):
    df[column] = df[column].str.split(', ')
    df = df.explode(column)
    return df

df_exploded = df.copy()
df_exploded = split_and_explode(df_exploded, 'country')
df_exploded = split_and_explode(df_exploded, 'cast')
df_exploded = split_and_explode(df_exploded, 'director')
df_exploded = split_and_explode(df_exploded, 'listed_in')

# Разделение данных по типам
df_movies = df_exploded[df_exploded['type'] == 'Movie']
df_shows = df_exploded[df_exploded['type'] == 'TV Show']

# Группировка по жанрам и подсчет уникальных шоу
genre_counts_movies = df_movies.groupby('listed_in')['show_id'].nunique().reset_index(name='count')
genre_counts_shows = df_shows.groupby('listed_in')['show_id'].nunique().reset_index(name='count')

# Создание дашборда Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Netflix Dashboard'),
    
    html.Div([
        html.H2('Общая статистика'),
        html.Div([
            html.Div([
                html.H3('Количество фильмов'),
                html.P(movies_count)
            ], className='card'),
            html.Div([
                html.H3('Количество сериалов'),
                html.P(shows_count)
            ], className='card'),
        ], className='card-container')
    ]),
    
    html.Div([
        html.H2('График добавлений контента по месяцам/годам'),
        dcc.Graph(
            id='content_by_date',
            figure=px.bar(df.groupby(['year_added', 'month_added']).size().reset_index(name='count'), 
                          x='year_added', y='count', color='month_added', 
                          title='Добавления контента по месяцам/годам')
        )
    ]),
    
    html.Div([
        html.H2('Жанры и категории'),
        html.Div([
            dcc.Graph(
                id='genre_distribution_movies',
                figure=px.pie(genre_counts_movies, values='count', names='listed_in', 
                              title='Распределение фильмов по жанрам')
            ),
            dcc.Graph(
                id='genre_distribution_shows',
                figure=px.pie(genre_counts_shows, values='count', names='listed_in', 
                              title='Распределение шоу по категориям')
            )
        ])
    ]),
    
    html.Div([
        html.H2('Страны производства'),
        html.Div([
            dcc.Graph(
                id='country_distribution',
                figure=px.choropleth(df_exploded.groupby('country')['show_id'].nunique().reset_index(name='count'), 
                                    locations='country', locationmode='country names', color='count', 
                                    title='Тепловая карта стран по количеству контента', 
                                    color_continuous_scale='viridis', range_color=[0, df_exploded['show_id'].nunique()])
            )
        ])
    ]),

    html.Div([
        html.H2('Режиссеры и актеры'),
        html.Div([
            dcc.Graph(
                id='top_directors',
                figure=px.bar(df_exploded['director'].value_counts().head(10), 
                              x=df_exploded['director'].value_counts().head(10).values, 
                              y=df_exploded['director'].value_counts().head(10).index, orientation='h', 
                              title='Топ режиссеров по количеству контента')
            ),
            dcc.Graph(
                id='top_cast',
                figure=px.bar(df_exploded['cast'].value_counts().head(10), 
                              x=df_exploded['cast'].value_counts().head(10).values, 
                              y=df_exploded['cast'].value_counts().head(10).index, orientation='h', 
                              title='Топ актеров по количеству контента')
            )
        ])
    ]),
    
    html.Div([
        html.H2('Возрастные рейтинги и продолжительность'),
        html.Div([
            dcc.Graph(
                id='rating_distribution',
                figure=px.histogram(df, x='rating', title='Распределение контента по возрастным рейтингам')
            ),
            dcc.Graph(
                id='movies_duration',
                figure=px.box(df[df['type'] == 'Movie'], y='duration_int', 
                              title='Средняя продолжительность фильмов')
            ),
            dcc.Graph(
                id='shows_seasons',
                figure=px.box(df[df['type'] == 'TV Show'], y='duration_int', 
                              title='Среднее количество сезонов сериалов')
            )
        ])
    ]),
    
    html.Div([
        html.H2('Текстовый анализ описаний'),
        html.Div([
            html.Img(id='wordcloud', src=''),
        ])
    ])
])

@app.callback(
    Output('wordcloud', 'src'),
    Input('wordcloud', 'id')
)
def update_wordcloud(src):
    text = " ".join(description for description in df['description'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    buf = BytesIO()
    wordcloud.to_image().save(buf, format="PNG")
    data = base64.b64encode(buf.getbuffer()).decode("utf8")
    return "data:image/png;base64,{}".format(data)
