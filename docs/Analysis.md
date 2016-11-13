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
train-test split to classify and predict.  I considered a few situations:

1. Binary classification: {'SCZ', 'CON'} labeled data
2. Multiclass: Three classes {'SCZ', 'SCZ-SIB', 'CON', 'CON'}.
3. Multiclass: Four classes {'SCZ', 'SCZ-SIB', 'CON', 'CON-SIB'}.

The model performs quite well, >95% on the binary classification problem,
which is not surprising.  It performs similar to random guessing on the other,
multiclass classification problems.


### fMRI Analysis

#### Preprocessing

I have not done much more preprocessing than was implemented in the original
FSL pipeline -- FEAT, FLIRT, FNIRT.
I processed the raw data using an m4.4xlarge Amazon Web Services (AWS)
computer loaded with a customized NeuroDebian public AMI (ami-bffb65a8). I
then used NiPype/FSL on filtered fMRI data, transforming it via affine and
nonlinear warping transformations into standard MNI coordinate space.

I use an MSDL atlas to segment the brain into regions.
I then use Nilearn's GraphSparseCovarianceCV to calculate
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

I then use Scikit-learn's GradientBoostingClassifier to fit a model to the
data, considering a few cases:

1. Binary classification: {'SCZ', 'CON'} labeled data
2. Multiclass: Three classes {'SCZ', 'SCZ-SIB', 'CON', 'CON'}.
3. Multiclass: Four classes {'SCZ', 'SCZ-SIB', 'CON', 'CON-SIB'}.

The model has not turned out to be predictive, yet.  I suspect that
working on fMRI preprocessing and signal/noise analysis might yield a
predictive model.  This would be very interesting!
