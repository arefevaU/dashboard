import pandas as pd

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

# Группировка по жанрам и подсчет уникальных шоу
genre_counts = df_exploded.groupby('listed_in')['show_id'].nunique().reset_index(name='count')