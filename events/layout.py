import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc
from datetime import date

def create_events_layout(session_data):
    
    user_permissions = session_data.get('permissions', [])
    
    add_event_button = None
    if "EDIT_EVENTS" in user_permissions:
        add_event_button = dbc.Button("Добавить мероприятие", id="add-event-button", color="success", className="mb-3")

    admin_delete_controls = None
    if "DELETE_EVENTS" in user_permissions:
        admin_delete_controls = html.Div([
            html.H5("Панель Администратора", className="card-title"),
            dbc.InputGroup([
                dbc.Input(id="delete-event-id-input", placeholder="ID мероприятия для удаления", type="number"),
                dbc.Button("Удалить по ID", id="delete-event-id-button", color="danger"),
            ]),
            html.Div(id="delete-event-admin-alert"),
            html.Hr(className="my-3") 
        ], className="mb-3")

    modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Добавление мероприятия")),
            dbc.ModalBody(
                [
                dbc.Form([
                    dbc.Input(id="event-title-input", placeholder="Название", className="mb-3"),
                    dbc.Textarea(id="event-desc-input", placeholder="Описание", className="mb-3", style={"height": "100px"}),
                    dbc.Input(id="event-location-input", placeholder="Место", className="mb-3"),
                    
                    html.Label("Дата мероприятия:", className="fw-bold mb-2"),
                    dcc.DatePickerSingle(
                        id='event-date-input',
                        display_format='DD.MM.YYYY',
                        className="mb-3 w-100",
                        date=date.today()
                    ),
                    
                    html.Label("Время (необязательно, напр: 14:00):", className="fw-bold mb-2"),
                    dbc.Input(id="event-time-input", placeholder="14:00", className="mb-3"),
                    
                    html.Label("Тип мероприятия:", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        id='event-type-input',
                        options=[
                            {'label': 'Хакатон', 'value': 'Хакатон'},
                            {'label': 'Лекция', 'value': 'Лекция'},
                            {'label': 'Конференция', 'value': 'Конференция'},
                            {'label': 'Мастер-класс', 'value': 'Мастер-класс'},
                            {'label': 'Спортивное соревнование', 'value': 'Спортивное соревнование'},
                            {'label': 'День открытых дверей', 'value': 'День открытых дверей'},
                        ],
                        placeholder="Выберите тип",
                        className="mb-3"
                    ),
                ]),
                html.Div(id="event-modal-alert")
                ]
            ),
            dbc.ModalFooter(
                [
                    dbc.Button("Отмена", id="cancel-event-button", color="secondary"),
                    dbc.Button("Сохранить", id="save-event-button", color="primary")
                ]
            ),
        ],
        id="event-modal",
        is_open=False,
    )

    return html.Div([
        dbc.Row(
            [
                html.H1("📅 Мероприятия", className="mb-4"),
                add_event_button
            ],
            justify="between",
            align="center"
        ),
        
        html.P("Календарь событий и мероприятий университета", 
               className="text-muted mb-4"),
        
        dbc.Card([
            dbc.CardBody([
                
                admin_delete_controls,

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
                            placeholder="Загрузка...",
                            value='all',
                            clearable=False,
                            className="events-dropdown"
                        )
                    ], md=6, className="mb-3")
                ])
            ])
        ], className="mb-4 bg-secondary"),
        
        html.Div(id='events-cards-container'),
        
        dcc.Store(id='events-form-trigger'),
        modal
    ])