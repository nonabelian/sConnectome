import os
import multiprocessing as mp
import threading

import numpy as np
import nibabel as nib
from nipype.interfaces import fsl


class fMRIExperimentData(object):
    ''' Class that contains FEAT fMRI data FOR ALL SUBJECTS performed by one
        particular subject, given a subject directory.
        INPUT: string, string, string, string, string, string, string
                'directories' -- list of subject directories
                'working_directory' -- needed for manipulating nii images. 
                'filtered_data' -- filtered 4D fMRI subject data
                'structure_data' -- high resolution subject structural image
                'standard_data' -- generic template.
                'affine' -- affine transformation from 'filtered' to 'structure'
                'warp' -- subsequent warp transformation from 'structure' to
                          'standard'
                'confounds' -- a '.mat' text file containing confounds
    '''

    def __init__(self, directories, working_directory='./.tmp',
                 filtered_data='filtered_func_data.nii.gz',
                 structure_data='highres.nii.gz',
                 standard_data='standard.nii.gz',
                 affine='example_func2highres.mat',
                 warp='highres2standard_warp.nii.gz',
                 confounds='confoundevs.txt'):

        self.directories = directories
        self.working_directory = working_directory
        self.filtered_data=filtered_data
        self.structure_data=structure_data
        self.standard_data=standard_data
        self.affine=affine
        self.warp=warp
        self.confounds=confounds

        self.subject_fmri_data = self.load_subject_data()


    def load_subject_data(self):
        subjects_data = []

        for d in self.directories:
            fsd = fMRISubjectData(d, self.working_directory, self.filtered_data,
                                  self.structure_data, self.standard_data,
                                  self.affine, self.warp, self.confounds)

            subjects_data.append(fsd)

        return subjects_data


    def iter_subject_data(self):
        for sd in self.subject_fmri_data:
            yield sd

#    def generate_mni_parallel(self):
#        pool = mp.Pool(processes=mp.cpu_count())
#        multi_proc = [pool.apply_async(sd.generate_mni_threaded, ()) for sd \
#                      in self.iter_subject_data()]
#
#        [proc.get() for proc in multi_proc]

def generate_mni_parallel(ec):
    pool = mp.Pool(processes=mp.cpu_count())
    multi_proc = [pool.apply_async(generate_mni_threaded, (sd,)) for sd \
                  in ec.iter_subject_data()]

    [proc.get() for proc in multi_proc]


class fMRISubjectData(object):
    ''' Class that contains FEAT fMRI data FOR ALL TASKS performed by one
        particular subject, given a subject directory.
        INPUT: string, string, string, string, string, string, string
                'directory' -- subject root directory -- 'sub001/'
                'working_directory' -- needed for manipulating nii images. 
                'filtered_data' -- filtered 4D fMRI subject data
                'structure_data' -- high resolution subject structural image
                'standard_data' -- generic template.
                'affine' -- affine transformation from 'filtered' to 'structure'
                'warp' -- subsequent warp transformation from 'structure' to
                          'standard'
                'confounds' -- a '.mat' text file containing confounds
    '''

    def __init__(self, directory, working_directory='./.tmp',
                 filtered_data='filtered_func_data.nii.gz',
                 structure_data='highres.nii.gz',
                 standard_data='standard.nii.gz',
                 affine='example_func2highres.mat',
                 warp='highres2standard_warp.nii.gz',
                 confounds='confoundevs.txt'):
        self.directory = directory
        self.working_directory = self._make_wd(working_directory)

        # Label for this data -- e.g. 'sub001', should match that found in
        # 'demographics.txt'
        self.name = self.get_subject_name(directory=directory)

        # List of fMRITaskData objects
        self.task_fmri_data = self.load_task_data(directory,
                                                     self.working_directory,
                                                     filtered_data,
                                                     structure_data,
                                                     standard_data,
                                                     affine,
                                                     warp,
                                                     confounds)

    def _make_wd(self, working_directory):
        ''' Create a working directory to run Nipype interface FSL
            command line functions -- they work with files. Returns this
            subject's MNI working directory.
            INPUT: string
            OUTPUT: string
        '''
        name = self.get_subject_name(directory=self.directory)

        if not os.path.exists(working_directory):
            os.makedirs(working_directory)

        MNI_path = os.path.join(working_directory, 'MNI')

        if not os.path.exists(MNI_path):
            os.makedirs(MNI_path)

        subj_wpath = os.path.join(MNI_path, name)

        if not os.path.exists(subj_wpath):
            os.makedirs(subj_wpath)

        return subj_wpath
        

    def get_subject_name(self, directory=None):
        ''' Parses the directory given to extract the subject 'name' or tag.
            INPUT: string
            OUTPUT: string
        '''

        if not directory:
            return self.name

        root, dirname = os.path.split(directory.strip(os.sep))
        return dirname


    def load_task_data(self, directory, working_directory, filtered_data,
                          structure_data, standard_data, affine, warp,
                          confounds):
        ''' Walks through the subject directory and creates a list of task
            fMRI measurements, stored in fMRITaskData class objects.
            Inputs are mirrored from this classes inputs.
            Returns a list of fMRITaskData class objects.
            INPUT: string, string, string, string, string, string
            OUTPUT: list
        '''

        subj_fmri = []

        for d, _, files in os.walk(directory):
            if filtered_data in files:
                fmri_task = fMRITaskData(d, working_directory,
                                         filtered_data, structure_data,
                                         standard_data, affine, warp)

                subj_fmri.append(fmri_task)
        
        return subj_fmri

    def iter_task_data(self):
        for task_data in self.task_fmri_data:
            yield task_data

