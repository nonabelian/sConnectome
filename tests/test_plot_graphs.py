import os
import nose.tools as n

from nilearn import datasets
from nilearn.connectome import GroupSparseCovarianceCV

from .context import src
from src.process_data.fmri_data import fMRIExperimentData
from src.process_data.graph_data import GraphExperimentData
from src.visualization.plot_graphs import plot_connectome2d
from src.visualization.plot_graphs import plot_filtered_mni
from get_message import get_message


def test_plot_connectome2d():
    dirs = [os.path.join('data', 'sub')]
    wd = 'data'
    fed = fMRIExperimentData(dirs, working_directory=wd)

    # Load the MNI files into the class
    fed.load_subject_mni()

    # Our graph model -- MSDL Atlas, GroupSparseCovarianceCV
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV(verbose=2)

    # Use default graph properties
    ged = GraphExperimentData([gsc], fed, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps)

    ged.load_graph_data()

    image_path = os.path.join('data', 'images')

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    for name, gd in ged.graph_data.iteritems():
        save_file = name + '_graph.png'
        save_image = os.path.join(image_path, save_file)

        plot_connectome2d(gd, save_image=save_image)


def test_plot_filtered_mni():
    dirs = [os.path.join('data', 'sub')]
    wd = 'data'
    fed = fMRIExperimentData(dirs, working_directory=wd)

    # Load the MNI files into the class
    fed.load_subject_mni()

    image_path = os.path.join('data', 'images')

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    for fsd in fed.iter_subject_data():
        for ftd in fsd.iter_task_data():

            save_file = fsd.name + ftd.name + '_mni.png'
            save_image = os.path.join(image_path, save_file)

            plot_filtered_mni(ftd, save_image=save_image)
