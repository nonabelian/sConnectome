import os
import cPickle as pickle

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

import src.models.metadata_model as mm
from src.models.utils import get_fi_sorted
from src.process_data.demographic_data import DemographicData


def iterate_models(dd, maps=None):
    for m in maps:
        dd.group(m)

        print '=' * 50
        print 'Grouping: ', m
        print '=' * 50

        X, Y = dd.get_XY()

        le = LabelEncoder()
        Y = le.fit_transform(Y)

        X = mm.impute_mean(X)

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,
                                                            random_state=1,
                                                            stratify=Y)

        lr = LogisticRegression(class_weight='balanced')
        svc = SVC(class_weight='balanced')
        knn = KNeighborsClassifier()
        rfc = RandomForestClassifier(n_estimators=100, class_weight='balanced')
        gbc = GradientBoostingClassifier(n_estimators=200)

        models = [lr, svc, knn, gbc, rfc]

        for model in models:
            print '-' * 40
            print model.__class__.__name__
            model.fit(X_train, Y_train)
            predictions = model.predict(X_test)
            print "Score: ", model.score(X_test, Y_test)
            print classification_report(Y_test, predictions)
    


if __name__ == '__main__':
    filename = os.path.join('data', 'ds115_metadata', 'demographics.txt')
    model_directory = os.path.join('data', 'models')
    model_file = 'meta_model.pkl'
    dataframe_directory = os.path.join('data', 'dataframes')
    dataframe_file = 'meta_dataframe.pkl'

    dd = DemographicData(filename, 'condit')
    dd.process()
    dd.make_categoricals()

    # Loop through some models for some different mappings and see the results
    mapping = {'SCZ': 'SCZ', 'SCZ-SIB': 'CON', 'CON': 'CON', 'CON-SIB': 'CON'}
    maps = [None, mapping]
    iterate_models(dd, maps=maps)


    # Look at the preformance of the tests at identifying schizophrenic people
    dd.group(mapping)

    X, Y = dd.get_XY()
    le = LabelEncoder()
    Y = le.fit_transform(Y)
    X = mm.impute_mean(X)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,
                                                        random_state=1,
                                                        stratify=Y)

    gbc = GradientBoostingClassifier(n_estimators=200)

    gbc.fit(X_train, Y_train)

    print '-' * 40
    print gbc.__class__.__name__
    gbc.fit(X_train, Y_train)
    predictions = gbc.predict(X_test)
    print "Score: ", gbc.score(X_test, Y_test)
    print classification_report(Y_test, predictions)

    df = dd.df.copy()
    del df['condit']

    feature_importances = get_fi_sorted(df.columns.tolist(),
                                        gbc.feature_importances_)

    print 'Top 5 Features:'
    for fi in feature_importances[:5]:
        print fi

    # Pickle the model:
    print 'Saving Model... ',
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)

    save_file = os.path.join(model_directory, model_file)

    with open(save_file, 'w') as f:
        pickle.dump(gbc, f)

    print 'Done'

    # Pickle the DataFrame

    print 'Saving Data... ',

    if not os.path.exists(dataframe_directory):
        os.makedirs(dataframe_directory)

    save_file = os.path.join(dataframe_directory, dataframe_file)

    with open(save_file, 'w') as f:
        pickle.dump({'data': X,
                     'target': Y,
                     'columns': df.columns.tolist()},
                    f)
    print 'Done'
