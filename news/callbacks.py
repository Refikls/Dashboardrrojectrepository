import dash
from dash import html, dcc, Input, Output, State, callback
import pandas as pd
import json
from datetime import datetime
import dash_bootstrap_components as dbc
import time

DATA_FILE = 'data/news.json'

def load_news_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('news', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_news_data(news_list):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({'news': news_list}, f, ensure_ascii=False, indent=4)
        return True
    except IOError:
        return False

def register_news_callbacks(app):

    @app.callback(
        Output('news-container', 'children'),
        [Input('news-category-filter', 'value'),
         Input('news-important-filter', 'value'),
         Input('news-form-trigger', 'data')]
    )
    def update_news_list(category, is_important, form_trigger_timestamp):
        
        news_data = load_news_data()
        if not news_data:
            return dbc.Alert("Новостей пока нет.", color="info")

        df = pd.DataFrame(news_data)
        
        if 'date' in df.columns:
             df['date'] = pd.to_datetime(df['date'], errors='coerce')
             df = df.sort_values('date', ascending=False, na_position='last')
        
        if category:
            df = df[df['category'] == category]
        
        if is_important:
            df = df[df['is_important'] == True]

        if df.empty:
            return dbc.Alert("Новости по вашим фильтрам не найдены.", color="info")

        cards = []
        for _, row in df.iterrows():
            card_color = "danger" if row.get('is_important', False) else "secondary"
            
            title = row.get('title', 'Новость без заголовка')
            content = row.get('content', 'Нет содержания.')
            image_url = row.get('image_url')
            category_text = row.get('category', 'Новость')
            news_id = row.get('id', '??')
            
            date_str = "Дата не указана"
            if pd.notna(row.get('date')):
                try:
                    date_str = pd.to_datetime(row['date']).strftime('%d.%m.%Y')
                except Exception:
                    pass 

            card = dbc.Card([
                dbc.CardHeader(
                    dbc.Row([
                        dbc.Col(html.H5(title, className="mb-0"), width=10),
                        dbc.Col(
                            dbc.Badge(category_text, color=card_color, className="ms-1"), 
                            width=2, 
                            className="text-end"
                        )
                    ], justify="between")
                ),
                dbc.CardBody([
                    html.Img(src=image_url, style={'width': '100%', 'max-height': '200px', 'object-fit': 'cover', 'margin-bottom': '10px'}) 
                        if image_url else None,
                    html.P(content),
                ]),
                dbc.CardFooter(
                    dbc.Row([
                        dbc.Col(f"Опубликовано: {date_str}"),
                        dbc.Col(f"ID: {news_id}", className="text-end text-muted")
                    ])
                )
            ], className="mb-3")
            cards.append(card)
        
        return cards

    @app.callback(
        [Output("news-modal", "is_open"),
         Output("news-modal-alert", "children")],
        [Input("add-news-button", "n_clicks"),
         Input("cancel-news-button", "n_clicks"),
         Input("save-news-button", "n_clicks")],
        [State("news-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_news_modal(n_add, n_cancel, n_save, is_open):
        if n_add or n_cancel or n_save:
            return not is_open, ""
        return is_open, ""

    @app.callback(
        [Output("news-form-trigger", "data"),
         Output("news-modal-alert", "children", allow_duplicate=True)],
        [Input("save-news-button", "n_clicks")],
        [State("news-title-input", "value"),
         State("news-content-input", "value"),
         State("news-image-input", "value"),
         State("news-category-input", "value"),
         State("news-important-input", "value")],
        prevent_initial_call=True
    )
    def save_new_news(n_clicks, title, content, image_url, category, is_important):
        if not n_clicks:
            return dash.no_update, dash.no_update
            
        if not title or not content or not category:
            alert = dbc.Alert("Ошибка: Заполните Заголовок, Текст и Категорию.", color="danger", className="mt-3")
            return dash.no_update, alert

        all_news = load_news_data()
        
        new_id = (max([news['id'] for news in all_news]) + 1) if all_news else 1
        
        new_news_item = {
            "id": new_id,
            "title": title,
            "content": content,
            "date": datetime.now().isoformat(),
            "category": category,
            "is_important": is_important,
            "image_url": image_url if image_url else ""
        }
        
        all_news.append(new_news_item)
        
        if save_news_data(all_news):
            return time.time(), dash.no_update
        else:
            alert = dbc.Alert("Ошибка: Не удалось сохранить новость (IOError).", color="danger", className="mt-3")
            return dash.no_update, alert
            
    @app.callback(
        [Output("news-form-trigger", "data", allow_duplicate=True),
         Output("delete-admin-alert", "children")],
        [Input("delete-id-button", "n_clicks")],
        [State("delete-id-input", "value")],
        prevent_initial_call=True
    )
    def delete_news_by_id(n_clicks, id_to_delete):
        if not n_clicks or not id_to_delete:
            alert = dbc.Alert("Ошибка: Введите ID.", color="warning")
            return dash.no_update, alert

        try:
            id_to_delete = int(id_to_delete)
        except ValueError:
            alert = dbc.Alert(f"Ошибка: ID '{id_to_delete}' должен быть числом.", color="danger")
            return dash.no_update, alert

        all_news = load_news_data()
        
        news_to_keep = [news for news in all_news if news.get('id') != id_to_delete]
        
        if len(news_to_keep) == len(all_news):
            alert = dbc.Alert(f"Ошибка: Новость с ID {id_to_delete} не найдена.", color="danger")
            return dash.no_update, alert

        if save_news_data(news_to_keep):
            alert = dbc.Alert(f"Успех: Новость с ID {id_to_delete} удалена.", color="success")
            return time.time(), alert
        else:
            alert = dbc.Alert("Ошибка: Не удалось сохранить (IOError).", color="danger")
            return dash.no_update, alert