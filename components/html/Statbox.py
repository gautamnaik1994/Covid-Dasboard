import dash_html_components as html
from components.plots.Sparkline import draw_sparkline_chart

import dash_core_components as dcc


def Statbox(name, value, className=""):
    '''Returns a Statbox component

    Parameters:
        name (str): Name of stat and also name of class applied
        value (int): value of stat
        className (string): classname

    Returns:
        html.Div:A div
    '''
    return html.Div(
        className=f'statbox {name} {className}',
        children=[
            html.Div(name, className="name"),
            html.Div(value, className="value")
        ]
    )


def StatboxBig(name, value, other_info, secondary_name, secondary_value, data, color, className=""):
    '''Returns a Big Statbox component

    Parameters:
        name (str): Name of stat and also name of class applied
        value (int): value of stat
        other_info (dictionary):  More info to display below main value
        secondary_name (string): secondary name
        secondary_value (int): secondary value
        data (array): data for sparkline
        className (string): classname
        color (string): color

    Returns:
        html.Div:A div
    '''
    return html.Div(
        className=f'statbox big  {className}',
        children=[
            dcc.Graph(figure=draw_sparkline_chart(data),
                      className="sparkline", config={'displayModeBar': False}),
            html.Div(name, className=f'text-{color} name'),
            html.Div("{:,}".format(value), className="value"),
            html.Div(children=[
                html.Div(className="secondary", children=[
                    key, " : ", html.Strong(other_info[key])
                ]) for key in other_info
            ], className="one-rem-mt")
        ]
    )


def comma_number(value):
    return "{:,}".format(value)

