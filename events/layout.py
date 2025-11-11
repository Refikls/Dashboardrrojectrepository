import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc
from datetime import date

def create_events_layout(session_data):
    
    user_permissions = session_data.get('permissions', [])
    
    add_event_button = None
    if "EDIT_EVENTS" in user_permissions:
        add_event_button = dbc.Button("Добавить мероприятие", color="success", className="mb-3")

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
        
        html.Div(id='events-cards-container')
    ])