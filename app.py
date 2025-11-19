import dash
import dash_bootstrap_components as dbc
import dash.html as html
import dash.dcc as dcc
import random
from datetime import datetime
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

# Функция для получения ежедневного котика
def get_daily_cat_index():
    """Генерирует индекс котика на основе текущей даты"""
    today = datetime.now()
    return hash(str(today.date())) % 5 + 1  # 5 разных котиков

# Список мотивационных фраз
MOTIVATIONAL_PHRASES = [
    "Ты справишься! 💪",
    "Отличная работа! 🌟", 
    "Продолжай в том же духе! 🚀",
    "Каждый день - это новый шанс! ✨",
    "Ты делаешь это великолепно! 👍",
    "Не сдавайся! У тебя все получится! 💫",
    "Маленькие шаги ведут к большим целям! 🐾",
    "Ты заслуживаешь перерыва! 😸"
]

def create_main_layout(session_data):
    """Создает layout главной страницы с котиками"""
    cat_index = get_daily_cat_index()
    motivational_phrase = random.choice(MOTIVATIONAL_PHRASES)
    
    # Получаем имя пользователя из session_data если есть
    username = session_data.get('username', 'Студент') if session_data else 'Студент'
    
    return html.Div([
        # Заголовок и приветствие
        dbc.Row([
            dbc.Col([
                html.H1(f"Добро пожаловать, {username}! 👋", className="mb-3"),
                html.P("Ваш персональный дашборд для эффективной учебы", 
                      className="lead mb-4"),
            ], width=12)
        ]),
        
        # Основной контент в две колонки
        dbc.Row([
            # Левая колонка - меню быстрого доступа
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Быстрый доступ", className="card-title mb-3"),
                        dbc.ListGroup([
                            dbc.ListGroupItem(
                                dbc.Button("📅 Расписание", 
                                         color="primary", 
                                         className="w-100 text-start",
                                         href="/schedule"),
                                className="border-0 p-1"
                            ),
                            dbc.ListGroupItem(
                                dbc.Button("📰 Новости", 
                                         color="primary", 
                                         className="w-100 text-start",
                                         href="/news"),
                                className="border-0 p-1"
                            ),
                            dbc.ListGroupItem(
                                dbc.Button("🎭 Мероприятия", 
                                         color="primary", 
                                         className="w-100 text-start", 
                                         href="/events"),
                                className="border-0 p-1"
                            ),
                            dbc.ListGroupItem(
                                dbc.Button("🔧 Сервисы", 
                                         color="primary", 
                                         className="w-100 text-start",
                                         href="/services"),
                                className="border-0 p-1"
                            ),
                        ], flush=True)
                    ])
                ], className="shadow mb-4"),
                
                # Статистика или уведомления
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Сегодня", className="card-title"),
                        dbc.ListGroup([
                            dbc.ListGroupItem("✅ Занятия по расписанию"),
                            dbc.ListGroupItem("📝 2 новых уведомления"),
                            dbc.ListGroupItem("🎯 Цели на день"),
                        ], flush=True),
                    ])
                ], className="shadow"),
            ], width=8),
            
            # Правая колонка - котик для настроения
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Котик дня 🐱", className="card-title text-center mb-3"),
                        
                        # Изображение котика
                        html.Div([
                            html.Img(
                                src=f"/assets/cats/cat_{cat_index}.jpg",
                                style={
                                    'width': '100%',
                                    'max-width': '250px',
                                    'height': 'auto',
                                    'border-radius': '10px',
                                },
                                className="mb-3"
                            ),
                        ], className="text-center"),
                        
                        # Мотивационная фраза
                        dbc.Alert(
                            motivational_phrase,
                            color="warning",
                            className="text-center h5 mb-0"
                        ),
                        
                        html.P(
                            "Обновляется каждый день!",
                            className="text-muted text-center small mt-2"
                        ),
                    ])
                ], className="shadow h-100"),
            ], width=4),
        ]),
        
        # Дополнительная информация
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("О дашборде", className="card-title"),
                        html.P([
                            "Этот дашборд поможет вам в учебном процессе. ",
                            html.Br(),
                            "Здесь вы можете отслеживать расписание, новости и мероприятия."
                        ]),
                        html.P("Котик дня - для хорошего настроения! 🐾", 
                              className="text-warning font-italic mb-0")
                    ])
                ], className="shadow mt-4"),
            ], width=12)
        ])
    ])

@app.callback(
    Output("page-container", "children"),
    Input("url", "pathname"),
    Input("session-store", "data")
)
def display_page(pathname, session_data):
    
    if pathname == "/logout":
        return dcc.Location(pathname="/login", id="redirect-to-login")

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
        # Новая главная страница с котиками
        page_content = create_main_layout(session_data)
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