# Разметка модуля


import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc

def create_schedule_layout():
    return dbc.Container([
        html.H1("📅 Расписание", className="mb-4"),
        
        # Фильтры и управление
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Фильтры", className="card-title"),
                        dcc.Dropdown(
                            id='group-filter',
                            options=[
                                {'label': 'Группа 1', 'value': 'group1'},
                                {'label': 'Группа 2', 'value': 'group2'},
                            ],
                            placeholder="Выберите группу"
                        ),
                        dcc.DatePickerSingle(
                            id='date-picker',
                            display_format='DD.MM.YYYY',
                            className="mt-3"
                        )
                    ])
                ])
            ], width=3),
            
            # Основное расписание
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Расписание занятий", className="card-title"),
                        html.Div(id="schedule-table")
                    ])
                ])
            ], width=9)
        ])
    ])