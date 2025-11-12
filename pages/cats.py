import dash
import dash_bootstrap_components as dbc
import dash.html as html
import dash.dcc as dcc
import random
import os
from datetime import datetime

# Список поддерживающих фраз
MOTIVATIONAL_PHRASES = [
    "Ты справишься! 💪",
    "Отличная работа! 🌟",
    "Продолжай в том же духе! 🚀",
    "Каждый день - это новый шанс! ✨",
    "Ты делаешь это великолепно! 👍",
    "Не сдавайся! У тебя все получится! 💫",
    "Маленькие шаги ведут к большим целям! 🐾",
    "Ты заслуживаешь перерыва! 😸",
    "Учеба - это путь, а не цель! 📚",
    "Гордись своими достижениями! 🏆"
]

def get_daily_cat_index():
    """Генерирует индекс котика на основе текущей даты"""
    today = datetime.now()
    return hash(today.date()) % 10 + 1  # 10 разных котиков

def create_cats_layout():
    # Получаем индекс котика на сегодня
    cat_index = get_daily_cat_index()
    
    # Выбираем случайную фразу
    motivational_phrase = random.choice(MOTIVATIONAL_PHRASES)
    
    layout = html.Div([
        html.Div([
            html.H1("Котики для настроения 🐱", 
                   className="mb-4 text-center",
                   style={'color': '#ffffff', 'textShadow': '2px 2px 4px rgba(0,0,0,0.5)'}),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2("Ваш ежедневный котик", 
                           className="card-title text-center mb-4",
                           style={'color': '#2c3e50'}),
                    
                    html.Hr(style={'borderColor': '#34495e'}),
                    
                    # Контейнер для котика
                    html.Div([
                        html.Img(
                            src=f"/assets/cats/cat_{cat_index}.jpg",
                            style={
                                'width': '100%',
                                'max-width': '500px',
                                'height': 'auto',
                                'border-radius': '15px',
                                'box-shadow': '0 4px 8px rgba(0,0,0,0.3)',
                                'border': '3px solid #34495e'
                            },
                            className="mb-4"
                        ),
                    ], className="text-center"),
                    
                    # Поддерживающее сообщение
                    dbc.Alert(
                        motivational_phrase,
                        color="warning",
                        className="text-center h4",
                        style={
                            'border': 'none', 
                            'background': 'linear-gradient(135deg, #f39c12, #e74c3c)',
                            'color': '#ffffff',
                            'fontWeight': 'bold',
                            'borderRadius': '25px',
                            'padding': '15px',
                            'margin': '20px 0'
                        }
                    ),
                    
                    # Информация о функциональности
                    html.P(
                        "🐾 Котик меняется каждый день! Заходите завтра за новым котиком! 🐾",
                        className="text-center mt-3",
                        style={'color': '#bdc3c7', 'fontStyle': 'italic'}
                    ),
                    
                    # Дополнительные котики
                    html.Hr(style={'borderColor': '#34495e', 'margin': '30px 0'}),
                    html.H4("Еще немного котиков для хорошего настроения:", 
                           className="mt-4 text-center",
                           style={'color': '#ecf0f1'}),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Img(
                                    src=f"/assets/cats/cat_{(cat_index + i) % 10 + 1}.jpg",
                                    style={
                                        'width': '100%',
                                        'max-width': '200px',
                                        'height': 'auto',
                                        'border-radius': '10px',
                                        'border': '2px solid #34495e',
                                        'box-shadow': '0 2px 4px rgba(0,0,0,0.2)',
                                        'transition': 'transform 0.3s ease'
                                    },
                                    className="cat-image"
                                )
                            ], className="text-center p-2")
                        ], width=4, className="mb-3") for i in range(1, 4)
                    ], className="justify-content-center mt-3"),
                    
                ], style={'backgroundColor': '#ecf0f1', 'borderRadius': '15px'})
            ], className="shadow-lg", style={'border': 'none', 'borderRadius': '15px'}),
            
            # CSS для анимации при наведении
            html.Style('''
                .cat-image:hover {
                    transform: scale(1.05);
                }
                .card {
                    background: linear-gradient(135deg, #34495e, #2c3e50);
                }
            ''')
            
        ], style={
            'background': 'linear-gradient(135deg, #2c3e50 0%, #3498db 100%)',
            'minHeight': '100vh',
            'padding': '20px'
        })
    ])
    
    return layout