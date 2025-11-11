import dash_bootstrap_components as dbc
import dash.html as html

def create_navbar():
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="/assets/logo.png", height="30px")),
                            dbc.Col(dbc.NavbarBrand("Портал", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                
                dbc.Nav(
                    [dbc.NavLink("Выйти", href="/logout", active="exact", external_link=True)],
                    className="ms-auto",
                    navbar=True
                )
            ]
        ),
        color="dark",
        dark=True,
        fixed="top",
        style={"height": "3.5rem"}
    )
    return navbar