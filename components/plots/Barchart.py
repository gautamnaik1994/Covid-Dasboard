
import plotly.graph_objects as go
from helpers.constants import *
from helpers.apputils import *


def draw_bar_chart(data):
    data["Total_CADR"] = data["Recovered"] + \
        data["Confirmed"] + data["Active"] + data["Recovered"]
    data = data[data["Total_CADR"] > 0]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data["State"],
        y=data["Confirmed"],
        name='Confirmed',
        marker_color=confirmed_color, text=data[
            "Confirmed"], hovertemplate="%{x}<br />%{y} Confirmed<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=data["State"],
        y=data["Active"],
        name='Active',
        marker_color=active_color, text=data[
            "Active"], hovertemplate="%{x}<br />%{y} Active<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=data["State"],
        y=data["Recovered"],
        name='Recovered',
        marker_color=recovered_color, text=data[
            "Recovered"], hovertemplate="%{x}<br />%{y} Recovered<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=data["State"],
        y=data["Deaths"],
        name='Deaths',
        marker_color=death_color, text=data[
            "Deaths"], hovertemplate="%{x}<br />%{y} Deaths<extra></extra>",
    ))

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    fig.update_layout(title='Statewise Data', xaxis_title='State', yaxis_title='Count',
                      margin=dict(
                          l=0, r=0,
                      ),

                      legend=dict(
                          xanchor="right",
                          yanchor="bottom",
                          orientation="h",
                          x=1,
                          y=1
                      ),
                      barmode='group', xaxis_tickangle=-90,
                      height=800,
                      title_font_size=20,
                      )
    return fig
