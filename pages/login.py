import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from users_db import check_user
import dash
import pandas as pd

def create_login_layout():
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(className="dbc", children=[
                        html.H4("Вход в систему", className="card-title text-center mb-4"),
                        dbc.Input(id="login-email", placeholder="Email @uni-dubna.ru", type="email", className="mb-3"),
                        dbc.Input(id="login-password", placeholder="Пароль", type="password", className="mb-3"),
                        dbc.Button("Войти", id="login-button", color="primary", n_clicks=0, className="w-100"),
                        html.Div(id="login-alert", className="mt-3"),
                        html.Div(dcc.Link("Нет аккаунта? Зарегистрироваться", href="/register"), className="text-center mt-3")
                    ])
                ),
                width=10, md=6, lg=4
            ),
            justify="center", className="mt-5"
        ),
        fluid=True
    )

def register_login_callbacks(app):

    @app.callback(
        Output('session-store', 'data', allow_duplicate=True),
        Input('url', 'pathname'),
        State('session-store', 'data'),
        prevent_initial_call=True
    )
    def clear_session_on_login_page_load(pathname, session_data):
        if pathname == '/login' and session_data is not None:
            return None
        return dash.no_update

    @app.callback(
        [Output("session-store", "data"),
         Output("login-alert", "children")],
        [Input("login-button", "n_clicks")],
        [State("login-email", "value"),
         State("login-password", "value")],
        prevent_initial_call=True
    )
    def handle_login(n_clicks, email, password):
        if n_clicks == 0 or not email or not password:
            return dash.no_update, ""

        base_role, permissions_str = check_user(email, password)
        
        if base_role:
            
            if pd.isna(permissions_str) or permissions_str == "":
                permissions_list = []
            else:
                permissions_list = str(permissions_str).replace(" ", "").split(',')

            if "IS_SUPER_ADMIN" in permissions_list:
                admin_tags = [
                    "EDIT_NEWS", 
                    "EDIT_SCHEDULE",
                    "EDIT_EVENTS",
                    "DELETE_NEWS", 
                    "DELETE_EVENTS", 
                    "DELETE_SCHEDULE", 
                    "EDIT_USERS"
                ]
                
                for tag in admin_tags:
                    if tag not in permissions_list:
                        permissions_list.append(tag)
            # --------------------

            session_data = {
                'base_role': base_role,
                'permissions': permissions_list
            }
            
            return session_data, dbc.Alert(f"Успех! Вход как {base_role}", color="success")
        else:
            return dash.no_update, dbc.Alert("Неверный email или пароль", color="danger")