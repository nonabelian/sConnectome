import os
from collections import defaultdict
import cPickle as pickle
import multiprocessing as mp

import numpy as np
import networkx as nx
from nilearn import image
from nilearn import input_data
from sklearn.externals.joblib import Memory


class GraphExperimentData(object):
    ''' Container class for GraphData -- one GraphData per subject
        INPUT: models, fMRIExperimentData, atlas, map, list
                models -- to predict time-averaged covariance between regions
                fMRIExperiment -- container for all experiment data
                atlas -- chosen brain atlas regions
                map -- atlas corresponding map
                list -- properties of interest in the graph -- e.g. efficiency
    '''

    def __init__(self, models, fmri_data, atlas, maps, properties=None):
        self.models = models
        self.fmri_data = fmri_data
        self.atlas = atlas
        self.maps = maps
        self.properties = properties

        self.graph_data = self.load_subject_graphs()

        self.working_directory = self._set_wd()


    def _set_wd(self):
        return os.path.join(self.fmri_data.working_directory, 'graphs')


    def load_subject_graphs(self):
        ''' Loads a graph for each subject data in fMRIExperimentData and
            stores in a list.
            Returns the list of graphs -- one per subject, or averaged over
            tasks.
            INPUT: None
            OUTPUT: list
        '''
        graphs = {}

        for subject_data in self.fmri_data.iter_subject_data():
            gd = GraphSubjectData(self.models, subject_data, self.atlas,
                                  self.maps, properties=self.properties)

            graphs[subject_data.name] = gd

        return graphs


    def load_graph_data(self, graph_data_file=None):

        if not graph_data_file:
            load_file = os.path.join(self.working_directory, 'graph_data.pkl')

        if not os.path.exists(load_file):
            raise ValueError("ValueError: Graph file does not exist!")

        with open(load_file) as f:
            data = pickle.load(f)

        for sub, gd in self.graph_data.iteritems():
            # Set the graph data
            gd.graph = data[sub]['graph']
            gd.graph_properties

            # Set the graph property data
            for prop in data[sub]:
                if prop == 'graph':
                    continue

                gd.graph_properties[prop] = data[sub][prop]


    def save_graph_data(self, save_directory=None):

        if save_directory:
            self.working_directory = save_directory

        data = {}

        for n, gd in self.graph_data.iteritems():
            data[n] = {}
            data[n]['graph'] = gd.graph
            data[n]['properties'] = gd.graph_properties

        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)

        save_file = os.path.join(self.working_directory, 'graph_data.pkl')

        with open(save_file, 'w') as f:
            pickle.dump(data, f)


    def iter_graph_data(self):
        for name, gd in self.graph_data.iteritems():
            yield gd


class GraphSubjectData(object):
    ''' Class to generate and encapsulate graph data for fMRI data (from
        a fMRIExperimentData class object.
        INPUT: models, fMRISubjectData, atlas, map, list
                models -- to predict time-averaged covariance between regions.
                          This is a list for possible future implementation,
                          but currently only accesses first model.
                fMRIExperiment -- container for all experiment data
                atlas -- chosen brain atlas regions
                map -- atlas corresponding map
                list -- properties of interest in the graph -- e.g. efficiency
    '''

    def __init__(self, models, fmri_data, atlas, maps, properties=None):       
        self.subject_data = fmri_data
        self.models = models
        self.atlas = atlas
        self.maps = maps
        self.graph = None
        self.norm_cov = None

        self.mem = None
        self.masker = self._set_masker(maps)

        # Quantitative graph properties
        self.graph_properties = {}
        self.properties = self.set_properties(properties)


    def _set_masker(self, maps):
        wdir = self.subject_data.working_directory
        memdir = os.path.join(wdir, 'nilearn_cache')
        self.mem = Memory(memdir)

        masker = input_data.NiftiMapsMasker(
               self.maps, resampling_target="maps", detrend=True,
               low_pass=None, high_pass=0.01, t_r=2.5, standardize=True,
               memory=self.mem, memory_level=1, verbose=2)
        masker.fit()

        return masker


    def set_properties(self, properties):
        if not properties:
            return ['average_node_connectivity', \
                    'degree_centrality', \
                    'betweenness_centrality', \
#                    'eigenvector_centrality', \
                    'current_flow_closeness_centrality', \
                    'current_flow_betweenness_centrality', \
                    'average_shortest_path_length', \
                    'diameter', \
                    'radius', \
                    'eccentricity']
#                    'efficency', \
#                    'global_efficiency']

        return properties


    def graph_to_edge_dict(self, graph):
        ''' Utility funciton to create an 'edge dict'.
            INPUT: nx.Graph
            OUTPUT: defaultdict: tuple -> float (weight)
        '''
        edge_dict = defaultdict(float)

        for n1, n2w in graph.iteritems():
            for n2, w in n2w.iteritems():
                if (n2, n1) in edge_dict.keys():
                    continue

                edge_dict[(n1, n2)] = w['weight']

        return edge_dict


    def collect_ts_confounds(self):
        ''' Gathers (in lists) the time series task data, one task per entry,
            and task data confounds.
            INPUT: None
            OUTPUT: list, list
        '''
        ts_data = []
        confounds_data = []
        for task_data in self.subject_data.iter_task_data():
            _, task_mni_data = task_data.filtered_mni_image
            _, confounds = task_data.confounds
            ts_data.append(task_mni_data)
            confounds_data.append(confounds)

        return ts_data, confounds_data


    def calculate_graph_properties(self):
        for p in self.properties:
            self.graph_properties[p] = getattr(nx.algorithms, p)(self.graph)


def generate_graphs_parallel(ged):
    ''' Calculates inter-region correlations by masking the atlas with
        provided precomputed and computed high variance confounds,
        fitting the model(s), and extracting the appropriate coefficients/
        precisions (also normalizes this matrix).
        INPUT: GraphExperimentData
        OUTPUT: GraphExperimentData
    '''

    if os.path.exists(ged.working_directory):
        print "Graph data exists! Skipping..."
        return ged

    pool = mp.Pool(processes=mp.cpu_count())
    multi_proc = [(name, pool.apply_async(generate_graph_threaded, (gd,))) for \
                  name, gd in ged.graph_data.iteritems()]

    new_ged = GraphExperimentData(ged.models, ged.fmri_data, ged.atlas,
                                  ged.maps, properties=ged.properties)
    new_ged.graph_data = {}

    for name, proc in multi_proc:
        new_gd = proc.get()
        
        new_ged.graph_data[name] = new_gd

    return new_ged

    
def generate_graph_threaded(gd):
    ''' Calculates inter-region correlations by masking the atlas with
        provided precomputed and computed high variance confounds,
        fitting the model(s), and extracting the appropriate coefficients/
        precisions (also normalizes this matrix).
        TODO: Actually make this threaded.
        INPUT: GraphData
        OUTPUT: GraphData
    '''
    ts_data, confounds_data = gd.collect_ts_confounds()

    region_time_series = []
    for img, c in zip(ts_data, confounds_data):
        # Computing some confounds -- takes 4D NifTi file as argument
        hv_confounds = gd.mem.cache(image.high_variance_confounds)(img)

        # Extract region
        region_ts = gd.masker.transform(img, confounds=[hv_confounds, c])

        # List of regional time series data
        region_time_series.append(region_ts) 

    m = gd.models[0]
    m.fit(region_time_series)

    max_abs = np.max(np.fabs(m.precisions_[..., 0]))
    gd.norm_cov = m.precisions_[..., 0] / max_abs

    gd.graph = nx.Graph(-gd.norm_cov)

    return gd
