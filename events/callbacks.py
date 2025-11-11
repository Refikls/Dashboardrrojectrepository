import dash
from dash import html, dcc, Input, Output, callback
import pandas as pd
import json
from datetime import datetime, date
import dash_bootstrap_components as dbc

def load_events_data():
    try:
        with open('data/events.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('events', [])
    except FileNotFoundError:
        return []

def get_events_df():
    events = load_events_data()
    if not events:
        return pd.DataFrame()
    
    df = pd.DataFrame(events)
    if not df.empty and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
    return df

def get_event_types():
    df = get_events_df()
    if not df.empty and 'type' in df.columns:
        return sorted(df['type'].unique().tolist())
    return []

def get_event_color(event_type):
    color_map = {
        'хакатон': 'success',
        'лекция': 'info',
        'конференция': 'primary',
        'мастер-класс': 'warning',
        'спортивное соревнование': 'danger',
        'день открытых дверей': 'secondary'
    }
    event_type_lower = event_type.lower()
    for key, color in color_map.items():
        if key in event_type_lower:
            return color
    return 'primary'

def register_events_callbacks(app):
    
    @app.callback(
        Output('event-type-filter', 'options'),
        Input('url', 'pathname')
    )
    def update_event_type_options(pathname):
        if pathname == '/events':
            event_types = get_event_types()
            options = [{'label': 'Все типы', 'value': 'all'}] + \
                      [{'label': event_type, 'value': event_type} for event_type in event_types]
            return options
        return []

    @app.callback(
        Output('events-cards-container', 'children'),
        [Input('date-range-picker', 'start_date'),
         Input('date-range-picker', 'end_date'),
         Input('event-type-filter', 'value')]
    )
    def update_events_cards(start_date, end_date, event_type):
        df = get_events_df()
        
        if df.empty:
            return dbc.Alert("Нет данных о мероприятиях", color="warning")
        
        if start_date and end_date:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        if event_type and event_type != 'all':
            df = df[df['type'] == event_type]
        
        if df.empty:
            return dbc.Alert("Мероприятия не найдены по выбранным фильтрам", color="info")
        
        df = df.sort_values('date')
        
        cards = []
        for _, event in df.iterrows():
            card_color = get_event_color(event['type'])
            
            icon_map = {
                'хакатон': '💻',
                'лекция': '🎓',
                'конференция': '📊',
                'мастер-класс': '🎤',
                'спортивное соревнование': '⚽',
                'день открытых дверей': '🏛️'
            }
            
            event_icon = '📅'
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