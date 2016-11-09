import numpy as np


def get_fi_sorted(names, importances):
    return np.array(sorted(zip(names, importances), key=lambda x: x[1])[::-1])

