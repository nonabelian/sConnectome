import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
from bs4 import BeautifulSoup


def plot_feature_importances(names, importances):
    fis = np.array(sorted(zip(names, importances), key=lambda x: x[1])[::-1])

    trace0 = go.Bar(
        x=fis[:, 0],
        y=fis[:, 1].astype(float),
        text=fis[:, 0],
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )

    data = [trace0]
    layout = go.Layout(
        title='Significant Properties',
        xaxis=dict(range=[-0.5,3]),
    )

    fig = go.Figure(data=data, layout=layout)
    divscript = offline.plot(fig, include_plotlyjs=False, output_type='div')

    soup = BeautifulSoup(divscript, 'html.parser')
    div = soup.select('div')[0]
    script = soup.select('script')[0]

    return div, script



