import plotly.graph_objects as go
from helpers.constants import *
from helpers.apputils import *


def draw_heatmap(data, data_type, cmap="Viridis"):
    # data = data.drop(["TT", "Unnamed: 39"], axis=1)
    data = data[data["Status"] == data_type].drop("Status", axis=1)
    fig = go.Figure(data=go.Heatmap(
        z=data,
        y=data.columns,
        x=data.reset_index()["Date"],
        name="", text=data, transpose=True,
        hovertemplate="%{x}<br />State: %{y}<br />%{z} "+data_type,
        colorscale=cmap))

    fig.add_shape(
        type="line",
        x0=lockdown_day,
        y0=0,
        x1=lockdown_day,
        y1=1,
        name="Lockdown",
        yref="paper",
        line=dict(
            width=2,
            color=death_color, dash="dot"
        )
    )
    fig.add_annotation(
        yref="paper",
        x=lockdown_day,
        y=0.5, textangle=-90,
        showarrow=False, font_color="white", bgcolor=death_color, borderpad=2, font_size=12,
        text=" Lockdown ")

    fig.update_layout(
        title=f'Daily {data_type} Cases State Density', xaxis_title='Date', yaxis_title='State', height=500,
        margin=dict(
            l=0, r=0,
        ),
        title_font_size=20,
    )

    return fig
