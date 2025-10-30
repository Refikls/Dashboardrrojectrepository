import dash
import dash_bootstrap_components as dbc
import dash.html as html
import dash.dcc as dcc
from dash.dependencies import Input, Output

from components.navbar import create_navbar
from components.sidebar import create_sidebar

### Интеграция schedule
from components.schedule.layout import create_schedule_layout
from components.schedule.callbacks import register_schedule_callbacks

app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.SUPERHERO],
    suppress_callback_exceptions=True
)
server = app.server

CONTENT_STYLE = {
    "margin-top": "3.5rem",
    "margin-left": "18rem",
    "padding": "2rem 1rem",
}

navbar = create_navbar()
sidebar = create_sidebar()

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    sidebar,
    html.Div(id="page-content", style=CONTENT_STYLE)
])

# Регистрируем callback'и
register_schedule_callbacks(app)

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/":
        return html.H1("Главная страница")
    elif pathname == "/schedule":
        return create_schedule_layout()  # Используем модуль расписания
    #html.H1("Расписание")
    elif pathname == "/news":
        return html.H1("Новости")
    elif pathname == "/events":
        return html.H1(" Мероприятия")
    elif pathname == "/services":
        return html.H1("Сервисы")
    
    return html.Div(
        [
            html.H1("404: Страница не найдена", className="text-danger"),
            html.Hr(),
            html.P(f"Путь {pathname} не был распознан..."),
        ],
        className="text-center",
    )

if __name__ == '__main__':
    app.run(debug=True, port=8050)