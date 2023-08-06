# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 12:57:04 2020

@author: hinsm
"""

from numba import njit, prange
import numpy as np
import math
from copy import copy
import os
os.environ[ 'NUMBA_CACHE_DIR' ] = '/tmp/'

# STILL THE FASTEST OPTION

@njit(cache = True)
def generate_valid_indices_vector(valid_indices_vector, valid_x0_vector, valid_y0_vector, pixel_indices):
    
    for i in range(valid_y0_vector.size):
        
        valid_indices_vector[i] = pixel_indices[valid_y0_vector[i], valid_x0_vector[i]]

    return valid_indices_vector




@njit(cache = True, fastmath = True)
def ellipse_boolean(c, d, x_diff, cos_P, y_diff, sin_P):
    
    return (1/c**2)*(x_diff * cos_P + y_diff * sin_P)**2 + (1/d**2)*(x_diff * sin_P - y_diff * cos_P)**2 <= 1



@njit(cache = True, fastmath = True)
def is_indices_in_shape(box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, current_coord, shape_sample, processed_shape_samples_s):
    
    x_a = current_coord[0] #x
    y_b = current_coord[1] #y
    #c = shape_sample[0] / 2 + 0.000000001
    #d = shape_sample[1] / 2 + 0.000000001
    #P = shape_sample[2]
    
    y0_vector, x0_vector = box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector
    
    x_diff = x0_vector - x_a
    y_diff = y0_vector - y_b
    c = processed_shape_samples_s[0]
    d = processed_shape_samples_s[1]
    sin_P = processed_shape_samples_s[2]
    cos_P = processed_shape_samples_s[3]
    #sin_P = math.sin(P)
    #cos_P = math.cos(P)
    
    boolean = ellipse_boolean(c, d, x_diff, cos_P, y_diff, sin_P)
    #boolean = (1/c**2)*(x_diff * cos_P + y_diff * sin_P)**2 + (1/d**2)*(x_diff * sin_P - y_diff * cos_P)**2 <= 1

    # Return the locations of x0_vector, y0_vector values that satisfy the equations.
    valid_locations_vector = np.where(boolean)[0]
    
    # Retrieve the actual pixel indices with the x0, y0 locations
    valid_x0_vector = x0_vector[valid_locations_vector]
    
    valid_y0_vector = y0_vector[valid_locations_vector]
    
    #valid_indices_vector = pixel_indices[valid_y0_vector, valid_x0_vector]
    valid_indices_vector = np.zeros((valid_x0_vector.size, ), dtype = np.int64)
    
    valid_indices_vector = generate_valid_indices_vector(valid_indices_vector, valid_x0_vector, valid_y0_vector, pixel_indices)
    #valid_indices_vector = pixel_indices[valid_y0_vector, valid_x0_vector]
    
    return valid_indices_vector


"""
Test:
import time
start_time = time.time()
valid_indices_vector = is_indices_in_shape(box_region_pixel_indices, pixel_indices, object_center, shape_sample)
print("--- %s seconds ---" % (time.time() - start_time))
"""



#//////////////////////////////////////////////////////////////////////////

#@njit(cache=True)
def check_indices_in_existing_shapes(box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, box_region_indices_array, pixel_indices, object_center_array, S):

    n = S.shape[0]
    
    m = box_region_indices_array.size
    
    combined_indices_in_S = np.full((n, m), -1, dtype = np.int64)
    
    c_vector = S[:,0] / 2 + 0.000001
    d_vector = S[:,1] / 2 + 0.000001
    sin_P_vector = np.sin(S[:,2]).reshape((S[:,2].size, 1))
    cos_P_vector = np.cos(S[:,2]).reshape((S[:,2].size, 1))
    processed_S_array = np.column_stack((c_vector, d_vector, sin_P_vector, cos_P_vector))
    
    for s in range(n):
        
        indices_in_s = is_indices_in_shape(box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, object_center_array[s], S[s], processed_S_array[s])
        #indices_in_s = get_indices_in_shape(pixel_indices, current_coord, shape_sample)
        
        if indices_in_s.size != 0:
            
            combined_indices_in_S[s, 0 : indices_in_s.size] = indices_in_s

    # Flatten array
    flatten = combined_indices_in_S.flatten()
    
    # Retain only unique values
    unique = np.unique(flatten)
    
    # Remove zeros (these zeros come from when the array in this function was generated)
    output = unique[ unique != -1 ]
    
    
    return output



"""
Test:
import time
start_time = time.time()
combined_indices_in_S = check_indices_in_existing_shapes(box_region_pixel_indices, pixel_indices, object_center_array, S)
print("--- %s seconds ---" % (time.time() - start_time))
"""

#//////////////////////////////////////////////////////////////////////////



"""
Assumption: fg_set is SUBSET of box_set.
Purpose: This function finds the bg_set (complementary) set of fg_set within the box_set.
"""

@njit(cache=True)
def get_bg(mask_set, whole_set, box_set, fg_set):

    # This function/math is valid because our mask set is the original set of image pixels.
    
    #mask_box = np.repeat(-1, len(whole_set))
    mask_box = mask_set.copy()
    mask_box[box_set] = -2

    complement = whole_set[mask_box == -1]

    #mask_complement_fg = np.repeat(-1, len(whole_set))
    mask_complement_fg = mask_set.copy()
    mask_complement_fg[complement] = -2
    mask_complement_fg[fg_set] = -2

    bg_set = whole_set[mask_complement_fg == -1]

    return bg_set


"""
Purpose: This function takes the union of two sets and remove duplicates.
"""
@njit(cache = True, fastmath = True)
def union(mask_set, whole_set, arr1, arr2):

	#mask = np.repeat(-1, len(whole_set))
    mask = mask_set.copy()
    mask[arr2] = -2
    mask[arr1] = -2
    
    return whole_set[mask == -2]



@njit(cache=True)
def log_data_likelihood(combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, pixel_indices_vector, current_coord, shape_sample, processed_shape_samples_s, mask_set):

    # Finding all indices in shapes - these pixels will be foreground    
    valid_indices_vector = is_indices_in_shape(box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, current_coord, shape_sample, processed_shape_samples_s)
    
    fg_indices_in_box = union(mask_set, pixel_indices_vector, valid_indices_vector, combined_indices_in_shapes)
    
    # Finding all indices outside shapes, but in box - these pixels will be background
    bg_indices_in_box = get_bg(mask_set, pixel_indices_vector, box_region_indices_array, fg_indices_in_box)
    #bg_indices_in_box = np.setdiff1d(np.arange(len(pixel_indices_vector)), fg_indices_in_box)
    
    
    # Compute log likelihood
    return np.sum(log_normalized_fg_prob_vector[fg_indices_in_box]) + np.sum(log_normalized_bg_prob_vector[bg_indices_in_box])



#////////////////////////////////////////////////////////////////////////////
@njit(cache=True, parallel = True)
def shapes_sample_log_likelihood(num, combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, 
                                 box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, current_coord, shapes_sample_array, mask_set):

    shapes_sample_log_l_array = np.empty((num,1))
    
    c_vector = shapes_sample_array[:,0] / 2 + 0.000001
    d_vector = shapes_sample_array[:,1] / 2 + 0.000001
    sin_P_vector = np.sin(shapes_sample_array[:,2]).reshape((shapes_sample_array[:,2].size, 1))
    cos_P_vector = np.cos(shapes_sample_array[:,2]).reshape((shapes_sample_array[:,2].size, 1))
    processed_shape_samples_array = np.column_stack((c_vector, d_vector, sin_P_vector, cos_P_vector))
    
    pixel_indices_vector = pixel_indices.reshape((pixel_indices.size,))
    
    for s in prange(num):
                            
        shapes_sample_log_l_array[s] = log_data_likelihood(combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, pixel_indices_vector, current_coord, shapes_sample_array[s], processed_shape_samples_array[s], mask_set)
    
    #shapes_sample_log_l_array = np.array([log_data_likelihood() for s in range(300)])
    
    return shapes_sample_log_l_array



#////////////////////////////////////////////////////////////////////////////
#import multiprocessing as mp

#pool = mp.Pool()
#import concurrent.futures


#def shapes_sample_log_likelihood2(combined_indices_in_S, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, current_coord, shapes_sample_array):

    #shapes_sample_log_l_array = np.empty((shapes_sample_array.shape[0],1))
    
#    pixel_indices_vector = pixel_indices.reshape((pixel_indices.size,))
    
#    wrapper = lambda e: log_data_likelihood(combined_indices_in_S, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, 
#                                            box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, 
#                                            pixel_indices, pixel_indices_vector, current_coord, e)
    
#    #return np.array(list(pool.map(wrapper, shapes_sample_array)))
#    with concurrent.futures.ThreadPoolExecutor(max_workers = 8) as exe:
        
#        return np.array(list(exe.map(wrapper, shapes_sample_array)))
    


#////////////////////////////////////////////////////////////////////////////
@njit(cache = True)
def same_state_log_likelihood(combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, pixel_indices_vector, mask_set):
    
    fg_indices_in_box = combined_indices_in_shapes
    
    # Finding all indices outside shapes, but in box - these pixels will be background
    bg_indices_in_box = get_bg(mask_set, pixel_indices_vector, box_region_indices_array, fg_indices_in_box)
    
    # Compute log likelihood    
    log_l_fg = np.sum(log_normalized_fg_prob_vector[fg_indices_in_box])
    
    log_l_bg = np.sum(log_normalized_bg_prob_vector[bg_indices_in_box])

    log_likelihood = log_l_fg + log_l_bg
    
    return log_likelihood   
    

