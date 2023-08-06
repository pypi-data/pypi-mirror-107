# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 02:21:19 2021
@author: hinsm
"""

import numpy as np
from rtree import index

class GridPoint(object):
    
    def __init__(self, coords):
        
        self.coords = coords
        
        # Distance to nearest neighbour
        self.dist = float("inf")
        
        # Nearest neighbour (x, y)
        self.nearest = None


def test_do_nothing(GridPoints_object_array):
    # O(m)
    dists = []
    
    for g in range(GridPoints_object_array.shape[0]):
        
        dists.append(GridPoints_object_array[g, 0].dist)
        
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
        if object_centre[0] == GridPoints_object_array[g, 0].nearest[0] and object_centre[1] == GridPoints_object_array[g, 0].nearest[1]:
            
            # Get the two nearest
            nearest = list(object_center_tree.nearest(tuple(GridPoints_object_array[g, 0].coords), 2, objects = 'raw'))
            
            if len(nearest) == 0:
                 
                dists.append(1)
                
            elif len(nearest) == 1:
                
                dists.append(np.linalg.norm(GridPoints_object_array[g, 0].coords - nearest[0]))
                
            else:
            
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
        
        if object_centre[0] == GridPoints_object_array[g, 0].nearest[0] and object_centre[1] == GridPoints_object_array[g, 0].nearest[1]:
            
            nearest = list(object_center_tree.nearest(tuple(GridPoints_object_array[g, 0].coords), 2, objects = 'raw'))
            
            if len(nearest) == 1:
                GridPoints_object_array[g, 0].dist = np.linalg.norm(GridPoints_object_array[g, 0].coords - np.array([50,50]))
            
                GridPoints_object_array[g, 0].nearest = np.array([50,50])          
            
            else: 
                GridPoints_object_array[g, 0].dist = np.linalg.norm(GridPoints_object_array[g, 0].coords - nearest[1])
            
                GridPoints_object_array[g, 0].nearest = nearest[1]
            
    object_center_tree.delete(object_pixel_index, [x0, y0, x0 + 1, y0 + 1])