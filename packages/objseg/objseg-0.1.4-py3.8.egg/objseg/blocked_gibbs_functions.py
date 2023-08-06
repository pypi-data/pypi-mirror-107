# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 18:34:34 2021

@author: hinsm
"""

from numba import njit, prange
import numpy as np
import math


@njit(cache = True)
def logsumexp(x):
    
    c = x.max()
    
    return c + np.log(np.sum(np.exp(x - c)))


@njit(cache = True)
def blocking_image(img, num_y_pixels_per_block=0, num_x_pixels_per_block=0):
    
    if num_y_pixels_per_block != 0 and num_x_pixels_per_block != 0:
        
        M = num_y_pixels_per_block
        N = num_x_pixels_per_block
    
    else:
        gcd = math.gcd(img.shape[0], img.shape[1])
    
        if gcd == img.shape[0] or gcd == img.shape[1]:
            gcd = int(gcd/2)
        
        M = gcd
        N = gcd
    
    return [img[y : y + M, x : x + N]  for y in range(0, img.shape[0], M) for x in range(0, img.shape[1], N)]


#@njit(cache = True)
def reshape_tiles(tiles):
    
    tiles = np.array(tiles)
    num_blocks = tiles.shape[0]
    block_len = tiles.shape[1] * tiles.shape[2]
    
    flatten_tiles_pixel_indices = np.zeros((num_blocks, block_len), dtype = 'int64')
    
    for t in range(tiles.shape[0]):
    
        flatten_tiles_pixel_indices[t, :] = tiles[t].reshape((tiles[t].size, ))    
    
    return flatten_tiles_pixel_indices



@njit(cache = True)
def block_log_likelihood(flatten_tiles_pixel_indices, log_normalized_fg_prob_vector):
    
    block_log_likelihood_vector = np.zeros((flatten_tiles_pixel_indices.shape[0], ))
    
    for f in range(flatten_tiles_pixel_indices.shape[0]):

        block_log_likelihood_vector[f] = np.sum(log_normalized_fg_prob_vector[flatten_tiles_pixel_indices[f, ]])
        
    return block_log_likelihood_vector



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