# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:45:07 2020

@author: hinsm
"""

import numpy as np


def find_argwhere(object_center_array, current_coord):
    
    i1 = np.argwhere(object_center_array[:,0] == current_coord[0])
    i2 = np.argwhere(object_center_array[:,1] == current_coord[1])
    
    return (i1, i2)
    

#This code is tested and appear to be stable.
#@numba.njit(cache=True)
def oc_pos_search(object_center_array, current_coord):
    #------------------------------------------------------------------------------
    # Input: current_coord (np.array), object_center_array (np.array)
    # Output: row position (integer) of the current_coord in the object_center_array
    #------------------------------------------------------------------------------    
    i1, i2 = find_argwhere(object_center_array, current_coord)
    
    if i1.size == 0 or i2.size == 0:
        pos = 'No'
    else:
        pos = np.intersect1d(i1,i2)
        if pos.size == 0:
            pos = 'No'
        else:
            pos = pos[0]
    return pos


