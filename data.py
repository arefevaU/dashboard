import pandas as pd

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