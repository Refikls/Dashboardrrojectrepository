import dash.html as html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "3.5rem",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

def create_sidebar():
    sidebar = html.Div(
        [
            html.H4("Навигация", style={"textAlign": "center"}),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Главная", href="/", active="exact"),
                    dbc.NavLink("Расписание", href="/schedule", active="exact"),
                    dbc.NavLink("Новости", href="/news", active="exact"),
                    dbc.NavLink("Мероприятия", href="/events", active="exact"),
                    dbc.NavLink("Сервисы", href="/services", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )
    return sidebar