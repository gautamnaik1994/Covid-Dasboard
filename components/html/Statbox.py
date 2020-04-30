import dash_html_components as html
from components.plots.Sparkline import draw_sparkline_chart
from helpers.apputils import comma_number

import dash_core_components as dcc


def Statbox(name, value, color, secondary_name, secondary_value, confirmed,
            className=""):
    '''Returns a Statbox component

        Parameters:
            name (str): Name of stat and also name of class applied
            value (int): value of stat
            color (str): color of items
            secondary_name (str): secondary text
            secondary_value (int): secondary value
            confirmed(int) : Total Confimed
            className (string): classname

        Returns:
            html.Div:A div
    '''
    percentage = ((value/confirmed)*100).astype(int)
    # print(f'{percentage} = {value} /{confirmed}')
    return html.Div(
        className=f'statbox {className}',
        children=[
            html.Div(name, className=f'text-{color} name'),
            html.Div("{:,}".format(value), className="value"),
            html.Div(
                  html.Div(className="secondary", children=[
                      secondary_name, " : ", "▲" if secondary_value > 0 else "▼", html.Strong(
                          comma_number(secondary_value))
                  ])
            ),
            html.Div(f"{percentage}%", className=f'percentage bg-{color}')
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


def draw_arrow(value):
    if value > 0:
        return ['▲']
    else:
        return ['▼']
