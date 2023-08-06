# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 22:54:50 2021

@author: hinsm
"""

import h5py
import numpy as np
#import pandas as pd
from datetime import datetime

from objseg.hybrid_gibbs import hybrid_gibbs
from objseg.basic_preprocessing import basic_preprocessing
from objseg.post_process import load_results_df


def seg(
        in_image,
        min_semi_axis,
        max_semi_axis,
        min_area_thresh,
        max_area_thresh,
        num_chains=3000,
        num_cluster=2,
        spatial_distance_pixel_number=20,
        num_y_pixels_per_block=0, 
        num_x_pixels_per_block=0,
        percent=0.15,
        gmm_n=2,
        log_p_R_option="homo",
        seed=None):

    if seed is not None:
        np.random.seed(seed)

    param = basic_preprocessing(True, in_image, spatial_distance_pixel_number, min_semi_axis, max_semi_axis, min_area_thresh, max_area_thresh, num_cluster, gmm_n, log_p_R_option).basic_image_analyses()


    Z_sample = param[4]
    accepted =  np.array([0,0,0, 0] * param[5].shape[0]).reshape((param[5].shape[0], 4)) # Initialize acceptance counts; the FOURTH ZERO is to keep track whether the center has been deleted or not.
    
    start = datetime.now()
    
    param, Z_matrix, S_mode, accepted = hybrid_gibbs(param, Z_sample, accepted, num_chains, num_y_pixels_per_block, num_x_pixels_per_block, percent).hybrid_gibbs_sampler()

    now = datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")
    
    exec_time = now - start

    out_file = '../data_output/h5py_data_output_' + date_time + '_' + exec_time.seconds + 's' + exec_time.seconds.microseconds + 'ms' + '.h5'
    
    with h5py.File(out_file, 'w') as fh:
        
        fh.create_dataset('/data/final_cell_centres', data = param[6])
                
        fh.create_dataset('/data/final_S_vector', data = param[5])



def write_results_file(in_results_file, compress=False):

    df = load_results_df(in_results_file)
    
    now = datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")
    
    if compress:
        df.to_csv('../data_output/cell_location_shape_info_' + date_time + '.tsv', compression='gzip', float_format='%.4f', index=False, sep='\t')

    else:
        df.to_csv('../data_output/cell_location_shape_info_' + date_time + '.tsv', float_format='%.4f', index=False, sep='\t')