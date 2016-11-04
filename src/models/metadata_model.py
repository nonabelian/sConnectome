import pandas as pd
import numpy as np

from sklearn.preprocessing import Imputer


def impute_KNN(X):
    pass

def impute_mean(X):

    imp = Imputer()
    return imp.fit_transform(X)
