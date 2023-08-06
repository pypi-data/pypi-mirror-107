# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:20:02 2020

@author: hinsm
"""

from objseg.step1_posterior import step1_posterior
from objseg.step2_shapes_adapMH import step2_shape_likelihood
from objseg.step3_update import step3_update

class single_site_gibbs:
    
    #Without specifying the num_chains to run, this SSGS will only run ONCE!
    def __init__(self, param, S_mode, current_chain_num, num_chains, accepted):
        self.param = param
        self.S_mode = S_mode
        self.current_chain_num = current_chain_num
        self.num_chains = num_chains
        self.accepted = accepted
        
    def single_site_gibbs_sampler(self):
        # param = (pixel_indices, Z, S, object_center_array, beta_d, M, grid_points_array
        # km_bg_int, km_fg_int, MAX)
        upd_imdata = self.param[1]
        pixel_indices = self.param[3]
        min_semi_axis, max_semi_axis = self.param[18], self.param[19]
        log_normalized_fg_prob_vector, log_normalized_bg_prob_vector = self.param[10], self.param[11]
        mask_set = self.param[15]
        
        
        step1_Z, step1_S, updated_centres, updated_nod, updated_object_center_tree, self.S_mode, self.accepted = step1_posterior(self.param, self.S_mode, self.current_chain_num, self.accepted, pixels_to_skip=None).step1_prob()

        step2_S, self.S_mode, self.accepted = step2_shape_likelihood(step1_Z, step1_S, self.S_mode, upd_imdata, updated_centres, pixel_indices, min_semi_axis, max_semi_axis, self.current_chain_num, self.num_chains, self.accepted, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, mask_set).step2_prob()
        
        #This is where we update the param
        step3_update(self.param, step1_Z, step2_S, updated_centres, updated_nod, updated_object_center_tree).step3_prob()
        
        #Return only variables we want for visualization purposes! 
        return (self.param, self.S_mode, self.accepted)