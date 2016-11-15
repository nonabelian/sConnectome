import os

import nose.tools as n
import numpy as np
import nibabel as nib

from .context import src
from src.process_data.fmri_data import fMRIExperimentData
from src.process_data.fmri_data import fMRISubjectData
from src.process_data.fmri_data import fMRITaskData
from src.process_data.fmri_data import generate_mni_parallel
from src.process_data.fmri_data import generate_mni_threaded
from get_message import get_message


def testfMRIExperimentData():
    dirs = [os.path.join('tests', 'data', 'sub')]
    wd = os.path.join('tests', 'data')
    fed = fMRIExperimentData(dirs, working_directory=wd)

    exp = 1
    act = len(fed.subject_fmri_data)
    n.assert_equal(exp, act, msg=get_message('Subject fMRI List Length', exp,
                   act))

    exp = True
    act = isinstance(fed.subject_fmri_data[0], fMRISubjectData)
    n.assert_equal(exp, act, msg=get_message('Subject fMRI Type Check', exp,
                   act))


def test_fMRISubjectData():
    d = os.path.join('tests', 'data', 'sub')
    wd = os.path.join('tests', 'data')
    fsd = fMRISubjectData(d, working_directory=wd)

    exp = os.path.join('tests', 'data', 'sub')
    act = fsd.directory
    n.assert_equal(exp, act, msg=get_message('Directory', exp, act))

    exp = os.path.join('tests', 'data', 'MNI', 'sub')
    act = fsd.working_directory
    n.assert_equal(exp, act, msg=get_message('Working Directory', exp, act))

    exp = 'sub'
    act = fsd.name
    n.assert_equal(exp, act, msg=get_message('Name', exp, act))
    
    exp = 2
    act = len(fsd.task_fmri_data)
    n.assert_equal(exp, act, msg=get_message('Task fMRI List Length', exp, act))

    exp = True
    act = isinstance(fsd.task_fmri_data[0], fMRITaskData)
    n.assert_equal(exp, act, msg=get_message('Task fMRI Type Check', exp, act))


def test_get_subject_name():
    d = os.path.join('tests', 'data', 'sub')
    wd = os.path.join('tests', 'data')
    fsd = fMRISubjectData(d, working_directory=wd)

    exp = 'sub-name'
    d = os.path.join('tmp', 'dir.name', 'sub-name')
    act = fsd.get_subject_name(directory=d)
    n.assert_equal(exp, act, msg=get_message('Getting Subject Name 1', exp, act))

    exp = 'sub-name'
    d = os.path.join('tmp', 'dir.name', 'sub-name')
    act = fsd.get_subject_name(directory=d)
    n.assert_equal(exp, act, msg=get_message('Getting Subject Name 2', exp, act))


