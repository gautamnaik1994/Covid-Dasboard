
import dash
import dash_core_components as dcc
import dash_html_components as html


def Navbar(title):
    """Returns a Navbar component

        Keyword arguments:
            title -- string to display in Navbar
    """
    return html.Nav(
        className="navbar navbar-dark bg-dark",
        children=[
            html.A(children=[title], className="navbar-brand")
        ]
    )
