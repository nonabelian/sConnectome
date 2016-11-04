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
from src.process_data.demographic_data import DemographicData


if __name__ == '__main__':
    filename = 'data/ds115_metadata/demographics.txt'

    dd = DemographicData(filename, 'condit')
    dd.process()
    dd.make_categoricals()

    mapping = {'SCZ': 'SCZ', 'SCZ-SIB': 'CON', 'CON': 'CON', 'CON-SIB': 'CON'}
    maps = [None, mapping]

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

