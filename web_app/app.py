import cPickle as pickle

import numpy as np
from nilearn import datasets
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import offline
from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.plotting import output_file
from bokeh.plotting import show
from flask import Flask
from flask import render_template
app = Flask(__name__)

from .context import src
from src.process_data.demographic_data import DemographicData
import src.visualization.web_plots as wp

with open('data/dataframes/graph_dataframe.pkl') as f:
    GRAPH_DATA = pickle.load(f)

with open('data/models/graph_model.pkl') as f:
    GRAPH_MODEL = pickle.load(f)

with open('data/dataframes/meta_dataframe.pkl') as f:
    META_DATA = pickle.load(f)

with open('data/models/meta_model.pkl') as f:
    META_MODEL = pickle.load(f)
#GRAPH_DATA=None
#GRAPH_MODEL=None
#META_DATA=None
#META_MODEL=None


@app.route('/')
def index():
    m_fi_div, m_fi_script = plot_meta_feature_importances()
    c3d_div, c3d_script = plot_graph_connectome_3d()
    g_fi_div, g_fi_script = plot_graph_feature_importances()

    coords = get_region_coords()

    return render_template('scroll_me.html', title='sConnectome',
                           m_fi_div=m_fi_div, m_fi_script=m_fi_script,
                           c3d_div=c3d_div, c3d_script=c3d_script,
                           g_fi_div=g_fi_div, g_fi_script=g_fi_script,
                           connectome_coords=coords)


def get_region_coords():
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()

    np_coords = np.array(msdl_atlas_dataset['region_coords'])

    return list(np_coords)


def plot_meta_feature_importances():
    names = META_DATA['columns']
    percents = META_MODEL.feature_importances_

    div, script = wp.plot_feature_importances(names, names, percents)

    return div, script


def plot_graph_connectome_3d():
    coords = get_region_coords()
    msdl_atlas = datasets.fetch_atlas_msdl()
    names = msdl_atlas['labels']
    graph_file = 'data/graphs/sub001_graph_data.pkl'

    with open(graph_file) as f:
        data = pickle.load(f)

    covs = data['norm_cov']

    div, script = wp.plot_connectome3d(coords, names, covs)

    return div, script


def plot_graph_feature_importances():
    names = GRAPH_DATA['columns']
    percents = GRAPH_MODEL.feature_importances_

    msdl_atlas = datasets.fetch_atlas_msdl()
    labels = msdl_atlas['labels']

    proper_names = []

    for n in names:
        if str.isdigit(n[-1]):
            idx = int(filter(str.isdigit, n))
            proper_names.append(labels[idx])
        else:
            proper_names.append(n)

    div, script = wp.plot_feature_importances(names, proper_names, percents)

    return div, script


def run_app():
    with open('data/dataframes/graph_dataframe.pkl') as f:
        GRAPH_DATA = pickle.load(f)

    with open('data/models/graph_model.pkl') as f:
        GRAPH_MODEL = pickle.load(f)

    with open('data/dataframes/meta_dataframe.pkl') as f:
        META_DATA = pickle.load(f)

    with open('data/models/meta_model.pkl') as f:
        META_MODEL = pickle.load(f)

    app.run(host='0.0.0.0', port=8080, debug=True)
