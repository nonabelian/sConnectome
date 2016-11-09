import os
import cPickle as pickle

import pandas as pd
import numpy as np
import scipy.stats as scs
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report

from src.process_data.demographic_data import DemographicData
from src.models.utils import get_fi_sorted


def load_graphs(d):
    files = os.listdir(d)

    names = []
    graphs = []

    for filename in files:
        name = filename.split(os.sep)[-1][0:6]

        ofilename = os.path.join(d, filename)

        with open(ofilename) as f:
            graphs.append(pickle.load(f))
            names.append(name)

    return names, graphs


def featurize(graphs):

    dfs = []

    for graph in graphs:
        df = pd.DataFrame()
        for prop, feature in graph['properties'].iteritems():

            # If dictionary, create all columns
            if isinstance(feature, dict):
                for k, v in feature.iteritems():
                    colname = prop + str(k)
                    df[colname] = [v]
            elif isinstance(feature, float) or isinstance(feature, int):
                df[prop] = [feature]
            else:
                print 'Unexpected column type: ', feature

        dfs.append(df.copy())

    full_df = pd.concat(dfs)

    return full_df


if __name__ == '__main__':

    graph_directory = 'data/graphs/'
    demographic_data = 'data/ds115_metadata/demographics.txt'
    model_directory = 'data/models/'
    model_file = 'graph_model.pkl'
    dataframe_directory = 'data/dataframes/'
    dataframe_file = 'graph_dataframe.pkl'

    names, graphs = load_graphs(graph_directory)

    df_graphs = featurize(graphs)
    df_graphs['subcode'] = names

    dd = DemographicData(demographic_data, 'condit')

    df_dd = dd.df

    df_labels = df_dd[['subcode', 'condit']].copy()

    df = pd.merge(df_graphs, df_labels, how='inner')

    del df['subcode']

    Y = df.pop('condit').values
    X = df.values

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,
                                                        random_state=1,
                                                        stratify=Y)

    rfc = RandomForestClassifier(n_estimators=100, class_weight='balanced')
    gbc = GradientBoostingClassifier(n_estimators=200)

    gbc.fit(X_train, Y_train)
    rfc.fit(X_train, Y_train)

    print 'GBC Score:', gbc.score(X_test, Y_test)
    print 'RFC Score:', rfc.score(X_test, Y_test)

    predictions = gbc.predict(X_test)
    print classification_report(Y_test, predictions)

    feature_importances = get_fi_sorted(df.columns.tolist(),
                                        gbc.feature_importances_)

    print 'Top 5 Features:'
    for fi in feature_importances[:5]:
        print fi

    # Pickle the model:
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)

    save_file = os.path.join(model_directory, model_file)

    with open(save_file, 'w') as f:
        pickle.dump(gbc, f)

    # Pickle the DataFrame
    if not os.path.exists(dataframe_directory):
        os.makedirs(dataframe_directory)

    save_file = os.path.join(dataframe_directory, dataframe_file)

    with open(save_file, 'w') as f:
        pickle.dump({'data': X,
                     'target': Y,
                     'columns': df.columns.tolist()},
                    f)


