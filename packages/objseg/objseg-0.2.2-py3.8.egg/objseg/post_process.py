# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:10:56 2021

@author: hinsm
"""

import h5py
import numpy as np
import pandas as pd



def load_results_df(file_name):
    
    with h5py.File(file_name, 'r') as fh:
        
        cell_centres = fh['/data/final_cell_centres'][()]

        shape_param = fh['/data/final_S_vector'][()]

    shape_param = shape_param[:,0:4]
    
    df = np.hstack((cell_centres, shape_param))
    
    df = np.hstack(((np.arange(cell_centres.shape[0]) + 1).reshape((cell_centres.shape[0],1)), df))

    df = pd.DataFrame(df)

    df = df.rename(columns = {0: 'cell_count', 1: 'x_coordinate', 2: 'y_coordinate', 3: 'x_major_full_axis_length', 4: 'y_minor_full_axis_length', 5: 'rotational_angle', 6: 'pixel_indices'})

    return df

