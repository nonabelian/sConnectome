import nose.tools as n

from nilearn import datasets
from nilearn.connectome import GroupSparseCovarianceCV

from .context import src
from src.process_data.fmri_data import fMRIExperimentData
from src.process_data.fmri_data import generate_mni_parallel
from src.process_data.fmri_data import generate_mni_threaded
from src.process_data.graph_data import GraphExperimentData
from src.process_data.graph_data import generate_graphs_parallel
from get_message import get_message


def testGraphExperimentData():
    dirs = ['data/sub']
    fed = fMRIExperimentData(dirs, working_directory='data/')

    # Generate the MNI files
    generate_mni_parallel(fed)

    # Load the MNI files into the class
    fed.load_subject_mni()

    # Our graph model -- MSDL Atlas, GroupSparseCovarianceCV
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV(verbose=2)

    # Use default graph properties
    ged = GraphExperimentData([gsc], fed, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps)

    ged = generate_graphs_parallel(ged)


def test_load_graph_data():
    pass


def test_save_graph_data():
    dirs = ['data/sub']
    fed = fMRIExperimentData(dirs, working_directory='data/')

    # Generate the MNI files
    generate_mni_parallel(fed)

    # Load the MNI files into the class
    fed.load_subject_mni()

    # Our graph model -- MSDL Atlas, GroupSparseCovarianceCV
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV(verbose=2)

    # Use default graph properties
    ged = GraphExperimentData([gsc], fed, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps)

    ged = generate_graphs_parallel(ged)

    ged.save_graph_data()


def test_generate_graph_threaded():
    pass

def test_generate_graphs_parallel():
    pass

