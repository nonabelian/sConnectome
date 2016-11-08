from nilearn.connectome import GroupSparseCovarianceCV
from nilearn import datasets

from src.process_data.fmri_data import fMRIExperimentData
from src.process_data.fmri_data import generate_mni_parallel
from src.process_data.graph_data import generate_graph_parallel
from src.process_data.graph_data import GraphExperimentData


if __name__ == '__main__':

    dirlist = ['data/sub%03d/'% i for i in range(1, 103)]

    fed = fMRIExperimentData(dirlist, working_directory='data/')

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

    ged = generate_graph_parallel(ged)