#    def generate_mni_threaded(self):
#        threads = []
#
#        for td in self.iter_task_data():
#            threads.append(threading.Thread(target=td.generate_mni(),
#                                            args=()))
#
#        for th in threads:
#            th.start()
#
#        for th in threads:
#            th.join()

def generate_mni_threaded(sc):
    threads = []

    for td in sc.iter_task_data():
        threads.append(threading.Thread(target=generate_mni(), args=([td])))

    for th in threads:
        th.start()

    for th in threads:
        th.join()

class fMRITaskData(object):
    ''' Class to encapsulate FEAT preprocessed fMRI data -- given a subject
        task directory.
        INPUT: string, string, string, string, string, string, string
                'directory' -- subject root directory -- 'sub001/.../task001/'
                'working_directory' -- needed for manipulating nii images. 
                'filtered_data' -- filtered 4D fMRI subject data
                'structure_data' -- high resolution subject structural image
                'standard_data' -- generic template.
                'affine' -- affine transformation from 'filtered' to 'structure'
                'warp' -- subsequent warp transformation from 'structure' to
                          'standard'
                'confounds' -- a '.mat' text file containing confounds
    '''
    def __init__(self, directory, working_directory,
                 filtered_data='filtered_func_data.nii.gz',
                 structure_data='highres.nii.gz',
                 standard_data='standard.nii.gz',
                 affine='example_func2highres.mat',
                 warp='highres2standard_warp.nii.gz',
                 confounds='confoundevs.txt'):
        # Directory to the FEAT task data -- e.g.
        # 'sub001/model/model001/task001.feat/'
        self.directory = directory
        self.working_directory = working_directory

        # Task name.  As per the above example: 'task001'
        self.name = self.get_task_name(directory)

        # Note: the following images have the form [path, data]

        # FEAT filtered/preprocessed subject 4D fMRI data.
        self.filtered_image = self.load_nii(directory, filtered_data)

        # Highres structural MRI 3D image of patient
        self.structure_image = self.load_nii(directory, structure_data)

        # Structural template 3D image on which to fit all subjects.
        self.standard_mni_image = self.load_nii(directory, standard_data)

        self.affine = self.load_mat(directory, affine)
        self.warp = self.load_nii(directory, warp)
        self.confounds = self.load_mat(directory, confounds)

        # Warped 4D subject data -- fit to structural template.
        self.filtered_mni_image = None


    def get_task_name(self, directory):
        ''' Extracts the task 'name' or tag from the directory string
            INPUT: string
            OUTPUT: string
        '''
        if not directory:
            return self.name

        tname_dir, ext = os.path.splitext(directory.strip(os.sep))

        root, tname = os.path.split(tname_dir)
        return tname


    def load_nii(self, directory, fname):
        ''' Generic NIfTI image loader -- walks the directory structure,
            finding 'fname' and loads that file.
            Assumes the file is unique in the subdirectory tree.
            Returns a length 2 list -- [file path, NIfTI image].
            INPUT: string, string
            OUTPUT: list
        '''

        for d, _, files in os.walk(directory):
            if fname in files:
                f = os.path.join(d, fname)

                if not os.path.exists(f):
                    raise ValueError("ValueError: " + f + " does not exist!")
        
                return [f, nib.load(f)]

        raise ValueError("ValueError: " + fname + " does not exist!")


    def load_mat(self, directory, mat):
        ''' Similar to above function, tailored to loading .mat files.
            Assumes the file is unique in the subdirectory tree.
            Returns a length 2 list -- [file path, matrix np.array].
            INPUT: string, string
            OUTPUT: list
        '''

        for d, _, files in os.walk(directory):
            if mat in files:
                f = os.path.join(d, mat)

                if not os.path.exists(f):
                    raise ValueError("ValueError: " + f + " does not exist!")
        
                return [f, np.loadtxt(f)]

        raise ValueError("ValueError: " + f + " does not exist!")


    def save_mni_data(self, save_file=None):
        ''' Convenience function for saving MNI images stored in this class
            object.
            Note, these MNI images are probably already stored in the MNI
            working directory.
            INPUT: string
            OUTPUT: None
        '''

        if not self.filtered_mni_image:
            print "Warning: Must have generated MNI data first!"
            return

        if not save_file:
            name = self.name + '-' + 'mni.nii.gz'
            sf = os.path.join(self.working_directory, name)

        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)

        location = os.path.join(self.working_directory, save_file)
        nib.save(self.filtered_mni_image, location)


