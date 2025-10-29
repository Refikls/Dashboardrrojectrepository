import dash_bootstrap_components as dbc
import dash.html as html

def create_navbar():
    navbar = dbc.NavbarSimple(
        brand=html.Span(
            [
                "Дашборд Студента"
            ]
        ),
        brand_href="/",
        color="primary",
        dark=True,
        fixed="top",
    )
    return navbar