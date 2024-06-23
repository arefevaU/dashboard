import dash_bootstrap_components as dbc

from dash import Dash, Input, Output, dcc, html
from pages import page1, country, genres, actors, age, info

external_stylesheets = [dbc.themes.LUX]  # Вместо FLATLY выберите свою тему из https://bootswatch.com/
app = Dash(__name__, external_stylesheets=external_stylesheets,  use_pages=True)
app.config.suppress_callback_exceptions = True

# Задаем аргументы стиля для боковой панели. Мы используем position:fixed и фиксированную ширину
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "19rem",
    "padding": "2rem 1rem",
    "background-color": "#FFB266", # Цвет фона боковой панели меняем на тот, который больше всего подходит
}

# Справа от боковой панели размешается основной дашборд. Добавим отступы
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Netflix Dashboard", className="display-6"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Общая статистика", href="/", active="exact"),
                dbc.NavLink("Жанры и категории", href="/page-1", active="exact"),
                dbc.NavLink("Страны производства", href="/page-2", active="exact"),
                dbc.NavLink("Актёры и режиссёры", href="/page-3", active="exact"),
                dbc.NavLink("Возрастные рейтинги", href="/page-4", active="exact"),
                dbc.NavLink("О проекте", href="/page-5", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return page1.layout
    elif pathname == "/page-1":
        return genres.layout
    elif pathname == "/page-2":
        return country.layout
    elif pathname == "/page-3":
        return actors.layout
    elif pathname == "/page-4":
        return age.layout
    elif pathname == "/page-5":
        return info.layout
    # Если пользователь попытается перейти на другую страницу, верните сообщение 404. Мы изменим её в следующей практической.
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == '__main__':
        app.run_server(debug=True)

