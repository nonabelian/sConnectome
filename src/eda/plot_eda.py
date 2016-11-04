import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix

# Local package imports
from ..process_data import demographic_data as dd

def plot_test_histograms(df, target, label, columns=None, save_image=None):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    if not columns:
        columns = df.columns.tolist()
        columns.remove('condit')
        columns.remove('gender')
        columns.remove('race')
        columns.remove('age')
        columns.remove('yrschool')
        columns.remove('fyrschool')
        columns.remove('myrschool')
        columns.remove('parent_yrsschool')
        columns.remove('nback0_nont')
        columns.remove('nback0_targ')
        columns.remove('nback1_nont')
        columns.remove('nback1_targ')
        columns.remove('nback2_nont')
        columns.remove('nback2_targ')
        columns.remove('nback0_nont_medrt')
        columns.remove('nback0_targ_medrt')
        columns.remove('nback1_nont_medrt')
        columns.remove('nback1_targ_medrt')
        columns.remove('nback2_nont_medrt')
        columns.remove('nback2_targ_medrt')
    
    df[df[target] == label][columns].hist(ax=ax, alpha=0.5)

    # This is a bug
    # plt.tight_layout()

    if save_image:
        plt.savefig(save_image)

def plot_scatter_matrix(df, save_image=None):
    fig = plt.figure(figsize=(60, 60))
    ax = fig.add_subplot(111)
    smplot = scatter_matrix(df, ax=ax)

    if save_image:
        plt.savefig(save_image)