#    def generate_mni(self, force=False):
#        ''' Uses Nipype FSL interface to 'applywarp' on the class contained
#            NIfTI images and generate a corresponding MNI space file, stored
#            in the task associated working directory.
#            INPUT: bool
#            OUTPUT: None
#        '''
#        img_file, _ = self.filtered_image
#        mni_file, _ = self.standard_mni_image
#        warp_file, _ = self.warp
#        affine_file, _ = self.affine
#
#        name = self.name + '-' + 'mni.nii.gz'
#        sf = os.path.join(self.working_directory, name)
#
#        if os.path.exists(sf) and not force:
#            print "MNI File Exists: Loading ..."
#            self.filtered_mni_image = [sf, nib.load(sf)]
#        else:
#            print "Generating MNI -- this will take some time..."
#            aw = fsl.ApplyWarp()
#            aw.inputs.in_file = img_file
#            aw.inputs.ref_file = mni_file
#            aw.inputs.field_file = warp_file
#            aw.inputs.premat = affine_file
#            aw.inputs.out_file = sf
#
#            aw.run()
#
#            self.filtered_mni_image = [sf, nib.load(sf)]
#
#            print "Done, saved to:", sf


def generate_mni(tc, force=False):
    ''' Uses Nipype FSL interface to 'applywarp' on the class contained
        NIfTI images and generate a corresponding MNI space file, stored
        in the task associated working directory.
        INPUT: bool
        OUTPUT: None
    '''
    img_file, _ = tc.filtered_image
    mni_file, _ = tc.standard_mni_image
    warp_file, _ = tc.warp
    affine_file, _ = tc.affine

    name = tc.name + '-' + 'mni.nii.gz'
    sf = os.path.join(tc.working_directory, name)

    if os.path.exists(sf) and not force:
        print "MNI File Exists: Loading ..."
        tc.filtered_mni_image = [sf, nib.load(sf)]
    else:
        print "Generating MNI -- this will take some time..."
        aw = fsl.ApplyWarp()
        aw.inputs.in_file = img_file
        aw.inputs.ref_file = mni_file
        aw.inputs.field_file = warp_file
        aw.inputs.premat = affine_file
        aw.inputs.out_file = sf

        aw.run()

        tc.filtered_mni_image = [sf, nib.load(sf)]

        print "Done, saved to:", sf
###############
# End of File
###############
