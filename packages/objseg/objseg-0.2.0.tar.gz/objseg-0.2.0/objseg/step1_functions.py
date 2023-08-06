# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 14:18:28 2021

@author: hinsm
"""

from numba import njit, prange
import numpy as np
import math

@njit(cache = True)
def generate_shapes_sample_array(min_semi_axis, max_semi_axis, num):
    
    maj_axis = np.random.uniform(min_semi_axis, max_semi_axis, num)
                    
    min_axis = np.random.uniform(min_semi_axis, max_semi_axis, num)
                    
    angle = np.random.uniform(-math.pi, math.pi, num)
                        
    shapes_sample_array = (np.vstack((maj_axis, min_axis, angle))).T
    
    return shapes_sample_array


@njit(cache=True)
def get_normalized_p(log_p):
    """
    :param log_p: np.array([-1.61, -0.36, -3.00, -3.22, -4.61])
    :return: np.array([0.2, 0.7, 0.05, 0.04, 0.01])
    """
    log_C = np.logaddexp(log_p[0], log_p[1])
    
    for i in range(len(log_p) - 2):
        
        log_C = np.logaddexp(log_C, log_p[ i + 2 ])
        
    log_p = log_p - log_C
    
    p = np.exp(log_p)
    
    #rounded_p = np.round(p, decimals=8)
    return p


@njit(cache = True)
def logsumexp(x):
    
    c = x.max()
    
    return c + np.log(np.sum(np.exp(x - c)))
