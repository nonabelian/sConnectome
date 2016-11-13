import os
import nose.tools as n

import numpy as np
import networkx as nx
from nilearn import datasets
from nilearn.connectome import GroupSparseCovarianceCV
from nilearn import input_data

from .context import src
from src.process_data.fmri_data import fMRIExperimentData
from src.process_data.fmri_data import fMRISubjectData
from src.process_data.fmri_data import generate_mni_parallel
from src.process_data.graph_data import GraphExperimentData
from src.process_data.graph_data import GraphSubjectData
from src.process_data.graph_data import generate_graphs_parallel
from src.process_data.graph_data import generate_graph_threaded
from src.process_data.graph_data import cov_to_mat
from get_message import get_message


def testGraphExperimentData():
    # Setup a GraphExperimentData class
    dirs = [os.path.join('data', 'sub')]
    wd = 'data'

    fed = fMRIExperimentData(dirs, working_directory=wd)

    # Generate the MNI files
    generate_mni_parallel(fed)

    # Load the MNI files into the class
    fed.load_subject_mni()

    # Our graph model -- MSDL Atlas, GroupSparseCovarianceCV
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV(verbose=2)
    properties = ['average_node_connectivity', 'degree_centrality']

    ged = GraphExperimentData([gsc], fed, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps, properties=properties)

    # Test the GraphExperimentData class nontrivial attributes:

    exp = ['sub']
    act = ged.graph_data.keys()
    n.assert_equal(exp, act, msg=get_message('Graph Key', exp, act))
    

def testGraphSubjectData():
    # Setup a GraphSubjectData class:
    d = os.path.join('data', 'sub')
    wd = 'data'

    fsd = fMRISubjectData(d, working_directory=wd)

    # Our graph model -- MSDL Atlas, GroupSparseCovarianceCV
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV(verbose=2)
    properties = ['average_node_connectivity', 'degree_centrality']

    gd = GraphSubjectData([gsc], fsd, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps, properties=properties)

    # Test GraphSubjectData class nontrivial attributes:

    exp = 1
    act = len(gd.models)
    n.assert_equal(exp, act, msg=get_message('Length of Models', exp, act))

    exp = True
    act = isinstance(gd.models[0], GroupSparseCovarianceCV)
    n.assert_equal(exp, act, msg=get_message('Model Instance', exp, act))

    exp = True
    act = isinstance(gd.masker, input_data.NiftiMapsMasker)
    n.assert_equal(exp, act, msg=get_message('Masker Type Check', exp, act))

    exp = ['average_node_connectivity', 'degree_centrality']
    act = gd.properties
    n.assert_equal(exp, act, msg=get_message('Graph Properties', exp, act))


def test_cov_to_mat():
    mat = np.array([[1, -.5], [-1.1, 1]])
    exp = np.array([[1, 0], [0, 1]]).tolist()
    act = cov_to_mat(mat, sign_to_keep=1).tolist()
    n.assert_equal(exp, act, msg=get_message('Graph Matrix', exp, act))


def test_generate_graph_threaded():
    # Setup a GraphSubjectData class:
    d = os.path.join('data', 'sub')
    wd = 'data'

    fsd = fMRISubjectData(d, working_directory=wd)

    fsd.load_task_mni()

    # Our graph model -- MSDL Atlas, GroupSparseCovarianceCV
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV(verbose=2)
    properties = ['average_node_connectivity', 'degree_centrality']

    gd = GraphSubjectData([gsc], fsd, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps, properties=properties)


    gd = generate_graph_threaded(gd)

    exp = np.ndarray
    act = type(gd.norm_cov)
    n.assert_equal(exp, act, msg=get_message('Type Graph Matrix', exp, act))

    exp = True
    act = isinstance(gd.graph, nx.classes.graph.Graph)
    n.assert_equal(exp, act, msg=get_message('Type Graph', exp, act))


def test_generate_graphs_parallel():
    # Setup a GraphExperimentData class
    dirs = [os.path.join('data', 'sub')]
    wd = 'data'

    fed = fMRIExperimentData(dirs, working_directory=wd)

    # Generate the MNI files
    generate_mni_parallel(fed)

    # Load the MNI files into the class
    fed.load_subject_mni()

    # Our graph model -- MSDL Atlas, GroupSparseCovarianceCV
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV(verbose=2)
    properties = ['average_node_connectivity', 'degree_centrality']

    ged = GraphExperimentData([gsc], fed, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps, properties=properties)

    ged = generate_graphs_parallel(ged)

    exp = np.ndarray
    act = type(ged.graph_data['sub'].norm_cov)
    n.assert_equal(exp, act, msg=get_message('Type Graph Matrix', exp, act))

    exp = True
    act = isinstance(ged.graph_data['sub'].graph, nx.classes.graph.Graph)
    n.assert_equal(exp, act, msg=get_message('Type Graph', exp, act))


def test_save_graph_data():
    # Setup the GraphExperimentData class
    dirs = [os.path.join('data', 'sub')]
    wd = 'data'
    fed = fMRIExperimentData(dirs, working_directory=wd)
    generate_mni_parallel(fed)
    fed.load_subject_mni()
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV()
    ged = GraphExperimentData([gsc], fed, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps)

    ged = generate_graphs_parallel(ged)

    # Test

    # Generate the graph data:
    for name, gd in ged.graph_data.iteritems():
        gd.calculate_graph_properties()
        save_directory = os.path.join('data', 'graphs')
        gd.save_graph_data(save_directory=save_directory)

    save_file = os.path.join('data', 'graphs', 'sub_graph_data.pkl')

    exp = True
    act = os.path.exists(save_file)
    n.assert_equal(exp, act, msg=get_message('Graph Save File', exp, act))


def test_load_graph_data():
    # Setup the GraphExperimentData class
    dirs = [os.path.join('data', 'sub')]
    wd = 'data'
    fed = fMRIExperimentData(dirs, working_directory=wd)
    generate_mni_parallel(fed)
    fed.load_subject_mni()
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV()
    ged = GraphExperimentData([gsc], fed, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps)

    # Test loading functionality

    # Load
    ged.load_graph_data()

    exp = np.ndarray
    act = type(ged.graph_data['sub'].norm_cov)
    n.assert_equal(exp, act, msg=get_message('Type Graph Matrix', exp, act))

    exp = True
    act = isinstance(ged.graph_data['sub'].graph, nx.classes.graph.Graph)
    n.assert_equal(exp, act, msg=get_message('Type Graph', exp, act))

    exp = False
    act = (ged.graph_data['sub'].properties == {})
    n.assert_equal(exp, act, msg=get_message('Empty Properties', exp, act))
