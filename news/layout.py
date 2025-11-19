import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc

def create_news_layout(session_data):
    categories = ["Учебный процесс", "Мероприятие", "Стипендия", "Важное объявление"]
    options = [{'label': cat, 'value': cat} for cat in categories]
    
    user_permissions = session_data.get('permissions', [])
    
    add_news_button = None
    if "EDIT_NEWS" in user_permissions:
        add_news_button = dbc.Button("Добавить новость", id="add-news-button", color="success", className="mb-3")

    admin_delete_controls = None
    if "DELETE_NEWS" in user_permissions:
        admin_delete_controls = dbc.Card(
            dbc.CardBody([
                html.H5("Панель Администратора", className="card-title"),
                dbc.InputGroup([
                    dbc.Input(id="delete-id-input", placeholder="ID новости для удаления", type="number"),
                    dbc.Button("Удалить по ID", id="delete-id-button", color="danger"),
                ]),
                html.Div(id="delete-admin-alert")
            ]),
            color="dark",
            className="mb-3"
        )

    modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Добавление новости")),
            dbc.ModalBody(
                [
                dbc.Form([
                    dbc.Input(id="news-title-input", placeholder="Заголовок", className="mb-3"),
                    dbc.Textarea(id="news-content-input", placeholder="Текст новости", className="mb-3", style={"height": "150px"}),
                    dbc.Input(id="news-image-input", placeholder="URL картинки (необязательно)", className="mb-3"),
                    dcc.Dropdown(
                        id='news-category-input',
                        options=options,
                        placeholder="Выберите категорию",
                        className="mb-3"
                    ),
                    dbc.Switch(
                        id='news-important-input',
                        label="Важное объявление",
                        value=False,
                        className="mb-3"
                    ),
                ]),
                html.Div(id="news-modal-alert")
                ]
            ),
            dbc.ModalFooter(
                [
                    dbc.Button("Отмена", id="cancel-news-button", color="secondary"),
                    dbc.Button("Сохранить", id="save-news-button", color="primary")
                ]
            ),
        ],
        id="news-modal",
        is_open=False,
    )

    return dbc.Container([
        dbc.Row(
            [
                html.H1("📰 Новости", className="mb-4"),
                add_news_button
            ],
            justify="between",
            align="center"
        ),
        
        admin_delete_controls,
        
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
        ]),
        modal,
        dcc.Store(id='news-form-trigger')
    ])