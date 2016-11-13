import os

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from src.process_data.demographic_data import DemographicData
from src.models.graph_model import GraphModel
from src.models.utils import load_graphs
from src.models.utils import featurize


if __name__ == '__main__':

    graph_directory = os.path.join('data', 'graphs')
    demographic_data = os.path.join('data', 'ds115_metadata',
                                    'demographics.txt')
    model_directory = os.path.join('data', 'models')
    model_file = 'graph_model.pkl'
    dataframe_directory = os.path.join('data', 'dataframes')
    dataframe_file = 'graph_dataframe.pkl'

    names, graphs = load_graphs(graph_directory)

    df_graphs = featurize(graphs)

    # Set the column to merge on:
    df_graphs['subcode'] = names

    dd = DemographicData(demographic_data, 'condit')

    mapping1 = None
    mapping2 = {'SCZ': 'SCZ', 'SCZ-SIB': 'rSCZ', 'CON': 'CON', 'CON-SIB': 'CON'}
    mapping3 = {'SCZ': 'SCZ', 'rSCZ': 'SCZ', 'CON': 'CON', 'CON-SIB': 'CON'}

    mappings = [mapping1, mapping2, mapping3]

    for mapping in mappings:
        dd.group(mapping)

        # Merge on 'subcode' and get rid of it
        df_labels = dd.df[['subcode', 'condit']].copy()
        df = pd.merge(df_graphs, df_labels, how='inner').copy()
        del df['subcode']

        rfc = RandomForestClassifier(n_estimators=100, class_weight='balanced')
        gbc = GradientBoostingClassifier(n_estimators=200)

        gbc_gm = GraphModel(gbc, df)
        rfc_gm = GraphModel(rfc, df)
        
        gbc_gm.run()
        rfc_gm.run()

        print gbc_gm.report()
        print rfc_gm.report()

    # Pickle the final Gradient Boosting model:
    gbc_gm.save_model(model_directory, model_file)

    # Pickle the DataFrame
    gbc_gm.save_data(dataframe_directory, dataframe_file)

    # Plot
    save_image = os.path.join('images', 'models',
                              'graph_importances_readme.png')
    gbc_gm.plot_feature_importances(save_image=save_image)

#####################
# End of File
#####################
