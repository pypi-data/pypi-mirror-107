# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:58:13 2020

@author: hinsm
"""

# THIS FILE HAS BEEN VERIFIED TO PRODUCE CORRECT OUTPUT!

import math
import numpy as np
from numba import njit


@njit(cache = True)
def range_cal(a, b, c, img_num_row, img_num_col):
        
    cond_1m = min( max(a - c, 0), img_num_col - 1)
    cond_1n = min( max(a + c, 0), img_num_col - 1)
    cond_1o = min( max(b - c, 0), img_num_row - 1)
    cond_1p = min( max(b + c, 0), img_num_row - 1)
    
    if cond_1m < cond_1n:
        x_range = np.arange(math.floor(cond_1m), math.ceil(cond_1n + 1), 1)
    elif cond_1m > cond_1n:
        x_range = np.arange(math.floor(cond_1n), math.ceil(cond_1m + 1), 1)
    if cond_1o < cond_1p:
        y_range = np.arange(math.floor(cond_1o), math.ceil(cond_1p + 1), 1)
    elif cond_1o > cond_1p:
        y_range = np.arange(math.floor(cond_1p), math.ceil(cond_1o + 1), 1)

    return x_range, y_range



@njit(cache = True)
def numba_tile(x_range, y_range_size):
    
    repeat1 = np.repeat(x_range, y_range_size)
    reshape1 = repeat1.reshape(-1, y_range_size)
    transpose1 = np.transpose(reshape1)
    tile = transpose1.flatten()
    
    return tile



@njit(cache = True)
def find_indices_in_box(object_center, max_semi_axis, pixel_indices):
    
    a = object_center[0] # corresponds to x (since we flipped y <-> x in step 1)
    b = object_center[1] # corresponds to y
    c = int(max_semi_axis/2) + 3   
    
    top_left_pix_a = max(a-c, 0)
    top_left_pix_b = max(b-c, 0)
    
    max_x_axis = min(a+c, pixel_indices.shape[1])
    max_y_axis = min(b+c, pixel_indices.shape[0])
    
    return np.array([pixel_indices[y, x]  for y in range(top_left_pix_b, min(max_y_axis + 1, pixel_indices.shape[0])) for x in range(top_left_pix_a, min(max_x_axis + 1, pixel_indices.shape[1]))]).flatten()



@njit(cache = True)
def find_top_left_pixel(object_center, max_semi_axis, pixel_indices):
    
    a = object_center[0] # corresponds to x (since we flipped y <-> x in step 1)
    b = object_center[1] # corresponds to y
    c = int(max_semi_axis/2) + 3   
    
    top_left_pix_a = max(a-c, 0)
    top_left_pix_b = max(b-c, 0)
    
    top_left_pix = pixel_indices[top_left_pix_b, top_left_pix_a]
    
    return top_left_pix


#@njit(cache = True)
def box_indices_to_coordinates(object_center, max_semi_axis, pixel_indices):
    
    a = object_center[0] # corresponds to x (since we flipped y <-> x in step 1)
    b = object_center[1] # corresponds to y
    c = int(max_semi_axis/2) + 3   
    
    top_left_pix_x = max(a-c, 0)
    top_left_pix_y = max(b-c, 0)
    
    x_range, y_range = range_cal(a, b, c, pixel_indices.shape[0], pixel_indices.shape[1])
    
    x = np.arange(top_left_pix_x, top_left_pix_x + x_range.size)
    
    y = np.arange(top_left_pix_y, top_left_pix_y + y_range.size)
    
    #coords = np.transpose([np.repeat(y, len(x)), np.tile(x, len(y))])
    
    coords = [np.repeat(y, x.shape[0]), numba_tile(x, y.shape[0])]
    
    return coords