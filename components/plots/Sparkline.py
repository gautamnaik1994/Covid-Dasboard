import plotly.graph_objects as go
from helpers.constants import *
from helpers.apputils import *


def draw_sparkline_chart(data):
    # data = df_cases_time_series
    # data = data.reset_index()
    # fillcolor='#d0d1ec'
    date = data[0]
    C = data[1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date, y=C,
                             mode='lines',
                             line_shape='spline', line_smoothing=1.3,
                             line_color=color_variant(confirmed_color, 50),  fill='tozeroy',
                             ))

    fig.update_layout(margin=dict(l=0, r=0, t=0,
                                  b=0), xaxis_visible=False,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      yaxis_visible=False,)

    return fig
