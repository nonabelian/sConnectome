import os
from collections import defaultdict

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

        self.subject_graphs = self.load_subject_graphs()

    def load_subject_graphs(self):
        ''' Loads a graph for each subject data in fMRIExperimentData and
            stores in a list.
            Returns the list of graphs -- one per subject, or averaged over
            tasks.
            INPUT: None
            OUTPUT: list
        '''
        graphs = []

        for subject_data in self.fmri_data.iter_subject_data():
            gd = GraphSubjectData(self.models, subject_data, self.atlas,
                                  self.maps, properties=self.properties)

            graphs.append(gd)

        return graphs

    def generate_subject_graphs(self):
        ''' Generate graphs sequentially
            INPUT: None
            OUTPUT: None
        '''

        if not self.subject_graphs:
            raise ValueError("Error: Must load in GraphSubjectData first!")

        for sg in self.subject_graphs:
            sg.generate_graph()

    def generate_subject_graphs_ll(self):
        ''' Generate graphs in parallel
            INPUT:
            OUTPUT:
        '''
        pass


class GraphSubjectData(object):
    ''' Class to generate and encapsulate graph data for fMRI data (from
        a fMRIExperimentData class object.
        INPUT: models, fMRISubjectData, atlas, map, list
                models -- to predict time-averaged covariance between regions
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
        self.subj_graph_props = defaultdict(list)
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
            return ['average_node_connectivity', 'betweenness_centrality',\
                    'eigenvector_centrality', 'current_flow_closeness',\
                    'currnet_flow_betweenness', 'average_shortest_path_length',\
                    'diameter', 'efficency', 'global_efficiency']

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


    def generate_graph(self):
        ''' Calculates inter-region correlations by masking the atlas with
            provided precomputed and computed high variance confounds,
            fitting the model(s), and extracting the appropriate coefficients/
            precisions (also normalizes this matrix).
            INPUT: None
            OUTPUT: None
        '''
        ts_data, confounds_data = self.collect_ts_confounds()

        region_time_series = []
        for img, c in zip(ts_data, confounds_data):
            # Computing some confounds -- takes 4D NifTi file as argument
            hv_confounds = self.mem.cache(image.high_variance_confounds)(img)

            # Extract region
            region_ts = self.masker.transform(img, confounds=[hv_confounds, c])

            # List of regional time series data
            region_time_series.append(region_ts) 

#        for m in self.models:
#            m.fit(region_time_series)

        m = self.models[0]
        m.fit(region_time_series)

        max_abs = np.max(np.fabs(m.precisions_[..., 0]))
        self.norm_cov = m.precisions_[..., 0] / max_abs

        self.graph = nx.Graph(-self.norm_cov)

