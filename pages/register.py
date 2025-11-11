import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from users_db import add_user

def create_register_layout():
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(className="dbc", children=[
                        html.H4("Регистрация", className="card-title text-center mb-4"),
                        html.P("Для почты @uni-dubna.ru", className="text-muted text-center small"),
                        dbc.Input(id="reg-email", placeholder="Email @uni-dubna.ru", type="email", className="mb-3"),
                        dbc.Input(id="reg-password", placeholder="Придумайте пароль", type="password", className="mb-3"),
                        dbc.Button("Зарегистрироваться", id="reg-button", color="success", n_clicks=0, className="w-100"),
                        html.Div(id="reg-alert", className="mt-3"),
                        html.Div(dcc.Link("Уже есть аккаунт? Войти", href="/login"), className="text-center mt-3")
                    ])
                ),
                width=10, md=6, lg=4
            ),
            justify="center", className="mt-5"
        ),
        fluid=True
    )

def register_reg_callbacks(app):
    @app.callback(
        Output("reg-alert", "children"),
        [Input("reg-button", "n_clicks")],
        [State("reg-email", "value"),
         State("reg-password", "value")]
    )
    def handle_registration(n_clicks, email, password):
        if n_clicks == 0 or not email or not password:
            return ""

        success, message = add_user(email, password)
        
        if success:
            return dbc.Alert(message, color="success")
        else:
            return dbc.Alert(message, color="danger")