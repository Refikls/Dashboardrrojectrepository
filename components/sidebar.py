import dash.html as html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "3.5rem",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
}

def create_sidebar(session_data):
    
    base_role = session_data.get('base_role', 'student')

    common_links = [
        dbc.NavLink("Главная", href="/", active="exact"),
        dbc.NavLink("Расписание", href="/schedule", active="exact"),
        dbc.NavLink("Новости", href="/news", active="exact"),
        dbc.NavLink("Мероприятия", href="/events", active="exact"),
    ]
    
    role_specific_links = []

    if base_role == 'student':
        role_specific_links = [
            dbc.NavLink("Студ. Сервисы", href="/services", active="exact"),
        ]
    elif base_role == 'staff':
        role_specific_links = [
            dbc.NavLink("Сервисы Сотрудника", href="/services-staff", active="exact"),
        ]

    common_links.extend(role_specific_links)
    
    sidebar = html.Div(
        dbc.Nav(common_links, vertical=True, pills=True),
        style=SIDEBAR_STYLE,
    )
    return sidebar