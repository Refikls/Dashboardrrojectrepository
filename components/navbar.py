import dash_bootstrap_components as dbc
import dash.html as html

def create_navbar():
    LOGO_PATH = '/assets/logo.png'
    navbar = dbc.NavbarSimple(
        brand=html.Span(
            [
            html.Img(src=LOGO_PATH, height="45px", style={"marginRight": "10px"}),
            
                "Дашборд Студента"
            ]
        ),
        brand_href="/",
        color="dark",
        dark=True,
        fixed="top",
    )
    return navbar