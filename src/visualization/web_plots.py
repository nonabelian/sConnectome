import numpy as np
from nilearn import datasets
import colorlover as cl
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
from bs4 import BeautifulSoup


def plot_feature_importances(names, labels, importances):
    fis = np.array(sorted(zip(names, labels, importances),
                          key=lambda x: x[2])[::-1])

    xdata = fis[:, 0].tolist()
    ydata = fis[:, 2].astype(float).tolist()
    hover_labels = fis[:, 1].tolist()

    trace0 = go.Bar(
        x=xdata,
        y=ydata,
        text=hover_labels,
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
        xaxis=dict(range=[-0.5,3]),
    )

    fig = go.Figure(data=data, layout=layout)
    divscript = offline.plot(fig, include_plotlyjs=False, output_type='div')

    soup = BeautifulSoup(divscript, 'html.parser')
    div = soup.select('div')[0]
    script = soup.select('script')[0]

    return div, script


def plot_connectome3d(coords, names, covs):

    msdl_atlas = datasets.fetch_atlas_msdl()
    bupu = cl.scales['9']['seq']['BuPu']
    bupu_interp = cl.interp(bupu, len(msdl_atlas['labels']))

    xyz = np.array(coords)
    labels = msdl_atlas['labels']
    group = range(len(xyz))

    scale_factor = 100

    Xn = xyz[:, 0]
    Yn = xyz[:, 1]
    Zn = xyz[:, 2]
    Xe = []
    Ye = []
    Ze = []

    line_traces = []


    # Add graph connections colored by correlation, alpha'd by strength
    for i, pt1 in enumerate(xyz):
        for j, pt2 in enumerate(xyz):
            if j >= i:
                break

            if abs(covs[i, j]) < 0.1:
                continue

            Xe = [pt1[0], pt2[0], None]
            Ye = [pt1[1], pt2[1], None]
            Ze = [pt1[2], pt2[2], None]

            opacity = np.sqrt(abs(covs[i, j]))

            if covs[i, j] < 0:
                c = 'blue'
            if covs[i, j] > 0:
                c = 'red'

            trace1 = go.Scatter3d(x=Xe,
                                  y=Ye,
                                  z=Ze,
                                  mode='lines',
                                  line=go.Line(color=c, width=10),
                                  hoverinfo='none',
                                  opacity=opacity
                                  )

            line_traces.append(trace1)

    # Add scatter of brain atlas regions
    trace2 = go.Scatter3d(
                    x=Xn,
                    y=Yn,
                    z=Zn,
                    mode='markers',
                    name='actors',
                    marker=go.Marker(symbol='dot',
                                  size=10,
                                  color=bupu_interp,
                                  colorscale=bupu,
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
#            title="3D Connectome of Brain Regions",
            width=700,
            height=500,
            showlegend=False,
            scene=go.Scene(xaxis=go.XAxis(axis),
                        yaxis=go.YAxis(axis),
                        zaxis=go.ZAxis(axis),
                       ),
            margin=go.Margin(t=100),
            hovermode='closest',
            annotations=go.Annotations([
                        go.Annotation(
                        showarrow=False,
                        text="sub001",
                        xref='paper',
                        yref='paper',
                        x=0,
                        y=0.1,
                        xanchor='center',
                        yanchor='bottom',
                        font=go.Font(size=14)
                        )
                    ]),
            )

    data = go.Data(line_traces + [trace2])
    fig = go.Figure(data=data, layout=layout)

    divscript = offline.plot(fig, include_plotlyjs=False, output_type='div')

    soup = BeautifulSoup(divscript, 'html.parser')
    div = soup.select('div')[0]
    script = soup.select('script')[0]

    return div, script
