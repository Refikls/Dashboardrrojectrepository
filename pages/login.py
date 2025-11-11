import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from users_db import check_user
import dash

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
        [Output("session-store", "data"),
         Output("login-alert", "children")],
        [Input("login-button", "n_clicks")],
        [State("login-email", "value"),
         State("login-password", "value")]
    )
    def handle_login(n_clicks, email, password):
        if n_clicks == 0 or not email or not password:
            return dash.no_update, ""

        role = check_user(email, password)
        
        if role:
            return {'role': role}, dbc.Alert(f"Успех! Вход как {role}", color="success")
        else:
            return dash.no_update, dbc.Alert("Неверный email или пароль", color="danger")