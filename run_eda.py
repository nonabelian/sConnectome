import pandas as pd

from src.process_data.demographic_data import DemographicData
import src.eda.plot_eda as pe


if __name__ == '__main__':

    filename='data/ds115_metadata/demographics.txt'

    dd = DemographicData(filename, 'condit')

    # Make the columns nice!
    dd.process()

    obvious_cols = ['condit', 'gender', 'race','age', 'yrschool',\
                    'fyrschool', 'myrschool', 'parent_yrsschool']

    df = dd.df.copy()

    df_oc = df[obvious_cols]

    print '=' * 50
    print 'Summary EDA'
    print '=' * 50

    print '-' * 50
    print 'Value Counts'
    print '-' * 50
    print df_oc.condit.value_counts()
    print df_oc.gender.value_counts()
    print df_oc.race.value_counts()

    print '-' * 50
    print 'Obvious Columns'
    print '-' * 50
    print df_oc[['age', 'yrschool','fyrschool', 'myrschool', \
                 'parent_yrsschool']].describe()
    
    print '-' * 50
    print 'Group bys'
    print '-' * 50
    print df_oc.groupby(['condit', 'race', 'gender']).count()
    print df_oc.groupby(['condit', 'race', 'gender']).mean()

    print '-' * 50
    print 'z values -- head'
    print '-' * 50
    print df[['condit','z_iq_4grp','z_wm_4grp','z_em_4grp','z_ra_4grp',\
                'z_pos_4grp','z_neg_4grp','z_dis_4grp']].head()
    print '-' * 50
    print 'Correlation matrix'
    print '-' * 50
    print df.corr()

    print '-' * 50
    print 'NaNs -- A surprisingly large number for such a small dataset'
    print '-' * 50
    df[df.isnull().any(axis=1)]

    print '-' * 50
    print 'Plotting histograms'
    print '-' * 50
    pe.plot_test_histograms(df, 'condit', 'SCZ', columns=None,
                           save_image='images/eda/SCZ-test_histograms.png')
    pe.plot_test_histograms(df, 'condit', 'SCZ-SIB', columns=None,
                           save_image='images/eda/SCZ-SIB-test_histograms.png')
    pe.plot_test_histograms(df, 'condit', 'CON', columns=None,
                           save_image='images/eda/CON-test_histograms.png')
    pe.plot_test_histograms(df, 'condit', 'CON-SIB', columns=None,
                           save_image='images/eda/CON-SIB-test_histograms.png')

    print '-' * 50
    print 'Plotting scatter matrix -- this will take a while...'
    print '-' * 50
    pe.plot_scatter_matrix(df, save_image='images/eda/scatter_matrix.png')
    

    print '=' * 50
    print 'End Summary EDA'
    print '=' * 50