def test_fMRITaskData():
    d = os.path.join('tests', 'data', 'sub', 'model', 'task1.feat')
    wd = os.path.join('tests', 'data', 'MNI', 'sub')
    ftd = fMRITaskData(d, working_directory=wd)

    exp = os.path.join('tests', 'data', 'sub', 'model', 'task1.feat')
    act = ftd.directory
    n.assert_equal(exp, act, msg=get_message('Directory', exp, act))

    exp = os.path.join('tests', 'data', 'MNI', 'sub')
    act = ftd.working_directory
    n.assert_equal(exp, act, msg=get_message('Working Directory', exp, act))

    exp = 'task1'
    act = ftd.name
    n.assert_equal(exp, act, msg=get_message('Name', exp, act))

    exp = True
    act = isinstance(ftd.filtered_image[0], str)
    n.assert_equal(exp, act, msg=get_message('Filtered Image String Type', exp,
                   act))
    exp = True
    act = isinstance(ftd.filtered_image[1], nib.Nifti1Image)
    n.assert_equal(exp, act, msg=get_message('Filtered Image NIfTI Type', exp,
                   act))

    exp = True
    act = isinstance(ftd.structure_image[0], str)
    n.assert_equal(exp, act, msg=get_message('Structure Image String Type', exp,
                   act))
    exp = True
    act = isinstance(ftd.structure_image[1], nib.Nifti1Image)
    n.assert_equal(exp, act, msg=get_message('Structure Image NIfTI Type', exp,
                   act))

    exp = True
    act = isinstance(ftd.standard_mni_image[0], str)
    n.assert_equal(exp, act, msg=get_message('Standard Image String Type', exp,
                   act))
    exp = True
    act = isinstance(ftd.standard_mni_image[1], nib.Nifti1Image)
    n.assert_equal(exp, act, msg=get_message('Standard Image NIfTI Type', exp,
                   act))

    exp = True
    act = isinstance(ftd.affine[0], str)
    n.assert_equal(exp, act, msg=get_message('Affine String Type', exp, act))

    exp = np.ndarray
    act = type(ftd.affine[1])
    n.assert_equal(exp, act, msg=get_message('Affine Mat Type', exp, act))

    exp = True
    act = isinstance(ftd.warp[0], str)
    n.assert_equal(exp, act, msg=get_message('Warp String Type', exp, act))

    exp = True
    act = isinstance(ftd.warp[1], nib.Nifti1Image)
    n.assert_equal(exp, act, msg=get_message('Warp NIfTI Type', exp, act))

    exp = True
    act = isinstance(ftd.confounds[0], str)
    n.assert_equal(exp, act, msg=get_message('Confounds String Type', exp, act))

    exp = np.ndarray
    act = type(ftd.confounds[1])
    n.assert_equal(exp, act, msg=get_message('Confounds Mat Type', exp, act))

    exp = None
    act = ftd.filtered_mni_image
    n.assert_equal(exp, act, msg=get_message('Filtered MNI Initial Type', exp,
                   act))


def test_get_task_name():
    d = os.path.join('tests', 'data', 'sub', 'model', 'task1.feat')
    wd = os.path.join('tests', 'data', 'MNI', 'sub')
    ftd = fMRITaskData(d, working_directory=wd)

    exp = 'task1'
    d = os.path.join('tmp', 'dir.name', 'task1')
    act = ftd.get_task_name(directory='tmp/dir.name/task1/')
    n.assert_equal(exp, act, msg=get_message('Getting Subject Name 1', exp,
                   act))

    exp = 'task1'
    d = os.path.join('tmp', 'dir.name', 'task1.foo')
    act = ftd.get_task_name(directory='tmp/dir.name/task1.foo')
    n.assert_equal(exp, act, msg=get_message('Getting Subject Name 2', exp,
                   act))


def test_generate_mni_threaded():
    d = os.path.join('tests', 'data', 'sub')
    wd = os.path.join('tests', 'data')
    fsd = fMRISubjectData(d, working_directory=wd)

    generate_mni_threaded(fsd)

    for ftd in fsd.iter_task_data():
        exp = True
        act = isinstance(ftd.filtered_mni_image[0], str)
        n.assert_equal(exp, act, msg=get_message("Sting Type MNI", exp, act))

        exp = True
        act = isinstance(ftd.filtered_mni_image[1], nib.Nifti1Image)
        n.assert_equal(exp, act, msg=get_message("Nifti Type MNI", exp, act))

def test_generate_mni_parallel():
    fed = fMRIExperimentData(['data/sub/'], working_directory='data/')

    generate_mni_parallel(fed)

def test_load_mni():
    d = os.path.join('tests', 'data', 'sub', 'model', 'task1.feat')
    wd = os.path.join('tests', 'data', 'MNI', 'sub')
    ftd = fMRITaskData(d, working_directory=wd)

    ftd.load_mni()

    exp = True
    act = isinstance(ftd.filtered_mni_image[0], str)
    n.assert_equal(exp, act, msg=get_message('Filtered Image String Type', exp,
                   act))
    exp = True
    act = isinstance(ftd.filtered_mni_image[1], nib.Nifti1Image)
    n.assert_equal(exp, act, msg=get_message('Filtered Image NIfTI Type', exp,
                   act))
