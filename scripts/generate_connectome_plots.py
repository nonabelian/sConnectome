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

    # Our graph model -- MSDL Atlas, GroupSparseCovarianceCV
    msdl_atlas_dataset = datasets.fetch_atlas_msdl()
    gsc = GroupSparseCovarianceCV(verbose=2)

    # Use default graph properties
    ged = GraphExperimentData([gsc], fed, msdl_atlas_dataset,
                              msdl_atlas_dataset.maps)

    ged.load_graph_data()

    image_path = 'images/connectomes/'

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    for name, gd in ged.graph_data.iteritems():
        save_file = name + '_graph.png'
        save_image = os.path.join(image_path, save_file)

        plot_connectome2d(gd, save_image=save_image)
