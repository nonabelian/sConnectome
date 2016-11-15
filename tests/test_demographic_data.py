import os

import nose.tools as n
import pandas as pd

# Import local context
from .context import src
from src.process_data import demographic_data as dd
from get_message import get_message

def test_DemographicData():
    filename = os.path.join('tests', 'data', 'test_dd.txt')
    target = 'target'
    columns = ['b', 'c']
    sep = '\t'
    test_dd = dd.DemographicData(filename, target, columns=columns, sep=sep)
    
    # Instantiation:
    exp = columns
    act = test_dd.columns
    n.assert_equal(exp, act, msg=get_message("Object columns", exp, act))

    exp = sep
    act = test_dd.sep
    n.assert_equal(exp, act, msg=get_message("Separation", exp, act))

    exp = filename
    act = test_dd.filename
    n.assert_equal(exp, act, msg=get_message("Filename", exp, act))

    exp = target
    act = test_dd.target
    n.assert_equal(exp, act, msg=get_message("Target", exp, act))

    exp = pd.read_csv(filename, sep=sep).values.tolist()
    act = test_dd.df.values.tolist()
    n.assert_equal(exp, act, msg=get_message("Pandas DataFrame", exp, act))


def test_load_demographic_data():
    filename = os.path.join('tests', 'data', 'test_dd.txt')
    target = 'target'
    columns = ['b', 'c']
    sep = '\t'
    test_dd = dd.DemographicData(filename, target, columns=columns, sep=sep)

def test_process():
    filename = os.path.join('tests', 'data', 'test_dd.txt')
    target = 'target'
    columns = ['b', 'c']
    sep = '\t'
    test_dd = dd.DemographicData(filename, target, columns=columns, sep=sep)

def test_make_categoricals():
    filename = os.path.join('tests', 'data', 'test_dd.txt')
    target = 'target'
    columns = ['b', 'c']
    sep = '\t'
    test_dd = dd.DemographicData(filename, target, columns=columns, sep=sep)

def test_group():
    ''' Grouping the prediction 'target'
    '''
    filename = os.path.join('tests', 'data', 'test_dd.txt')
    target = 'target'
    columns = ['b', 'c']
    sep = '\t'
    test_dd = dd.DemographicData(filename, target, columns=columns, sep=sep)

def test_get_XY():
    ''' Retrieve X, Y data matrices
    '''
    filename = os.path.join('tests', 'data', 'test_dd.txt')
    target = 'target'
    columns = ['b', 'c']
    sep = '\t'
    test_dd = dd.DemographicData(filename, target, columns=columns, sep=sep)

