from nilearn import image
from nilearn import input_data
from nilearn import plotting


def plot_connectome2d(graph, show_plot=False, save_image=None):
    ''' Plot the 2D connectome a la Nilearn tutorials
        INPUT: GraphSubjectData
        OUPUT: None
    '''
    title = "GroupSparseCovariance"

    atlas_imgs = image.iter_img(graph.maps)
    atlas_region_coords = [plotting.find_xyz_cut_coords(img) \
                            for img in atlas_imgs]

    mat = graph.norm_cov

    display = plotting.plot_connectome(-1 * mat,
                                       atlas_region_coords,
                                       edge_threshold='90%',
                                       title=title,
                                       display_mode="lzr",
                                       edge_vmax=.5, edge_vmin=-.5)

    if save_image:
        display.savefig(save_image)

    if show_plot:
        plotting.show()


def plot_filtered_mni(fmri_task_data, show_plot=False, save_image=None):

    _, filtered_mni = fmri_task_data.filtered_mni_image
    _, c = fmri_task_data.confounds

    masker = input_data.NiftiMasker(detrend=True,
       low_pass=None, high_pass=0.01, t_r=2.5, standardize=True)

    masker.fit(filtered_mni)

    hv_confounds = image.high_variance_confounds(filtered_mni)
    img_2darray = masker.transform(filtered_mni, confounds=[hv_confounds, c])

    # Turn into a NIfTI image:
    pimg = masker.inverse_transform(img_2darray)

    # Grab a frame to plot
    i = 0
    for p1img in image.iter_img(pimg):
        if i == 10:
            break
        i += 1

    display = plotting.plot_stat_map(p1img)
    
    if save_image:
        display.savefig(save_image)

    if show_plot:
        plotting.show()


