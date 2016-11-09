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
#        title='Significant Properties',
        xaxis=dict(range=[-0.5,3]),
    )

    fig = go.Figure(data=data, layout=layout)
    divscript = offline.plot(fig, include_plotlyjs=False, output_type='div')

    soup = BeautifulSoup(divscript, 'html.parser')
    div = soup.select('div')[0]
    script = soup.select('script')[0]

    return div, script


def plot_connectome3d(coords, covs):

    xyz = np.array(coords)
    labels = map(str, range(len(xyz)))
    group = range(len(xyz))

    scale_factor = 100

    Xn = xyz[:, 0]
    Yn = xyz[:, 1]
    Zn = xyz[:, 2]
    Xe = []
    Ye = []
    Ze = []

    line_traces = []

    for i, pt1 in enumerate(xyz):
        for j, pt2 in enumerate(xyz):
            if j >= i:
                break

            if covs[i, j] < 0.02:
                continue

            Xe = [pt1[0], pt2[0], None]
            Ye = [pt1[1], pt2[1], None]
            Ze = [pt1[2], pt2[2], None]

            if covs[i, j] < 0:
                c_val = abs(covs[i, j])
                c = 'rgb({0},{1},{2})'.format(100, 100, scale_factor * c_val)
            if covs[i, j] > 0:
                c_val = abs(covs[i, j])
                c = 'rgb({0},{1},{2})'.format(scale_factor * c_val, 100, 100)

            trace1 = go.Scatter3d(x=Xe,
                                  y=Ye,
                                  z=Ze,
                                  mode='lines',
                                  line=go.Line(color=c, width=1),
                                  hoverinfo='none'
                                  )

            line_traces.append(trace1)

    trace2 = go.Scatter3d(
                    x=Xn,
                    y=Yn,
                    z=Zn,
                    mode='markers',
                    name='actors',
                    marker=go.Marker(symbol='dot',
                                  size=6,
                                  color=group,
                                  colorscale='Viridis',
                                  line=go.Line(color='rgb(50,50,50)', width=0.5)
                                  ),
                    text=labels,
                    hoverinfo='text'
                    )

    axis=dict(showbackground=False,
              showline=False,
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )

    layout = go.Layout(
            title="3D Connectome of Brain Region Connections",
            width=700,
            height=500,
            showlegend=False,
            scene=go.Scene(xaxis=go.XAxis(axis),
                        yaxis=go.YAxis(axis),
                        zaxis=go.ZAxis(axis),
                       ),
            margin=go.Margin(t=100),
            hovermode='closest',
            )

    data = go.Data(line_traces + [trace2])
    fig = go.Figure(data=data, layout=layout)

    divscript = offline.plot(fig, include_plotlyjs=False, output_type='div')

    soup = BeautifulSoup(divscript, 'html.parser')
    div = soup.select('div')[0]
    script = soup.select('script')[0]

    return div, script
