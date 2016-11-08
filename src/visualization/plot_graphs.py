from nilearn import image
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

    i = 0
    for img in image.iter_img(filtered_mni):
        if i == 10:
            break
        i += 1

    display = plotting.plot_stat_map(img, threshold=2000)
    
    if save_image:
        display.savefig(save_image)

    if show_plot:
        plotting.show()
