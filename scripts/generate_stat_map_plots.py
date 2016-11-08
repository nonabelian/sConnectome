import os

from nilearn import datasets
from nilearn.connectome import GroupSparseCovarianceCV

from src.process_data.fmri_data import fMRIExperimentData
from src.process_data.graph_data import GraphExperimentData
from src.visualization.plot_graphs import plot_connectome2d
from src.visualization.plot_graphs import plot_filtered_mni

if __name__ == '__main__':

    dirlist = ['data/sub%03d/'% i for i in range(1, 103)]

    fed = fMRIExperimentData(dirs, working_directory='data/')

    # Load the MNI files into the class
    fed.load_subject_mni()

    image_path = 'images/stat_maps/'

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    for fsd in fed.iter_subject_data():
        for ftd in fsd.iter_task_data():

            save_file = fsd.name + ftd.name + '_mni.png'
            save_image = os.path.join(image_path, save_file)

            plot_filtered_mni(ftd, save_image=save_image)

