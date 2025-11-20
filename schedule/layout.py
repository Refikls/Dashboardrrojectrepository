import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

def create_schedule_layout(session_data):
    
    user_permissions = session_data.get('permissions', [])
    
    edit_schedule_button = None
    if "EDIT_SCHEDULE" in user_permissions:
        edit_schedule_button = dbc.Button("Редактировать расписание", color="danger", className="mt-3")

    return dbc.Container([
        html.H1("📅 Расписание", className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody(className="dbc", children=[
                        html.H4("Фильтры", className="card-title"),
                        dcc.Dropdown(
                            id='group-filter',
                            options=[
                                {'label': 'Группа 3281', 'value': '3281'}, 
                            ],
                            value='3281',
                            placeholder="Выберите группу",
                            clearable=False
                        ),
                        dcc.DatePickerSingle(
                            id='date-picker',
                            display_format='DD.MM.YYYY',
                            className="mt-3 w-100",
                            date=datetime.today().date()
                        ),
                        edit_schedule_button
                    ])
                ])
            ], width=4, md=3),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id="schedule-title", className="card-title"),
                        html.Div(id="schedule-table")
                    ])
                ])
            ], width=8, md=9)
        ])

        ### Новое


        # , html.H1("📅 Расписание", className="mb-4"),
        
        # dbc.Row([
        #     dbc.Col([
        #         dbc.Card([
        #             dbc.CardBody(className="dbc", children=[
        #                 html.H4("Фильтры", className="card-title"),
        #                 dcc.Dropdown(
        #                     id='group-filter',
        #                     options=[
        #                         {'label': 'Группа 3281', 'value': '3281'}, 
        #                     ],
        #                     value='3281',
        #                     placeholder="Выберите группу",
        #                     clearable=False      
        #                 ),
        #                 dcc.DatePickerSingle(
        #                     id='date-picker',
        #                     display_format='DD.MM.YYYY',
        #                     className="mt-3 w-100",
        #                     date=datetime.today().date() + timedelta(days = 1)
        #                 ),
        #                 edit_schedule_button
        #             ])
        #         ])
        #     ], width=4, md=3),
            
        #     dbc.Col([
        #         dbc.Card([
        #             dbc.CardBody([
        #                 html.H4(id="schedule-title", className="card-title"),
        #                 html.Div(id="schedule-table")
        #             ])
        #         ])
        #     ], width=8, md=9)
        # ])
        
    ])