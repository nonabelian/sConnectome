import os

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier

from src.models.metadata_model import MetaModel
from src.models.utils import get_fi_sorted
from src.process_data.demographic_data import DemographicData


if __name__ == '__main__':
    filename = os.path.join('data', 'ds115_metadata', 'demographics.txt')
    model_directory = os.path.join('data', 'models')
    model_file = 'meta_model.pkl'
    dataframe_directory = os.path.join('data', 'dataframes')
    dataframe_file = 'meta_dataframe.pkl'

    dd = DemographicData(filename, 'condit')
    dd.process()
    dd.make_categoricals()

    df = dd.df.copy()
    df.pop('condit')
    cols = df.columns.tolist()

    # Loop through some models for some different mappings and see the results
    mapping = {'SCZ': 'SCZ', 'SCZ-SIB': 'CON', 'CON': 'CON', 'CON-SIB': 'CON'}
    maps = [None, mapping]

    rfc = RandomForestClassifier(n_estimators=100, class_weight='balanced')
    gbc = GradientBoostingClassifier(n_estimators=200)

    for m in maps:
        dd.group(m)

        print '=' * 50
        print 'Grouping: ', m
        print '=' * 50

        X, Y = dd.get_XY()

        rfc_mm = MetaModel(rfc, X, Y, cols)
        gbc_mm = MetaModel(gbc, X, Y, cols)

        models = [rfc_mm, gbc_mm]

        for model in models:
            model.run()
            print model.report()

    # Pickle the model:
    gbc_mm.save_model(model_directory, model_file)

    # Pickle the DataFrame
    gbc_mm.save_data(dataframe_directory, dataframe_file)
