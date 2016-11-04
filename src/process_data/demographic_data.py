import pandas as pd
import numpy as np

class DemographicData(object):
    def __init__(self, filename, target, columns=None, sep=None):
        self.filename = filename
        self.columns = self._set_columns(columns)
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

    def _set_sep(self, sep):
        if not sep:
            return '\t'

        return sep


    def _to_numeric(self, column):
        return self.df[column].apply(pd.to_numeric, errors='coerce')


    def set_target(self, target):
        self.target = target


    def load_demographic_data(self, filename):
        ''' Read in the in demographic data (tab separated) in 'filename'
            INPUT: string
            OUTPUT: pandas DataFrame
        '''

        return pd.read_csv(filename, sep=self.sep)


    def process(self):
        for c in self.columns:
            self.df[c] = self.df[c].apply(pd.to_numeric, errors='coerce')

        self.df.drop('subcode', inplace=True, axis=1)


    def make_categoricals(self):
        ''' Takes in the demographics data and turns 'race' and 'gender' into
            dummy variables
            INPUT: pandas DataFrame
            OUTPUT: pandas DataFrame
        '''
        columns = ['race', 'gender']
        values = ['WHITE', 'MALE']

        for c, v in zip(columns, values):
            self.df[c] = self.df[c].apply(lambda x: 1 if x == v else 0)

    def group(self, mapping):
        for k, v in mapping.iteritems():
            self.df[self.target] = self.df[self.target].apply(lambda x: \
                                                              v if x == k \
                                                              else x)

    def get_XY(self):
        data = self.df.copy()
        Y = data.pop(self.target).values
        X = data.values

        return X, Y

