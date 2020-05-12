import plotly.graph_objects as go
from helpers.constants import *

def draw_treemap(data):
    fig = go.Figure( go.Treemap(
        ids=data['id'],
        parents=data['parent'],
        labels=data['state'],
        customdata=data['value'],
        name='Zones',
        pathbar = {"visible": True},
        hovertemplate='<b> Region: %{label}</b> <br> Zone: %{customdata}<extra></extra>',
        marker=dict(colors = get_color(data['value']) )
        ))
    fig.update_layout(title="Zones",height=900,margin=dict(t=30, b=10, r=0, l=0));
    return fig

def get_color(val):
    c=[]
    for x in val:
        if x=="Green":c.append(recovered_color)
        elif x=="Red":c.append(death_color)
        elif x=="Orange":c.append(active_color)
        else: c.append("white")
    return c

