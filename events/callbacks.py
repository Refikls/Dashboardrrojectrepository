import dash
from dash import html, dcc, Input, Output, State, callback
import pandas as pd
import json
from datetime import datetime
import dash_bootstrap_components as dbc
import time

DATA_FILE = 'data/events.json'

def load_events_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('events', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_events_data(events_list):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({'events': events_list}, f, ensure_ascii=False, indent=4)
        return True
    except IOError:
        return False

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
         Input('event-type-filter', 'value'),
         Input('events-form-trigger', 'data')]
    )
    def update_events_cards(start_date, end_date, event_type, form_trigger):
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
                    dbc.Row([
                        dbc.Col(
                            dbc.Button(
                                "Зарегистрироваться" if event.get('is_registration_required', False) else "Подробнее",
                                href=event.get('registration_link', '#') if event.get('registration_link') else '#',
                                target="_blank" if event.get('registration_link') else "_self",
                                color=card_color,
                                size="sm"
                            ) if event.get('is_registration_required', False) or event.get('registration_link') else 
                            html.Small("Регистрация не требуется", className="text-muted")
                        ),
                        dbc.Col(
                            f"ID: {event.get('id', '??')}", 
                            className="text-end text-muted small"
                        )
                    ])
                )
            ], className="mb-3")
            cards.append(card)
        
        return cards
        
    @app.callback(
        [Output("events-form-trigger", "data", allow_duplicate=True),
         Output("delete-event-admin-alert", "children")],
        [Input("delete-event-id-button", "n_clicks")],
        [State("delete-event-id-input", "value")],
        prevent_initial_call=True
    )
    def delete_event_by_id(n_clicks, id_to_delete):
        if not n_clicks or not id_to_delete:
            alert = dbc.Alert("Ошибка: Введите ID.", color="warning")
            return dash.no_update, alert

        try:
            id_to_delete = int(id_to_delete)
        except ValueError:
            alert = dbc.Alert(f"Ошибка: ID '{id_to_delete}' должен быть числом.", color="danger")
            return dash.no_update, alert

        all_events = load_events_data()
        
        events_to_keep = [event for event in all_events if event.get('id') != id_to_delete]
        
        if len(events_to_keep) == len(all_events):
            alert = dbc.Alert(f"Ошибка: Мероприятие с ID {id_to_delete} не найдено.", color="danger")
            return dash.no_update, alert

        if save_events_data(events_to_keep):
            alert = dbc.Alert(f"Успех: Мероприятие с ID {id_to_delete} удалено.", color="success")
            return time.time(), alert
        else:
            alert = dbc.Alert("Ошибка: Не удалось сохранить (IOError).", color="danger")
            return dash.no_update, alert

    # --- "МОЗГ" 1: "ОТКРЫВАШКА" ---
    @app.callback(
        [Output("event-modal", "is_open"),
         Output("event-modal-alert", "children")],
        [Input("add-event-button", "n_clicks"),
         Input("cancel-event-button", "n_clicks"),
         Input("save-event-button", "n_clicks")],
        [State("event-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_event_modal(n_add, n_cancel, n_save, is_open):
        if n_add or n_cancel or n_save:
            return not is_open, ""
        return is_open, ""

    # --- "МОЗГ" 2: "СОХРАНЕНИЕ" ---
    @app.callback(
        [Output("events-form-trigger", "data", allow_duplicate=True),
         Output("event-modal-alert", "children", allow_duplicate=True)],
        [Input("save-event-button", "n_clicks")],
        [State("event-title-input", "value"),
         State("event-desc-input", "value"),
         State("event-location-input", "value"),
         State("event-date-input", "date"),
         State("event-time-input", "value"),
         State("event-type-input", "value")],
        prevent_initial_call=True
    )
    def save_new_event(n_clicks, title, desc, location, date, time_str, event_type):
        if not n_clicks:
            return dash.no_update, dash.no_update
            
        if not title or not desc or not location or not date or not event_type:
            alert = dbc.Alert("Ошибка: Заполните все поля (кроме времени).", color="danger", className="mt-3")
            return dash.no_update, alert

        all_events = load_events_data()
        
        new_id = (max([event['id'] for event in all_events]) + 1) if all_events else 1
        
        new_event_item = {
            "id": new_id,
            "title": title,
            "description": desc,
            "date": date,
            "time": time_str if time_str else "",
            "location": location,
            "type": event_type,
            "is_registration_required": False,
            "registration_link": ""
        }
        
        all_events.append(new_event_item)
        
        if save_events_data(all_events):
            return time.time(), dash.no_update
        else:
            alert = dbc.Alert("Ошибка: Не удалось сохранить (IOError).", color="danger", className="mt-3")
            return dash.no_update, alert