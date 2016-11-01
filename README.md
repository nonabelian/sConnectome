# Connectome for Schizophrenic and Healthy Individuals

We investigate an fMRI dataset comparing healthy individuals to individuals
diagnosed with schizophrenia. There are two main motivations for this project.
The first is to find functioning neurological processes that indicate illness
or susceptibility to illness.  This can be demonstrated in an accurate
classification or clustering of individuals. The second is to create
data-driven visualization and presentation of results.

The current belief is that connectivity between functional components is
significantly different in individuals with schizophrenia.

We find that ...

![High Resolution fMRI](images/highres_cutplane.png)

## Results



## Methods

We use the following packages:

* pandas -- Data manipulation (e.g. demographics.txt)
* sklearn -- Machine learning in python.
* nibabel -- Working with Nifti files.
* nilearn -- Machine learning on fMRI data.
* nipy -- fMRI manipulation tools in python.
* mayavi -- 2D/3D visualization.


## Data

The data are located at https://openfmri.org/dataset/ds000115/ [3].

The AWS hosted files consist of raw fMRI images for 102 patients in addition
to many preprocessed derivatives.  The data comes with an interesting
'demographics.txt' file, providing additional data for most of the subjects.

The data present two distinct challenges:

* Unfortunately the authors of the dataset have not also published the resting
  state data. This makes it difficult/impossible to separate resting state
  activity from task-based activity.
* The dataset is actually small.  There are only 102 samples. But the data
  is also big -- there are 49 columns of data in 'demographic.txt' in addition
  to the fMRI which is 3 (tests) * (64 * 64 * 36) (spatial) * 137 (temporal)
  = 20201472 or about 10^7 'features'.  *Of course, we hope to extract only a
  few meaningful features from all of those*.


## References
[1] http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3358772/

[2] http://www.ncbi.nlm.nih.gov/pubmed/21193174

[3] This data was obtained from the OpenfMRI database. Its accession number is ds000115

## Acknowledgments
I would like to thank the investigators for making the data publicly available:

* Barch DM
* Repovs G
* Csernansky JG
