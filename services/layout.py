import dash_bootstrap_components as dbc
from dash import html

def create_services_student_layout():
    services = [
        {"title": "Оплата общежития", "url": "https://pay.uni-dubna.ru/hostel", "icon": "fas fa-bed", "color": "primary"},
        {"title": "Оплата обучения", "url": "https://pay.uni-dubna.ru/edu", "icon": "fas fa-graduation-cap", "color": "success"},
        {"title": "Другие услуги", "url": "https://pay.uni-dubna.ru/other", "icon": "fas fa-receipt", "color": "info"},
        {"title": "Система LMS", "url": "https://lms.uni-dubna.ru/", "icon": "fas fa-book-reader", "color": "warning"},
    ]
    
    cards = []
    for s in services:
        card = dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Div(html.I(className=f"{s['icon']} fa-3x mb-3 text-{s['color']}"), className="text-center"),
                    html.H5(s['title'], className="card-title text-center"),
                    dbc.Button("Перейти", href=s['url'], target="_blank", color=s['color'], className="w-100 mt-3")
                ])
            ], className="shadow h-100 hover-card"),
            width=12, md=6, lg=3, className="mb-4"
        )
        cards.append(card)

    return html.Div([
        html.H1("🔧 Сервисы для студентов", className="mb-4"),
        dbc.Row(cards)
    ])

def create_services_staff_layout():
    services = [
        {"title": "Система LMS", "url": "http://lms.uni-dubna.ru", "icon": "fas fa-chalkboard-teacher", "color": "warning"},
        {"title": "Тех. поддержка", "url": "https://hd.uni-dubna.ru", "icon": "fas fa-headset", "color": "danger"},
        {"title": "Расписание каб.", "url": "https://goo.gl/kfk6Ss", "icon": "fas fa-desktop", "color": "info"},
        {"title": "Облако (Drive)", "url": "https://drive.uni-dubna.ru", "icon": "fas fa-cloud", "color": "primary"},
    ]
    
    cards = []
    for s in services:
        card = dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Div(html.I(className=f"{s['icon']} fa-3x mb-3 text-{s['color']}"), className="text-center"),
                    html.H5(s['title'], className="card-title text-center"),
                    dbc.Button("Открыть", href=s['url'], target="_blank", color=s['color'], className="w-100 mt-3")
                ])
            ], className="shadow h-100"),
            width=12, md=6, lg=3, className="mb-4"
        )
        cards.append(card)

    return html.Div([
        html.H1("💼 Кабинет сотрудника", className="mb-4"),
        dbc.Row(cards)
    ])