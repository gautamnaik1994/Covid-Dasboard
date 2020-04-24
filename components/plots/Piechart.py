
import plotly.graph_objects as go
from helpers.constants import *
from helpers.apputils import *


def draw_pie_chart(data, name):
    fig = go.Figure(data=[
        go.Pie(labels=data[0],
               values=data[1],
               name=name, hole=.3,
               hovertemplate="%{label}<br />%{value} " +
               name + "<extra></extra>",
               textposition=list(calculateTextpositions(data[1])))
    ])
    fig.update_layout(title=f'{name} Statewise Data', height=900,
                      margin=dict(
                          l=0, r=0,
                      ),

                      title_font_size=20,
                      legend=dict(
                          orientation="h"
                      ))
    return fig


def calculateTextpositions(values):
    total = sum(values)
    # Do not display percentages < 5%
    return map(lambda v: 'none' if float(v)/total < 0.05 else 'auto', values)
