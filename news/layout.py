import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc

def create_news_layout(session_data):
    categories = ["Учебный процесс", "Мероприятие", "Стипендия", "Важное объявление"]
    options = [{'label': cat, 'value': cat} for cat in categories]
    
    user_permissions = session_data.get('permissions', [])
    
    add_news_button = None
    if "EDIT_NEWS" in user_permissions:
        add_news_button = dbc.Button("Добавить новость", color="success", className="mb-3")

    return dbc.Container([
        dbc.Row(
            [
                html.H1("📰 Новости", className="mb-4"),
                add_news_button
            ],
            justify="between",
            align="center"
        ),
        
        dbc.Row([
            dbc.Col(md=3, children=[
                dbc.Card(
                    dbc.CardBody(className="dbc", children=[
                        html.H4("Фильтры", className="card-title"),
                        dcc.Dropdown(
                            id='news-category-filter',
                            options=options,
                            placeholder="Все категории",
                            clearable=True,
                            className="mb-3"
                        ),
                        dbc.Switch(
                            id='news-important-filter',
                            label="Только важное",
                            value=False,
                        ),
                    ])
                )
            ]),
            
            dbc.Col(md=9, children=[
                html.Div(
                    id='news-container', 
                    style={'maxHeight': '75vh', 'overflowY': 'auto', 'paddingRight': '15px'}
                )
            ])
        ])
    ])