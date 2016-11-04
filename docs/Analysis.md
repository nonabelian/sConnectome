# Anaysis

I outline some of the techniques used to perform the analysis.  For more detail,
have a look at the code!
The packages and programs (requirements) used for the analysis are listed in
the README.md. These are required to redo the analysis.

### Metadata Analysis

First I loaded the data into Pandas and used mean imputation to fill in NaN
fields. I have yet to implement KNN method to fill in values and I still need
to cross validate.

I used a gradient boosting classifier from Scikit-learn on a stratified
train-test split to classify and predict.  I considered two situations:

1. Binary classification: 'SCZ' versus not 'SCZ' labeled data
2. Multiclass: Four classes {'SCZ', 'SCZ-SIB', 'CON', 'CON-SIB'}.


### fMRI Analysis

#### Preprocessing

I have not done much more preprocessing than was implemented in the original
FSL pipeline -- FEAT, FLIRT, FNIRT. I used the affine and warp transformations
to transform the data into MNI space.

I use an MSDL atlas to segment the brain into regions.
I then use graph lasso and Nilearn's GraphSparseCovarianceCV to calculate
covariance and sparse inverse covarianc, as methods to examine the functional
connectome.  This results in a graph network for eash subject, aggregated
over all tasks.

#### Modeling

I add the following graph features to the labeled dataset:

* Average node connectivity
* Betweenness centrality
* Eigenvector centrality
* Current flow closeness
* Current flow betweenness
* Average shortest path length
* Diameter
* Efficiency and global efficiency

