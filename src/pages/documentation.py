import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(
    [
        html.H1("Documentation"),
        html.P("This is the documentation page! Under Developement!"),
    ]
)
