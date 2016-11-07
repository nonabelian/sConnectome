import nose.tools as n

from .context import src
from src.process_data.fmri_data import fMRIExperimentData
from src.process_data.fmri_data import fMRISubjectData
from src.process_data.fmri_data import fMRITaskData
from get_message import get_message


def testfMRIExperimentData():
    dirs = ['data/sub']
    fed = fMRIExperimentData(dirs, working_directory='data/')

    exp = 1
    act = len(fed.subject_fmri_data)
    n.assert_equal(exp, act, msg=get_message('Subject fMRI List Length', exp,
                   act))

    exp = type(fMRISubjectData)
    actual = type(fed.subject_fmri_data[0])
    n.assert_equal(exp, act, msg=get_message('Subject fMRI Type Check', exp,
                   act))


def test_fMRISubjectData():
    fsd = fMRISubjectData('data/sub/', working_directory='data/')

    exp = 'data/sub/'
    act = fsd.directory
    n.assert_equal(exp, act, msg=get_message('Directory', exp, act))

    exp = 'data/MNI'
    act = fsd.working_directory
    n.assert_equal(exp, act, msg=get_message('Working Directory', exp, act))

    exp = 'sub'
    act = fsd.name
    n.assert_equal(exp, act, msg=get_message('Name', exp, act))
    
    exp = 2
    act = len(fsd.task_fmri_data)
    n.assert_equal(exp, act, msg=get_message('Task fMRI List Length', exp, act))

    exp = type(fMRITaskData)
    actual = type(fed.task_fmri_data[0])
    n.assert_equal(exp, act, msg=get_message('Task fMRI Type Check', exp, act))


def test_get_subject_name():
    fsd = fMRISubjectData('data/sub/', working_directory='data/')

    exp = 'sub-name'
    act = fsd.get_subject_name(directory='tmp/dir.name/sub-name/')
    n.assert_equal(exp, act, msg=get_message('Getting Subject Name 1', exp, act))

    exp = 'sub-name'
    act = fsd.get_subject_name(directory='tmp/dir.name/sub-name')
    n.assert_equal(exp, act, msg=get_message('Getting Subject Name 2', exp, act))


def test_fMRITaskData():
    ftd = fMRITaskData('data/sub/model/task1.feat/', working_directory='data/')

    exp = 'data/sub/model/task1.feat/'
    act = fsd.directory
    n.assert_equal(exp, act, msg=get_message('Directory', exp, act))

    exp = 'data/MNI/sub/'
    act = fsd.working_directory
    n.assert_equal(exp, act, msg=get_message('Working Directory', exp, act))

    exp = 'task1'
    act = fsd.name
    n.assert_equal(exp, act, msg=get_message('Name', exp, act))

    exp = type(fMRITaskData)
    actual = type(fed.task_fmri_data[0])
    n.assert_equal(exp, act, msg=get_message('Task fMRI Type Check', exp, act))
    

def test_get_taskname():
    ftd = fMRITaskData('data/sub/task1.feat/',
                       working_directory='data/MNI/sub/')

    exp = 'task1'
    act = fsd.get_subject_name(directory='tmp/dir.name/task1/')
    n.assert_equal(exp, act, msg=get_message('Getting Subject Name 1', exp,
                   act))

    exp = 'task1'
    act = fsd.get_subject_name(directory='tmp/dir.name/task1.foo')
    n.assert_equal(exp, act, msg=get_message('Getting Subject Name 2', exp,
                   act))

def test_load_nii():
    pass

def test_load_mat():
#    ftd = fMRITaskData('data/sub/model/task1.feat/', working_directory='data/')
    pass

def test_save_mni_data():
    pass

def test_generate_mni():
    ftd = fMRITaskData('data/sub/model/task1.feat/', working_directory='data/')

    ftd.generate_mni()

    exp = str
    act = ftd.filtered_mni_image[0]
    n.assert_equal(exp, act, msg=get_message("Str Type MNI", exp, act))

    exp = True
    act = isinstance(ftd.filtered_mni_image[0], nib.Nifti1Image)
    n.assert_equal(exp, act, msg=get_message("Nifti Type MNI", exp, act))

