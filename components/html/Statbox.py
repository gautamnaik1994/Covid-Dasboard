import dash_html_components as html


def Statbox(name, value):
    '''Returns a Statbox component

    Parameters:
        name (str): Name of stat
        value (int): value of stat

    Returns:
        html.Div:A div
    '''
    return html.Div(
        className="statbox",
        children=[
            html.P(name),
            html.Div(value)
        ]
    )
