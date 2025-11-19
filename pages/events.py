import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import json
from datetime import datetime, date
import dash_bootstrap_components as dbc

# Загрузка данных
def load_events_data():
    try:
        with open('data/events.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('events', [])
    except FileNotFoundError:
        return []

# Преобразование данных в DataFrame
def get_events_df():
    events = load_events_data()
    if not events:
        return pd.DataFrame()
    
    df = pd.DataFrame(events)
    if not df.empty and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
    return df

# Получение уникальных типов мероприятий
def get_event_types():
    df = get_events_df()
    if not df.empty and 'type' in df.columns:
        return sorted(df['type'].unique().tolist())
    return []

# Функция для определения цвета по типу мероприятия
def get_event_color(event_type):
    color_map = {
        'хакатон': 'success',        # Зеленый
        'лекция': 'info',            # Голубой
        'конференция': 'primary',    # Синий
        'мастер-класс': 'warning',   # Оранжевый
        'спортивное соревнование': 'danger',  # Красный
        'день открытых дверей': 'secondary'   # Серый
    }
    
    # Приводим к нижнему регистру для сравнения
    event_type_lower = event_type.lower()
    
    # Ищем подходящий цвет
    for key, color in color_map.items():
        if key in event_type_lower:
            return color
    
    # Если тип не найден, используем цвет по умолчанию
    return 'primary'

def create_events_layout():
    event_types = get_event_types()
    
    return html.Div([
        html.H1("📅 Мероприятия", className="mb-4"),
        html.P("Календарь событий и мероприятий университета", 
               className="text-muted mb-4"),
        
        # Фильтры
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Диапазон дат:", className="fw-bold mb-2"),
                        dcc.DatePickerRange(
                            id='date-range-picker',
                            start_date=date(2025, 1, 1),
                            end_date=date(2025, 12, 31),
                            display_format='YYYY-MM-DD',
                            className="w-100"
                        )
                    ], md=6, className="mb-3"),
                    dbc.Col([
                        html.Label("Тип мероприятия:", className="fw-bold mb-2"),
                        dcc.Dropdown(
                            id='event-type-filter',
                            options=[{'label': 'Все типы', 'value': 'all'}] + 
                                    [{'label': event_type, 'value': event_type} for event_type in event_types],
                            value='all',
                            clearable=False,
                            className="events-dropdown"
                        )
                    ], md=6, className="mb-3")
                ])
            ])
        ], className="mb-4 bg-secondary"),
        
        # Карточки мероприятий
        html.Div(id='events-cards-container')
    ])

# Callback для фильтрации мероприятий
@callback(
    Output('events-cards-container', 'children'),
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date'),
     Input('event-type-filter', 'value')]
)
def update_events_cards(start_date, end_date, event_type):
    df = get_events_df()
    
    if df.empty:
        return dbc.Alert("Нет данных о мероприятиях", color="warning")
    
    # Фильтрация по дате
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Фильтрация по типу
    if event_type != 'all':
        df = df[df['type'] == event_type]
    
    if df.empty:
        return dbc.Alert("Мероприятия не найдены по выбранным фильтрам", color="info")
    
    # Сортируем по дате (от ближайших к дальним)
    df = df.sort_values('date')
    
    # Создание карточек мероприятий
    cards = []
    for _, event in df.iterrows():
        # Определяем цвет карточки
        card_color = get_event_color(event['type'])
        
        # Определяем иконку в зависимости от типа мероприятия
        icon_map = {
            'хакатон': '💻',
            'лекция': '🎓',
            'конференция': '📊',
            'мастер-класс': '🎤',
            'спортивное соревнование': '⚽',
            'день открытых дверей': '🏛️'
        }
        
        event_icon = '📅'  # Иконка по умолчанию
        for key, icon in icon_map.items():
            if key in event['type'].lower():
                event_icon = icon
                break
        
        card = dbc.Card([
            dbc.CardHeader([
                html.Div([
                    html.Div([
                        html.Span(event_icon, className="me-2"),
                        html.H5(event['title'], className="mb-0 d-inline")
                    ]),
                    dbc.Badge(event['type'], color=card_color, className="ms-2")
                ], className="d-flex justify-content-between align-items-center")
            ], className=f"bg-{card_color}"),
            dbc.CardBody([
                html.P(event['description'], className="card-text"),
                html.Div([
                    html.Div([
                        html.I(className="fas fa-calendar me-2"),
                        html.Span(f"{event['date'].strftime('%d.%m.%Y')} в {event.get('time', '')}")
                    ], className="mb-2"),
                    html.Div([
                        html.I(className="fas fa-map-marker-alt me-2"),
                        html.Span(event['location'])
                    ], className="mb-2")
                ])
            ]),
            dbc.CardFooter(
                dbc.Button(
                    "Зарегистрироваться" if event.get('is_registration_required', False) else "Подробнее",
                    href=event.get('registration_link', '#') if event.get('registration_link') else '#',
                    target="_blank" if event.get('registration_link') else "_self",
                    color=card_color,
                    size="sm"
                ) if event.get('is_registration_required', False) or event.get('registration_link') else 
                html.Small("Регистрация не требуется", className="text-muted")
            )
        ], className="mb-3")
        cards.append(card)
    
    return cards