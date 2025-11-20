import dash
import dash_bootstrap_components as dbc
import dash.html as html
import dash.dcc as dcc
from dash.dependencies import Input, Output
import random
from datetime import datetime

from components.navbar import create_navbar
from components.sidebar import create_sidebar

from services.layout import create_services_student_layout, create_services_staff_layout

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

def get_daily_cat_index():
    return hash(str(datetime.now().date())) % 5 + 1

def calculate_semester_progress():
    now = datetime.now()
    current_year = now.year
    start_date = datetime(current_year, 9, 1)
    end_date = datetime(current_year, 12, 30)
    
    if now.month < 9:
        start_date = datetime(current_year, 2, 7)
        end_date = datetime(current_year, 6, 30)

    total_days = (end_date - start_date).days
    days_passed = (now - start_date).days
    
    if days_passed < 0: return 0
    if days_passed > total_days: return 100
    
    return int((days_passed / total_days) * 100)

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
    cat_index = get_daily_cat_index()
    motivational_phrase = random.choice(MOTIVATIONAL_PHRASES)
    semester_percent = calculate_semester_progress()
    
    base_role = session_data.get('base_role', 'student')
    username = "Студент" if base_role == 'student' else "Сотрудник"
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H1(f"Добро пожаловать, {username}! 👋", className="mb-3"),
                html.P("Хорошего продуктивного дня!", className="lead mb-4"),
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📝 Личные заметки", className="card-title mb-3"),
                        dcc.Textarea(
                            id='dashboard-quick-notes',
                            placeholder="Запиши сюда что-нибудь...\n(Сохраняется в браузере)",
                            style={
                                'width': '100%', 'height': '150px', 'resize': 'none',
                                'borderRadius': '5px', 'padding': '10px',
                                'backgroundColor': '#2b3e50', 'color': 'white', 'border': '1px solid #4e5d6c'
                            },
                            persistence=True, persistence_type='local',
                        ),
                    ])
                ], className="shadow mb-4"),
                
                dbc.Card([
                    dbc.CardBody([
                        html.H4("⏳ Прогресс семестра", className="card-title mb-3"),
                        dbc.Progress(label=f"{semester_percent}%", value=semester_percent, color="info", striped=True, animated=True, className="mb-3"),
                    ])
                ], className="shadow"),
            ], width=12, md=8),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Котик дня 🐱", className="card-title text-center mb-3"),
                        html.Div([
                            html.Img(
                                src=f"/assets/cats/cat_{cat_index}.jpg",
                                style={'width': '100%', 'max-width': '250px', 'border-radius': '10px', 'height': 'auto'},
                                className="mb-3"
                            ),
                        ], className="text-center"),
                        dbc.Alert(motivational_phrase, color="warning", className="text-center h5 mb-0"),
                        html.P("Обновляется каждый день!", className="text-muted text-center small mt-2"),
                    ])
                ], className="shadow h-100"),
            ], width=12, md=4),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("О дашборде", className="card-title"),
                        html.P([
                            "Здесь вы можете отслеживать расписание, новости и мероприятия."
                        ]),
                        html.P("Котик дня - для хорошего настроения! 🐾", className="text-warning font-italic mb-0")
                    ])
                ], className="shadow mt-4"),
            ], width=12)
        ])
    ])

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
        page_content = create_main_layout(session_data)
    elif pathname == "/schedule":
        page_content = create_schedule_layout(session_data)
    elif pathname == "/news":
        page_content = create_news_layout(session_data)
    elif pathname == "/events":
        page_content = create_events_layout(session_data)
    elif pathname == "/services":
        page_content = create_services_student_layout()

    elif pathname == "/services-staff":
        page_content = create_services_staff_layout()
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