import dash
import dash_bootstrap_components as dbc
import dash.html as html
import dash.dcc as dcc
from dash.dependencies import Input, Output

from components.navbar import create_navbar
from components.sidebar import create_sidebar

from schedule.layout import create_schedule_layout
from schedule.callbacks import register_schedule_callbacks
from news.layout import create_news_layout
from news.callbacks import register_news_callbacks

from events.layout import create_events_layout
from events.callbacks import register_events_callbacks

from pages.login import create_login_layout, register_login_callbacks
from pages.register import create_register_layout, register_reg_callbacks

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

app.layout = html.Div([
    dcc.Store(id='session-store', storage_type='session'),
    dcc.Location(id="url", refresh=True),
    html.Div(id="page-container")
])

register_schedule_callbacks(app)
register_news_callbacks(app)
register_events_callbacks(app) 
register_login_callbacks(app) 
register_reg_callbacks(app)

def create_test_dashboard():
    return dbc.Container([
        html.H1("Главная (Тестовый режим)", className="mb-4"),
        dbc.Row([
            dbc.Col(md=6, children=[
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Расписание на сегодня", className="card-title"),
                        dbc.ListGroup([
                            dbc.ListGroupItem("09:00 - 10:30 | Математика (Лекция)"),
                            dbc.ListGroupItem("10:40 - 12:10 | Физика (Практика)"),
                        ], flush=True)
                    ])
                )
            ]),
            dbc.Col(md=6, children=[
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Последние новости", className="card-title"),
                        dbc.ListGroup([
                            dbc.ListGroupItem("Изменение в расписании занятий"),
                            dbc.ListGroupItem("Набор на хакатон по программированию"),
                        ], flush=True)
                    ])
                )
            ]),
        ])
    ])

@app.callback(
    Output("page-container", "children"),
    Input("url", "pathname"),
    Input("session-store", "data")
)
def display_page(pathname, session_data):
    
    if pathname == "/logout":
        session_data = None
        return create_login_layout()

    login_pages = ['/login', '/register']
    
    if not session_data:
        if pathname in login_pages:
            if pathname == '/login':
                return create_login_layout()
            else:
                return create_register_layout()
        else:
            return create_login_layout()
            
    if pathname in login_pages:
        return dcc.Location(pathname="/", id="redirect-to-home")

    page_content = None
    
    if pathname == "/":
        page_content = create_test_dashboard()
    elif pathname == "/schedule":
        page_content = create_schedule_layout(session_data)
    elif pathname == "/news":
        page_content = create_news_layout(session_data)
    elif pathname == "/events":
        page_content = create_events_layout(session_data)
    elif pathname == "/services":
        page_content = html.H1("Сервисы")
    else:
        page_content = html.Div(
            [
                html.H1("404: Страница не найдена", className="text-danger"),
                html.Hr(),
                html.P(f"Путь {pathname} не был распознан..."),
            ],
            className="text-center",
        )

    return html.Div([
        create_navbar(),
        create_sidebar(session_data),
        html.Div(id="page-content", style=CONTENT_STYLE, children=page_content)
    ])

if __name__ == '__main__':
    app.run(debug=True, port=8050)