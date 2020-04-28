import dash_html_components as html


def Navbar(title):
    """Returns a Navbar component

        Keyword arguments:
            title -- string to display in Navbar
    """
    return html.Nav(
        className="navbar ",
        children=[
            html.A(children=[title], className="navbar-brand")
        ]
    )
