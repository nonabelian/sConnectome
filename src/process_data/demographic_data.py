import pandas as pd
import numpy as np

class DemographicData(object):
    ''' Container class for the 'demographics.txt' meta data provided in the
        dataset -- see the project documentation.  Provieds some step-wise
        processing functions.
    '''


    def __init__(self, filename, target, sep=None, columns=None,
                 categoricals=None, drop_columns=None):
        self.filename = filename
        self.columns = self._set_columns(columns)
        self.categoricals = self._set_categoricals(categoricals)
        self.drop_columns = self._set_drop_columns(drop_columns)
        self.sep = self._set_sep(sep)
        self.target=target

        self.df = self.load_demographic_data(filename)


    def _set_columns(self, columns):
        if not columns:
            return ['sans25', 'd4prime', 'TRAILB', 'WCSTPSVE', \
                            'WAIS_VOCAB_SCALED', 'WAIS_MATRICS_SCALE', \
                            'LOGIALMEMORY_SCALE', 'FAMILYPICT_SCALE', \
                            'LNS_SCALE', 'SST_SCALE', 'z_iq_4grp', \
                            'z_em_4grp', 'fyrschool']

        return columns


    def _set_categoricals(self, columns):
        if not columns:
            return {'race': 'WHITE', 'gender': 'MALE'}

        return columns


    def _set_drop_columns(self, columns):
        if not columns:
            return ['subcode']

        return columns


    def _set_sep(self, sep):
        if not sep:
            return '\t'

        return sep


    def set_target(self, target):
        self.target = target


    def load_demographic_data(self, filename):
        ''' Read in the in demographic data (tab separated) in 'filename'
            INPUT: string
            OUTPUT: pandas DataFrame
        '''

        return pd.read_csv(filename, sep=self.sep)


    def process(self):
        ''' Process step purposefully not automatic, in case it is necessary
            to have access to the unprocessed data.  Inplace operation
            INPUT: None
            OUTPUT: None
        '''

        # Columns to transform (coerce) to numeric
        for c in self.columns:
            self.df[c] = self.df[c].apply(pd.to_numeric, errors='coerce')

        for c in self.drop_columns:
            self.df.drop(c, inplace=True, axis=1)


    def make_categoricals(self):
        ''' Process step purposefully not automatic.  Transforms specified
            columns into dummy variables.  Inplace.
            INPUT: None
            OUTPUT: None
        '''

        for c, v in self.categoricals.iteritems():
#            self.df = pd.get_dummies(self.df, columns=[c])
            self.df[c] = self.df[c].apply(lambda x: 1 if x == v else 0)


    def group(self, mapping):
        ''' Applies a class relabeling map provided by 'mapping', for example
            to change {'SCZ', 'SCZ-SIB', 'CON', 'CON-SIB'} into
            {'SCZ', 'CON'}.  Inplace.
            INPUT: dictionary
            OUTPUT: None
        '''
        if not mapping:
            return

        for k, v in mapping.iteritems():
            self.df[self.target] = self.df[self.target].apply(lambda x: \
                                                              v if x == k \
                                                              else x)

    def get_XY(self):
        ''' Returns numpy feature matrix and target vector for ML processing.
            INPUT: None
            OUTPUT: np.array, np.array
        '''

        data = self.df.copy()
        Y = data.pop(self.target).values
        X = data.values

        return X, Y

