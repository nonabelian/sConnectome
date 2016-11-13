import os
import cPickle as pickle

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report

from utils import get_fi_sorted

class GraphModel(object):
    ''' Class to perform machine learning on data formed by merging known
        labels and GraphData.
        INPUT: sklearn classifier, pandas dataframe, string
    '''

    def __init__(self, clf, df, target_name='condit'):
        self.clf = clf
        self.df = df
        self.target = target_name
        self.X = None
        self.Y = None
        self.X_train = None
        self.X_test = None
        self.Y_train = None
        self.Y_test = None
        self.columns = None


    def run(self):
        tmpdf = self.df.copy()

        self.Y = tmpdf.pop(self.target).values
        self.X = tmpdf.values

        self.columns = tmpdf.columns.tolist()

        X_train, X_test, Y_train, Y_test = self.get_XY_split()

        self.X_train = X_train
        self.X_test = X_test
        self.Y_train = Y_train
        self.Y_test = Y_test

        self.clf.fit(X_train, Y_train)


    def report(self):
        score = self.clf.score(self.X_test, self.Y_test)

        predictions = self.clf.predict(self.X_test)
        cr = classification_report(self.Y_test, predictions)

        output = '='*40 + '\n'
        output += self.clf.__class__.__name__ + '\n'
        output += '='*40 + '\n'
        output += 'Score: ' + str(score) + '\n'
        output += cr + '\n'
 
        feature_importances = get_fi_sorted(self.columns,
                                            self.clf.feature_importances_)

        output += 'Top 5 Features:' + '\n'
        for fi in feature_importances[:5]:
            output += str(fi) + '\n'

        return output       


    def get_XY_split(self):
        tmpdf = self.df.copy()

        Y = tmpdf.pop(self.target).values
        X = tmpdf.values

        return train_test_split(X, Y, test_size=0.2, random_state=2,
                                stratify=Y)


    def save_model(self, directory, filename):
        print 'Saving Model... ',
        if not os.path.exists(directory):
            os.makedirs(directory)

        save_file = os.path.join(directory, filename)

        print save_file + ': ',

        with open(save_file, 'w') as f:
            pickle.dump(self.clf, f)

        print 'Done'

    def save_data(self, directory, filename):
        print 'Saving Data... ',

        if not os.path.exists(directory):
            os.makedirs(directory)

        save_file = os.path.join(directory, filename)

        print save_file + ': ',

        with open(save_file, 'w') as f:
            pickle.dump({'data': self.X,
                         'target': self.Y,
                         'columns': self.columns},
                        f)
        print 'Done'


    def plot_feature_importances(self, save_image=None, show_plot=False):
        
        col_fi = get_fi_sorted(self.df.columns.tolist(),
                               self.clf.feature_importances_)

        fig = plt.figure(figsize=(20, 10))
        ax = fig.add_subplot(111)

        names = [name for name, score in col_fi]
        scores = [score for name, score in col_fi]
        ax.bar(range(len(names)), scores, align='center')
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=-45)
        ax.set_xlabel('Feature Names')
        ax.set_ylabel('Feature Importance')
        ax.set_title('Model feature_importance_')
        ax.set_xlim([-1, 5])

        plt.tight_layout()

        if save_image:
            plt.savefig(save_image)

        if show_plot:
            plt.show()
