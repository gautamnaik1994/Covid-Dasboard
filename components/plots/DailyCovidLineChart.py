import plotly.graph_objects as go
from helpers.constants import *
from helpers.apputils import *


def draw_line_chart(data, graph_type, xaxis_range=[]):
    data = data.reset_index()

    if graph_type == 'daily':
        graph_name = 'Daily'
        date = data["Date"]
        A = data["Daily Active"]
        C = data["Daily Confirmed"]
        D = data["Daily Deceased"]
        R = data["Daily Recovered"]
    else:
        graph_name = 'Cumilative'
        date = data["Date"]
        A = data["Total Active"]
        C = data["Total Confirmed"]
        D = data["Total Deceased"]
        R = data["Total Recovered"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date, y=D,
                             mode='lines+markers', name='Deceased',
                             line_shape='spline', line_color=death_color, hovertemplate="%{x}<br />%{y} Deceased<extra></extra>",
                             ))
    fig.add_trace(go.Scatter(x=date, y=C,
                             mode='lines+markers', name='Confirmed',
                             line_shape='spline', line_color=confirmed_color, hovertemplate="%{x}<br />%{y} Confirmed<extra></extra>",
                             ))
    fig.add_trace(go.Scatter(x=date, y=R,
                             mode='lines+markers', name='Recovered',
                             line_shape='spline', line_color=recovered_color, hovertemplate="%{x}<br />%{y} Recovered<extra></extra>",
                             ))
    fig.add_trace(go.Scatter(x=date, y=A,
                             mode='lines+markers', name='Active',
                             line_shape='spline', line_color=active_color, hovertemplate="%{x}<br />%{y} Active<extra></extra>",
                             ))

    fig.add_shape(
        x0=tabliqui_start,
        y0=0,
        x1=tabliqui_end,
        y1=1,
        yref="paper",
        line=dict(
            color=death_color,
        ),
        fillcolor=death_color,
        opacity=0.2,

    )

    fig.add_shape(
        type="line",
        x0=lockdown_day,
        y0=0,
        x1=lockdown_day,
        y1=1,
        yref="paper",
        name="Lockdown",
        line=dict(
            width=2, dash="dot", color=death_color,
        )
    )
    fig.add_shape(
        type="line",
        x0=public_gathering_ban,
        y0=0,
        x1=public_gathering_ban,
        y1=1,
        yref="paper",
        name="public_gathering_ban",
        line=dict(
            width=2,
            dash="dot", color=confirmed_color,
        )
    )

    # fig.add_trace(go.Scatter(
    #     x = [date_to_utc("11/03/2020")],
    #     y = [max_values_confirmed / 2],
    #     mode = "text",
    #     text = ["Tabliqui Time Period"],
    #     textposition = "bottom left",
    #     showlegend = False
    # ))

    fig.add_annotation(
        x=tabliqui_start,
        yref="paper",
        y=0.5,
        showarrow=False, xanchor="left", xshift=20,
        text="Tabliqui Event")

    fig.add_annotation(
        x=lockdown_day,
        yref="paper",
        y=0.5, textangle=-90,
        showarrow=False, font_color="white", bgcolor=death_color, borderpad=2, font_size=12,
        text=" Lockdown ")

    fig.add_annotation(
        x=public_gathering_ban,
        yref="paper",
        y=0.5, textangle=-90,
        showarrow=False, font_color="white", bgcolor=confirmed_color, borderpad=2, font_size=12,
        text="Ban on Public Gathering")

    fig.update_layout(title=graph_name, xaxis_title='Date',  height=500,
                      xaxis_range=[date_to_utc("01/01/2020"),
                                   date_to_utc("01/03/2020")],
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
                      title_font_size=20,
                      )

    if len(xaxis_range) != 0:
        fig.update_layout(xaxis_range=xaxis_range)

#     if isLog:
#     fig.update_layout(yaxis_type="log")
    # Add dropdown
#     fig.update_layout(
#         updatemenus=[
#             dict(
#                 buttons=list([
#                     dict(
#                         args=["yaxis_type", "log"],
#                         label="Log",
#                         method="relayout"
#                     ),
#                     dict(
#                         args=["yaxis_type", "linear"],
#                         label="Linear",
#                         method="relayout"
#                     )
#                 ]),
#                 direction="down",
#                 pad={"r": 10, "t": 10},
#                 showactive=True,
#                 x=0.1,
#                 xanchor="left",
#                 y=1.1,
#                 yanchor="top"
#             ),
#         ]
#     )

    fig.update_xaxes(rangeslider_visible=False,
                     rangeselector=dict(y=-0.1, x=1, yanchor="top", xanchor="right",
                                        buttons=list([
                                            dict(count=1, label="1m", step="month",
                                                 stepmode="backward"),
                                            dict(step="all")
                                        ])
                                        ))
    # fig.show()
    return fig
