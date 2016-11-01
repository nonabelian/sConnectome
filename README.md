# Connectome for Schizophrenic and Healthy Individuals

We investigate an fMRI dataset comparing healthy individuals to individuals
diagnosed with schizophrenia. The main motivation is to find functioning
neurological processes that indicate illness or susceptibility to illness.

The current belief is that connectivity between functional components is
significantly different in individuals with schizophrenia.

We find that ...

![High Resolution fMRI](images/highres_cutplane.png)

## Results



## Methods

## Data

The data are located at https://openfmri.org/dataset/ds000115/ [3].

The AWS hosted files consist of raw fMRI images for 102 patients in addition
to many preprocessed derivatives.  The data comes with an interesting
'demographics.txt' file, providing additional data for most of the subjects.

The data present two distinct challenges:

* Unfortunately the authors of the dataset have not also published the resting
  state data. This makes it difficult/impossible to separate resting state
  activity from task-based activity.
* The dataset is actually small.  There are only 102 samples.

## 

## Citations
[1] http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3358772/

[2] http://www.ncbi.nlm.nih.gov/pubmed/21193174

[3] This data was obtained from the OpenfMRI database. Its accession number is ds000115

## Acknowledgments
I would like to thank the investigators for making the data publicly available:

* Barch DM
* Repovs G
* Csernansky JG
