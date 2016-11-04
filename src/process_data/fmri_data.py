import os

import numpy as np
import nibabel as nib
from nipype.interfaces import fsl


class fMRISubjectData(object):
    ''' Class that contains FEAT fMRI data FOR ALL TASKS performed by one
        particular subject, given a subject directory.
        INPUT: string, string, string, string, string, string, string
                'working_directory' -- needed for manipulating nii images. 
                'filtered..' -- filtered 4D fMRI subject data
                'structure..' -- high resolution subject structural image
                'standard' -- generic template.
                'affine' -- affine transformation from 'filtered' to 'structure'
                'warp' -- subsequent warp transformation from 'structure' to
                          'standard'
    '''
    def __init__(self, directory, working_directory='./.tmp',
                 filtered_data='filtered_func_data.nii.gz',
                 structure_data='highres.nii.gz',
                 standard_data='standard.nii.gz',
                 affine='example_func2highres.mat',
                 warp='highres2standard_warp.nii.gz'):
        self.directory = directory
        self.working_directory = self._make_wd(working_directory)

        # Label for this data -- e.g. 'sub001', should match that found in
        # 'demographics.txt'
        self.name = self.get_subject_name(directory=directory)

        # Dictionary of task data, keyed by task name.
        self.task_fmri_data = self.load_subject_data(directory,
                                                     self.working_directory,
                                                     filtered_data,
                                                     structure_data,
                                                     standard_data,
                                                     affine,
                                                     warp)

    def _make_wd(self, working_directory):
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
        if not directory:
            return self.name

        root, dirname = os.path.split(directory.strip(os.sep))
        return dirname


    def load_subject_data(self, directory, working_directory, filtered_data,
                          structure_data, standard_data, affine, warp):
        subj_fmri = []

        for d, _, files in os.walk(directory):
            if filtered_data in files:
                fmri_task = fMRITaskData(d, working_directory,
                                         filtered_data, structure_data,
                                         standard_data, affine, warp)

                subj_fmri.append(fmri_task)
        
        return subj_fmri


class fMRITaskData(object):
    ''' Class to encapsulate FEAT preprocessed fMRI data -- given a subject
        task directory.
        INPUT: string, string, string, string, string, string, string
                'filtered..' -- filtered 4D fMRI subject data
                'structure..' -- high resolution subject structural image
                'standard' -- generic template.
                'affine' -- affine transformation from 'filtered' to 'structure'
                'warp' -- subsequent warp transformation from 'structure' to
                          'standard'
    '''
    def __init__(self, directory, working_directory,
                 filtered_data='filtered_func_data.nii.gz',
                 structure_data='highres.nii.gz',
                 standard_data='standard.nii.gz',
                 affine='example_func2highres.mat',
                 warp='highres2standard_warp.nii.gz'):
        # Directory to the FEAT task data -- e.g.
        # 'sub001/model/model001/task001.feat/'
        self.directory = directory
        self.working_directory = working_directory

        # Task name.  As per the above example: 'task001'
        self.name = self.get_taskname(directory)

        # Note: the following images have the form [path, data]

        # FEAT filtered/preprocessed subject 4D fMRI data.
        self.filtered_image = self.load_nii(directory, filtered_data)

        # Highres structural MRI 3D image of patient
        self.structure_image = self.load_nii(directory, structure_data)

        # Structural template 3D image on which to fit all subjects.
        self.standard_mni_image = self.load_nii(directory, standard_data)

        self.affine = self.load_affine(directory, affine)
        self.warp = self.load_nii(directory, warp)

        # Warped 4D subject data -- fit to structural template.
        self.filtered_mni_image = None


    def get_taskname(self, directory):
        if not directory:
            return self.name

        tname_dir, ext = os.path.splitext(directory.strip(os.sep))

        root, tname = os.path.split(tname_dir)
        return tname

    def load_nii(self, directory, fname):
        for d, _, files in os.walk(directory):
            if fname in files:
                f = os.path.join(d, fname)

                if not os.path.exists(f):
                    raise ValueError("ValueError: " + f + " does not exist!")
        
                return [f, nib.load(f)]

        raise ValueError("ValueError: " + f + " does not exist!")


    def load_affine(self, directory, affine):
        for d, _, files in os.walk(directory):
            if affine in files:
                f = os.path.join(d, affine)

                if not os.path.exists(f):
                    raise ValueError("ValueError: " + f + " does not exist!")
        
                return [f, np.loadtxt(f)]

        raise ValueError("ValueError: " + f + " does not exist!")


    def save_mni_data(self, save_file=None):
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


    def generate_mni(self):
        img_file, _ = self.filtered_image
        mni_file, _ = self.standard_mni_image
        warp_file, _ = self.warp
        affine_file, _ = self.affine

        name = self.name + '-' + 'mni.nii.gz'
        sf = os.path.join(self.working_directory, name)

        aw = fsl.ApplyWarp()
        aw.inputs.in_file = img_file
        aw.inputs.ref_file = mni_file
        aw.inputs.field_file = warp_file
        aw.inputs.premat = affine_file
        aw.inputs.out_file = sf

        aw.run()

        self.filtered_mni_image = [sf, nib.load(sf)]


###############
# End of File
###############
