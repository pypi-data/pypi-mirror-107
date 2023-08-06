# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 22:43:35 2021

@author: hinsm
"""

import numpy as np
from numba import njit
import math


import objseg.shapes as shapes


@njit(cache = True)
def mh(jrange, n, accepted, S, S_mode, combined_indices_in_S, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, pixel_indices_vector, current_coord, mask_set):
    
    print("test1")
    rnorm = np.random.normal
    uniform = np.random.uniform
        
    for j in range(jrange):
        # Substep 0: 
        #validation_obj = shapes_validation(S[n], min_semi_axis, max_semi_axis)
        #major_axis_minimum, major_axis_maximum, minor_axis_minimum, minor_axis_maximum, min_rad, max_rad = validation_obj.comparison()
        eps_ra = rnorm(0, S[n, 4] ) # lambda_ra = S[n, 4]
                
        eps_rb = rnorm(0, S[n, 5] ) # lambda_rb = S[n, 5]
                
        eps_p = rnorm(0, S[n, 6] ) # lambda_p  S[n, 6]
        
        #print("eps_ra: " + str(eps_ra))
            
        # Substep 1. Proposing random walk shape_sample for each shape parameter independently
        proposed_shape_sample_ra = np.array([S[n, 0] + eps_ra, S[n, 1],          S[n, 2]]) #propose for major axis
        proposed_shape_sample_rb = np.array([S[n, 0],          S[n, 1] + eps_rb, S[n, 2]]) #propose for minor axis
        proposed_shape_sample_p = np.array([S[n, 0],          S[n, 1],          S[n, 2] + eps_p]) #propose for rotational angle
        
        processed_shape_sample_ra = np.array([proposed_shape_sample_ra[0] / 2 + 0.00001, proposed_shape_sample_ra[1] / 2 + 0.00001, math.sin(proposed_shape_sample_ra[2]), math.cos(proposed_shape_sample_ra[2])])
        processed_shape_sample_rb = np.array([proposed_shape_sample_rb[0] / 2 + 0.00001, proposed_shape_sample_rb[1] / 2 + 0.00001, math.sin(proposed_shape_sample_rb[2]), math.cos(proposed_shape_sample_rb[2])])
        processed_shape_sample_p = np.array([proposed_shape_sample_p[0] / 2 + 0.00001, proposed_shape_sample_p[1] / 2 + 0.00001, math.sin(proposed_shape_sample_p[2]), math.cos(proposed_shape_sample_p[2])])
            
        # Substep 2: Compute log appearance likelihood for each proposal (in our newest modification, this would be our log posterior with proposed value)
        #------------------------------------------------------------------------------------------------------------------
        proposed_log_shape_prob_ra = shapes.log_data_likelihood(combined_indices_in_S, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, pixel_indices_vector, current_coord, proposed_shape_sample_ra, processed_shape_sample_ra, mask_set)
        proposed_log_shape_prob_rb = shapes.log_data_likelihood(combined_indices_in_S, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, pixel_indices_vector, current_coord, proposed_shape_sample_rb, processed_shape_sample_rb, mask_set)
        proposed_log_shape_prob_p = shapes.log_data_likelihood(combined_indices_in_S, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, pixel_indices_vector, current_coord, proposed_shape_sample_p, processed_shape_sample_p, mask_set)
                
        #------------------------------------------------------------------------------------------------------------------
        # Substep 3: Compute log shape prior
        #sp_ma = sp_mb = 1 / (max_semi_axis - min_semi_axis)
        #sp_p = 1 / (2*math.pi)
                
        # Substep 5: Log-acceptance rate
        #if j == 0:
        current_log_shape_prob_ra = S_mode[n, 4]
        current_log_shape_prob_rb = S_mode[n, 5]
        current_log_shape_prob_p = S_mode[n, 6]
            
        # This is more sensible, but it always leads to reject since alpha >> 1.
        alpha_ra = proposed_log_shape_prob_ra - current_log_shape_prob_ra
        alpha_rb = proposed_log_shape_prob_rb - current_log_shape_prob_rb
        alpha_p = proposed_log_shape_prob_p - current_log_shape_prob_p
                
        # Substep 6: Sample a random uniform variate
        u_ra = uniform(0, 1)
                
        # Substep 7: Test proposed value
        #if np.log(u) < alpha:
        if np.log(u_ra) < alpha_ra:
            # Accept and officially updating the accepted "shape sample" and "posterior prob"
            S_mode[n, 4] = proposed_log_shape_prob_ra
                    
            S_mode[n, 0] = S[n, 0] = S[n, 0] + eps_ra
                    
            accepted[0] += 1
            #print("r_a: accepted")
            #else:
                # Reject
                # nothing happens; no action taken(?)
            #print("ra accepted: " + str(accepted[0]))
            
        u_rb = uniform(0, 1)
        if np.log(u_rb) < alpha_rb:
                    
            S_mode[n, 5] = proposed_log_shape_prob_rb
            
            S_mode[n, 1] = S[n, 1] = S[n, 1] + eps_rb
                    
            accepted[1] += 1   
            #print("r_b: accepted")

        u_p = uniform(0, 1)
        if np.log(u_p) < alpha_p:
                    
            S_mode[n, 6] = proposed_log_shape_prob_p
                    
            S_mode[n, 2] = S[n, 2] = S[n, 2] + eps_p
                    
            accepted[2] += 1     
            #print("p: accepted")
            
    return S, S_mode, accepted