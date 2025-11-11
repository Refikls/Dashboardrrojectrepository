import json
from dash.dependencies import Input, Output
import dash.html as html
import dash_bootstrap_components as dbc

def load_news_data():
    try:
        with open('data/news.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('news', [])
    except FileNotFoundError:
        return []

def register_news_callbacks(app):
    @app.callback(
        Output('news-container', 'children'),
        [Input('news-category-filter', 'value'),
         Input('news-important-filter', 'value')]
    )
    def update_news_feed(selected_category, is_important):
        all_news = load_news_data()
        
        if is_important:
            filtered_news = [news for news in all_news if news['is_important']]
        else:
            filtered_news = all_news
        
        if selected_category:
            filtered_news = [news for news in filtered_news if news['category'] == selected_category]
        
        if not filtered_news:
            return dbc.Alert("Новости по вашим фильтрам не найдены.", color="info")
        
        filtered_news.sort(key=lambda x: x['date'], reverse=True)
        
        cards = []
        for news in filtered_news:
            card = dbc.Card(
                dbc.CardBody([
                    html.H5(news['title'], className="card-title"),
                    html.H6(news['date'], className="card-subtitle mb-2 text-muted"),
                    html.P(news['content'], className="card-text"),
                    dbc.Badge("Важно", color="danger", className="me-1") if news['is_important'] else None,
                    dbc.Badge(news['category'], color="primary", className="me-1")
                ]),
                className="mb-3"
            )
            cards.append(card)
        
        return cards