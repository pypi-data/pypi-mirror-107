# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 02:21:19 2021

@author: hinsm
"""

import numpy as np
from rtree import index
from numba import int64, float64, njit, prange, jit
from numba.experimental import jitclass


spec = [
    ('coords', int64[:]),          # an array field
    ('dist', float64),             # a simpler field of just float
    ('nearest', int64[:]),         # an array field        
]

@jitclass(spec)
class GridPoint(object):
    
    def __init__(self):
        
        self.coords = np.arange(0,2, dtype = np.int64)
        
        # Distance to nearest neighbour
        #self.dist = float("inf")
        self.dist = 0.0001
        
        # Nearest neighbour (x, y)
        self.nearest = np.arange(0,2, dtype = np.int64)



def test_do_nothing(GridPoints_object_array):
    # O(m)
    size = GridPoints_object_array.shape[0]
    dists = np.zeros((size, ), dtype = np.float64)
    
    for g in range(size):
        
        dists[g] = GridPoints_object_array[g, 0].dist
        
    return dists


def test_insert(GridPoints_object_array, object_centre):
    # Complexity O(m)
    dists = []
    
    for g in range(GridPoints_object_array.shape[0]):
        
        d = np.linalg.norm(GridPoints_object_array[g, 0].coords - object_centre)
        
        if d < GridPoints_object_array[g, 0].dist:
            
            dists.append(d)
            
        else:
            
            dists.append(GridPoints_object_array[g, 0].dist)
            
    return dists


def test_remove(GridPoints_object_array, object_centre, object_center_tree):
    # O(m log n)
    dists = []
    
    for g in range(GridPoints_object_array.shape[0]):
        
        # Object centre being removed is nearest neighbour
        if object_centre == GridPoints_object_array[g, 0].nearest:
            
            # Get the two nearest
            nearest = list(object_center_tree.nearest(tuple(GridPoints_object_array[g, 0].coords), 2, objects = 'raw'))
            
            # it would be nearest[1], because nearest[0] would be object_centre.
            dists.append(np.linalg.norm(GridPoints_object_array[g, 0].coords - nearest[1]))
            
        else:    
            
            dists.append(GridPoints_object_array[g, 0].dist)
            
    return dists


def insert(GridPoints_object_array, object_pixel_index, object_centre, object_center_tree):
        
    x0, y0 = object_centre[0], object_centre[1]
    
    for g in range(GridPoints_object_array.shape[0]):
        
        d = np.linalg.norm(GridPoints_object_array[g, 0].coords - object_centre)
        
        if d < GridPoints_object_array[g, 0].dist:
            
            GridPoints_object_array[g, 0].dist = d
                    
            GridPoints_object_array[g, 0].nearest = object_centre
            
    object_center_tree.insert(object_pixel_index, [x0, y0, x0 + 1, y0 + 1],tuple(object_centre))
    
    
def remove(GridPoints_object_array, object_pixel_index, object_centre, object_center_tree):
    
    x0, y0 = object_centre[0], object_centre[1]
        
    for g in range(GridPoints_object_array.shape[0]):
        
        if object_centre == GridPoints_object_array[g, 0].nearest:
            
            nearest = object_center_tree.get_nearest(GridPoints_object_array[g, 0].coords, 2)
            
            GridPoints_object_array[g, 0].dist = np.linalg.norm(GridPoints_object_array[g, 0].coords - nearest[1])
            
            GridPoints_object_array[g, 0].nearest = nearest[1]
            
    object_center_tree.delete(object_pixel_index, [x0, y0, x0 + 1, y0 + 1])


