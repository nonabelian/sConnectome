import os
import cPickle as pickle

import pandas as pd
import numpy as np


def get_fi_sorted(names, importances):
    ''' Simple utility function for returning sorted paired importances
        and their names
        INPUT: list
        OUTPUT: np.array Nx2
    '''

    return np.array(sorted(zip(names, importances), key=lambda x: x[1])[::-1])


def load_graphs(d):
    ''' Takes the pickled graphs directory and returns a list of subject
        ids and their corresponding network graph data
        INPUT: string
        OUTPUT: list, list
    '''
    files = os.listdir(d)

    names = []
    graphs = []

    for filename in files:
        # Pull off the subject id: always 'subNNN' + '_....pkl'
        name = filename.split(os.sep)[-1][0:6]

        ofilename = os.path.join(d, filename)

        with open(ofilename) as f:
            graphs.append(pickle.load(f))
            names.append(name)

    return names, graphs


def featurize(graphs):
    ''' Takes a list of graph data of the form
        [sub001_graph, sub002_graph, ...] where
        graph = {'graph': networkx Graph,
                 'norm_cov': numpy matrix,
                 'properties': {'degree_centrality': {N1:#, N2:#...},
                                'diameter': {N1: #, N2#},
                                'average_node_connecivity': #,
                                ...
                                }
                }
        Returns a pandas DataFrame of the form:

                  'degree_centralityN1' 'degree_centralityN2' ...
        'sub001'           #                      #           ...
            .              .                      .           ...
            .              .                      .           ...

        INPUT: list
        OUTPUT: DataFrame
    '''

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
