# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:14:40 2020

@author: hinsm
"""

import numpy as np
import math
import matplotlib as mpl


from objseg.single_site_gibbs import single_site_gibbs
from objseg.blocked_gibbs import blocked_gibbs
from objseg.results_analyses import results_analyses
from objseg.step2_shapes_adapMH import step2_shape_likelihood
from objseg.step3_update import step3_update


class hybrid_gibbs:
    
    def __init__(self, param, Z_sample, accepted, num_chains, num_y_pixels_per_block=0, num_x_pixels_per_block=0, percent=0.15):
        self.param = param
        self.Z_sample = Z_sample
        self.accepted = accepted
        self.num_chains = num_chains
        self.num_y_pixels_per_block = num_y_pixels_per_block
        self.num_x_pixels_per_block = num_x_pixels_per_block
        self.percent = percent

    def hybrid_gibbs_sampler(self):
    
        initial_posterior_prob_matrix = np.array([1,1,1] * (np.sum(self.param[4]))).reshape((np.sum(self.param[4]), 3))
        
        S_mode = np.column_stack((self.param[5][:, 0:4], initial_posterior_prob_matrix))
        
        for i in range(self.num_chains):
            #We use the randomness of flipping a fair coin to determine whether we run 
            # a single site or a sigbbs sampler
            random = np.random.binomial(1, 0.5)
            
            print("Current iteration: " + str(i+1) + " of "  + str(self.num_chains)  + ". Num. of OC (last iteration) is: " + str(np.sum(self.param[4])) )
            if random == 0:
                
                # if the random value is 0, then we run a Single Site Gibbs Sampler
                #then store the sampled value
                #then update the parameter to this newly sampled value
                print("Running a Single Site Gibbs Sampler. Chain #" + str(i))
                
                ssgs_obj = single_site_gibbs(self.param, S_mode, i, self.num_chains, self.accepted)
                
                self.param, S_mode, self.accepted = ssgs_obj.single_site_gibbs_sampler()
    
            elif random == 1:
                    
                # if the random value is 0, then we run a blocked Gibbs Sampler
                #then store the sampled value
                #then update the parameter to this newly sampled value
                print("Running a Blocked Gibbs Sampler. Chain #" + str(i))
                
                bgs_obj = blocked_gibbs(self.param, S_mode, i, self.num_chains, self.accepted, self.num_y_pixels_per_block, self.num_x_pixels_per_block, self.percent)
                
                self.param, S_mode, self.accepted = bgs_obj.blocked_gibbs_sampler()
                
            # Define the updated parameters            
            updated_Z = self.param[4]
            
            updated_centres = self.param[6]
            
            # Outside the if/else statement, within the for-loop
            # Append the current sample and current chain into our sample storage vectors!
            self.Z_sample = np.column_stack((self.Z_sample, updated_Z))
            #S_sample = np.append(S_sample, updated_S)
            #centres_sample = np.append(centres_sample, updated_centres)
            
            # This would print out image every chain. We disabled this temporarily.
            #-------------------------------------------------------------------------------------------
            #Ellipse = np.array([])
            #for s in range(S_mode.shape[0]):
                
            #    info = S_mode[s]
                
            #    centre = updated_centres[s]
    
            #    #not as the mpl.patches.Ellipse document said. It should be (xy, minor axis (y), major axis (x))
            #    ell = mpl.patches.Ellipse((centre[0], centre[1]), info[1], info[0], 90 + abs(math.degrees(info[2])), color='green', fill = False)
                
            #    Ellipse = np.append(Ellipse, ell)
    
            #ellipse_obj = results_analyses(Ellipse, self.param[1].shape, self.param[1])
            
            #ellipse_obj.plot_ellipse()
            #-------------------------------------------------------------------------------------------
        
        # After the hybrid Gibbs, we execute Step 2 and train it again
        # List of parameters for the Gibbs
        #param = [imdata, upd_imdata, GridPoints, pixel_indices, Z [4], S [5], centres, 
        #         beta_d [7], M, grid_points_array [9], log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, object_center_tree [12], 
        #         MAX, 'binning', 0, 0, nearest_object_distance [17], min_semi_axis, max_semi_axis]
        upd_imdata = self.param[1]
        updated_S = self.param[5]
        pixel_indices = self.param[3]
        min_semi_axis = self.param[18]
        max_semi_axis = self.param[19]
        log_normalized_fg_prob_vector = self.param[10]
        log_normalized_bg_prob_vector = self.param[11]
        mask_set = self.param[15]
        
        accepted = np.array([0,0,0, 0] * updated_S.shape[0]).reshape((updated_S.shape[0], 4))
        
        # S_mode [:, 3:6] stores log_shape_probability/likelihood of the existing shapes, hence should not be modified.
        # Hence S_mode from Step_2 should be passed back into final run of Step 2 as it is.
        
        # However, the updated_S [:, 3:6] which represents the S.D. should be reset to 1.
        updated_S[:, 3:6] = 1
        rerun_iter_num = int(self.num_chains * 0.5)
        
        for nc in range(rerun_iter_num):
            updated_S, S_mode, accepted = step2_shape_likelihood(updated_Z, updated_S, S_mode, upd_imdata, updated_centres, pixel_indices, min_semi_axis, max_semi_axis, 
                                                                                nc, rerun_iter_num, accepted, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, mask_set).step2_prob()
        
        # Update the Shapes parameters
        self.param[5] = updated_S

        
        #We imprint the Ellipse shape on the original image and save it as .jpeg.
        #-------------------------------------------------------------------------------------------
        Ellipse = np.array([])
        for s in range(S_mode.shape[0]):
                
            info = S_mode[s]
                
            centre = updated_centres[s]
    
            #not as the mpl.patches.Ellipse document said. It should be (xy, minor axis (y), major axis (x))
            ell = mpl.patches.Ellipse((centre[0], centre[1]), info[1], info[0], 90 + abs(math.degrees(info[2])), color='green', lw = 3, fill = False)
                
            Ellipse = np.append(Ellipse, ell)
                
        # This will not plot Ellipse, since we disabled it, only save.    
        results_analyses(Ellipse, self.param[1].shape, self.param[1], display=False).plot_ellipse()

        #-------------------------------------------------------------------------------------------
        
        #return statement
        return (self.param, self.Z_sample, S_mode, self.accepted)