# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 18:34:34 2021

@author: hinsm
"""

import numpy as np


from objseg.blocked_gibbs_functions import logsumexp, blocking_image, reshape_tiles, block_log_likelihood
from objseg.step1_posterior import step1_posterior
from objseg.step2_shapes_adapMH import step2_shape_likelihood
from objseg.step3_update import step3_update


# TWO NEW PARAMETERS TO ADD TO PIPELINE INITIALIZATION PARAMETERS
#num_y_pixels_per_block=25, num_x_pixels_per_block=25 (DEFAULT TO 0 - IMPLYING LET SYSTEM DETERMINE)


def find_pixels_to_skip(img, pixel_indices, log_normalized_fg_prob_vector, num_y_pixels_per_block=0, num_x_pixels_per_block=0, percent=0.15):
    
    # To understand this structure, the OUTER loop is y, the INNER loop is x.
    tiles_pixel_indices = blocking_image(pixel_indices, num_y_pixels_per_block, num_x_pixels_per_block)


    # Flatten the tiles pixel indices, such that each row represents the pixel indices of each block
    flatten_tiles_pixel_indices = reshape_tiles(np.array(tiles_pixel_indices))


    # Compute the log foreground likelihood of each block
    block_log_likelihood_vector = block_log_likelihood(flatten_tiles_pixel_indices, log_normalized_fg_prob_vector)


    # LogExp Normalize the vector
    log_l_vec = np.around(block_log_likelihood_vector, decimals = 2)
    normalized_block_log_likelihood_vector = np.exp(log_l_vec - logsumexp(log_l_vec))


    # Sample the top 15% of all the blocks - these 5% would go through the Step 1 scan.
    top15_percent = int(max(2, np.ceil(block_log_likelihood_vector.size * percent))) # Use Ceiling; Also set max to scan at least 2 blocks
    
    x_disc = np.arange(0, normalized_block_log_likelihood_vector.size)
    
    try:
        
        block_number_vector = np.random.choice(x_disc, size = top15_percent, replace = False, p = normalized_block_log_likelihood_vector)
        
    except ValueError:
        
        block_number_vector = np.random.choice(x_disc, size = 1, replace = False, p = normalized_block_log_likelihood_vector)


    # Find pixels to skip scanning for Step1 Posterior
    blocks_pixel_indices_to_skip = flatten_tiles_pixel_indices[np.setdiff1d(x_disc, block_number_vector), :].flatten()

    return blocks_pixel_indices_to_skip



class blocked_gibbs:
    
    #Without specifying the num_chains to run, this SSGS will only run ONCE!
    def __init__(self, param, S_mode, current_chain_num, num_chains, accepted, num_y_pixels_per_block=0, num_x_pixels_per_block=0, percent=0.15):
        self.param = param
        self.S_mode = S_mode
        self.current_chain_num = current_chain_num
        self.num_chains = num_chains
        self.accepted = accepted
        self.num_y_pixels_per_block = num_y_pixels_per_block
        self.num_x_pixels_per_block = num_x_pixels_per_block
        self.percent = percent
        
    def blocked_gibbs_sampler(self):
        # param = (pixel_indices, Z, S, object_center_array, beta_d, M, grid_points_array
        # km_bg_int, km_fg_int, MAX)
        upd_imdata = self.param[1]
        pixel_indices = self.param[3]
        min_semi_axis, max_semi_axis = self.param[18], self.param[19]
        log_normalized_fg_prob_vector, log_normalized_bg_prob_vector = self.param[10], self.param[11]
        mask_set = self.param[15]
        
        
        blocks_pixel_indices_to_skip = find_pixels_to_skip(upd_imdata, pixel_indices, log_normalized_fg_prob_vector, self.num_y_pixels_per_block, self.num_x_pixels_per_block, self.percent)
        
        
        step1_Z, step1_S, updated_centres, updated_nod, updated_object_center_tree, self.S_mode, self.accepted = step1_posterior(self.param, self.S_mode, self.current_chain_num, self.accepted, blocks_pixel_indices_to_skip).step1_prob()

        
        step2_S, self.S_mode, self.accepted = step2_shape_likelihood(step1_Z, step1_S, self.S_mode, upd_imdata, updated_centres, pixel_indices, min_semi_axis, max_semi_axis, self.current_chain_num, self.num_chains, self.accepted, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, mask_set).step2_prob()
        
        #This is where we update the param
        step3_update(self.param, step1_Z, step2_S, updated_centres, updated_nod, updated_object_center_tree).step3_prob()
        
        #Return only variables we want for visualization purposes! 
        return (self.param, self.S_mode, self.accepted)

