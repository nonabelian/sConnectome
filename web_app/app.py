import os
import cPickle as pickle

import numpy as np
#from nilearn import datasets
from flask import Flask
from flask import render_template
application = app = Flask(__name__)

from context import src
from src.process_data.demographic_data import DemographicData
import src.visualization.web_plots as wp

WEB_ROOT = os.path.dirname(__file__)
DATA_DIR = os.path.join(WEB_ROOT, os.pardir, 'data')

graph_data = os.path.join(DATA_DIR, 'dataframes', 'graph_dataframe.pkl')
graph_model = os.path.join(DATA_DIR, 'models', 'graph_model.pkl')
meta_data = os.path.join(DATA_DIR, 'dataframes', 'meta_dataframe.pkl')
meta_model = os.path.join(DATA_DIR, 'models', 'meta_model.pkl')
sub001_graph_file = os.path.join(DATA_DIR,'graphs','sub001_graph_data.pkl')
ATLAS_COORDS_FILE = os.path.join(DATA_DIR, 'models', 'atlas_coords.npy')
ATLAS_NAMES_FILE = os.path.join(DATA_DIR, 'models', 'atlas_names.npy')

with open(graph_data) as f:
    GRAPH_DATA = pickle.load(f)

with open(graph_model) as f:
    GRAPH_MODEL = pickle.load(f)

with open(meta_data) as f:
    META_DATA = pickle.load(f)

with open(meta_model) as f:
    META_MODEL = pickle.load(f)

with open(sub001_graph_file) as f:
    SUB001_GRAPH_DATA = pickle.load(f)


@app.route('/')
def index():
    m_fi_div, m_fi_script = plot_meta_feature_importances()
    c3d_div, c3d_script = plot_graph_connectome_3d()
    g_fi_div, g_fi_script = plot_graph_feature_importances()

    names, coords = get_region_coords()

    return render_template('scroll_me.html', title='sConnectome',
                           m_fi_div=m_fi_div, m_fi_script=m_fi_script,
                           c3d_div=c3d_div, c3d_script=c3d_script,
                           g_fi_div=g_fi_div, g_fi_script=g_fi_script,
                           connectome_coords=coords)


def get_region_coords():
#    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
#    np_coords = np.array(msdl_atlas_dataset['region_coords'])
    np_coords = np.load(ATLAS_COORDS_FILE)
    names = np.load(ATLAS_NAMES_FILE)

    return names, list(np_coords)


def plot_meta_feature_importances():
    names = META_DATA['columns']
    percents = META_MODEL.feature_importances_

    div, script = wp.plot_feature_importances(names, names, percents)

    return div, script


def plot_graph_connectome_3d():
    names, coords = get_region_coords()
    covs = -SUB001_GRAPH_DATA['norm_cov']

    div, script = wp.plot_connectome3d(coords, names, covs)

    return div, script


def plot_graph_feature_importances():
    names = GRAPH_DATA['columns']
    percents = GRAPH_MODEL.feature_importances_

    labels, coords = get_region_coords()

    # Extract the corresponding MSDL brain region names
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
    app.run(host='0.0.0.0', port=8080, debug=True)
