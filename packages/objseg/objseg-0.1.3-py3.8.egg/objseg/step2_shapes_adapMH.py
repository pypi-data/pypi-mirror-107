# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:21:32 2020

@author: hinsm
"""

#from shapes_functions import shapes_coordinates, shapes_intensities, shapes_likelihood_class, transform_dist
import numpy as np
import math
import matplotlib as mpl
from cellseg.results_analyses import results_analyses


import objseg.shapes as shapes
from objseg.step2_functions import mh
from objseg.box import find_indices_in_box, box_indices_to_coordinates



class step2_shape_likelihood:
    
    def __init__(self, Z, S, S_mode, upd_imdata, object_center_array, pixel_indices, min_semi_axis, max_semi_axis, current_chain_num, num_chains, accepted, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, mask_set):
        self.Z = Z
        self.S = S
        self.S_mode = S_mode
        self.upd_imdata = upd_imdata
        self.object_center_array = object_center_array
        self.pixel_indices = pixel_indices
        self.min_semi_axis = min_semi_axis
        self.max_semi_axis = max_semi_axis
        self.current_chain_num = current_chain_num
        self.num_chains = num_chains
        self.accepted = accepted
        self.log_normalized_fg_prob_vector = log_normalized_fg_prob_vector
        self.log_normalized_bg_prob_vector = log_normalized_bg_prob_vector
        self.mask_set = mask_set
    
    def step2_prob(self):
        
        pixel_indices_vector = self.pixel_indices.reshape((self.pixel_indices.size,))

        rnorm = np.random.normal
        uniform = np.random.uniform
        
        N = np.sum(self.Z)
        #just_S, new_S = self.S[:, :-1], np.array([0,0,0])
        
        #S_456 = np.empty((N, 3))
        jrange = 100
        
        print("Beginning Step 2.")
        
        for n in range(N):
            #print("Step 2:" + str((n/N)*100) + "% completed.")
            current_coord = self.object_center_array[n]
            
            box_region_indices_array = find_indices_in_box(current_coord, self.max_semi_axis, self.pixel_indices)
            
            coords = box_indices_to_coordinates(current_coord, self.max_semi_axis, self.pixel_indices)
            
            box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector = coords[0], coords[1]

            combined_indices_in_S = shapes.check_indices_in_existing_shapes(box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector , box_region_indices_array, self.pixel_indices, self.object_center_array, self.S)
            
            #self.S, self.S_mode, self.accepted = mh(jrange, n, self.accepted, self.S, self.S_mode, combined_indices_in_S, self.log_normalized_fg_prob_vector, self.log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, self.pixel_indices, pixel_indices_vector, current_coord)
            

            for j in range(jrange):
                # Substep 0: 
                #validation_obj = shapes_validation(S[n], min_semi_axis, max_semi_axis)
                #major_axis_minimum, major_axis_maximum, minor_axis_minimum, minor_axis_maximum, min_rad, max_rad = validation_obj.comparison()
                proposal_ra = min(self.max_semi_axis, max(self.min_semi_axis, rnorm(self.S[n, 0], self.S[n, 4] ))) # lambda_ra = S[n, 4]
                
                proposal_rb = min(self.max_semi_axis, max(self.min_semi_axis, rnorm(self.S[n, 1], self.S[n, 5] ))) # lambda_rb = S[n, 5]
            
                proposal_p = min(math.pi, max(-math.pi, rnorm(self.S[n, 2], self.S[n, 6] ))) # lambda_p  S[n, 6]
                    
                #print("eps_ra: " + str(eps_ra))
                    
                # Substep 1. Proposing random walk shape_sample for each shape parameter independently
                proposed_shape_sample_ra = np.array([ proposal_ra, self.S[n, 1], self.S[n, 2]]) #propose for major axis
                proposed_shape_sample_rb = np.array([self.S[n, 0], proposal_rb,  self.S[n, 2]]) #propose for minor axis
                proposed_shape_sample_p = np.array([ self.S[n, 0], self.S[n, 1], proposal_p]) #propose for rotational angle

        
                processed_shape_sample_ra = np.array([proposed_shape_sample_ra[0] / 2 + 0.00001, proposed_shape_sample_ra[1] / 2 + 0.00001, math.sin(proposed_shape_sample_ra[2]), math.cos(proposed_shape_sample_ra[2])])
                processed_shape_sample_rb = np.array([proposed_shape_sample_rb[0] / 2 + 0.00001, proposed_shape_sample_rb[1] / 2 + 0.00001, math.sin(proposed_shape_sample_rb[2]), math.cos(proposed_shape_sample_rb[2])])
                processed_shape_sample_p = np.array([proposed_shape_sample_p[0] / 2 + 0.00001, proposed_shape_sample_p[1] / 2 + 0.00001, math.sin(proposed_shape_sample_p[2]), math.cos(proposed_shape_sample_p[2])])

            
                # Substep 2: Compute log appearance likelihood for each proposal (in our newest modification, this would be our log posterior with proposed value)
                #------------------------------------------------------------------------------------------------------------------
                proposed_log_shape_prob_ra = shapes.log_data_likelihood(combined_indices_in_S, self.log_normalized_fg_prob_vector, self.log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, self.pixel_indices, pixel_indices_vector, current_coord, proposed_shape_sample_ra, processed_shape_sample_ra, self.mask_set)
                proposed_log_shape_prob_rb = shapes.log_data_likelihood(combined_indices_in_S, self.log_normalized_fg_prob_vector, self.log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, self.pixel_indices, pixel_indices_vector, current_coord, proposed_shape_sample_rb, processed_shape_sample_rb, self.mask_set)
                proposed_log_shape_prob_p = shapes.log_data_likelihood(combined_indices_in_S, self.log_normalized_fg_prob_vector, self.log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, self.pixel_indices, pixel_indices_vector, current_coord, proposed_shape_sample_p, processed_shape_sample_p, self.mask_set)
                    
                #------------------------------------------------------------------------------------------------------------------
                # Substep 3: Compute log shape prior
                #sp_ma = sp_mb = 1 / (max_semi_axis - min_semi_axis)
                #sp_p = 1 / (2*math.pi)
                        
                # Substep 5: Log-acceptance rate
                #if j == 0:
                current_log_shape_prob_ra = self.S_mode[n, 4]
                current_log_shape_prob_rb = self.S_mode[n, 5]
                current_log_shape_prob_p = self.S_mode[n, 6]
                
                # This is more sensible, but it always leads to reject since alpha >> 1.
                alpha_ra = proposed_log_shape_prob_ra - current_log_shape_prob_ra
                alpha_rb = proposed_log_shape_prob_rb - current_log_shape_prob_rb
                alpha_p = proposed_log_shape_prob_p - current_log_shape_prob_p
                
                #print("alpha_ra: " + str(alpha_ra))

                # As long as we hit jrange, we will add one. This is just to keep track whether it has been deleted or added at all.
                # It keeps the tuning precise and accurate.
                self.accepted[n, 3] += 1

                # Substep 6: Sample a random uniform variate
                u_ra = uniform(0, 1)
                
                # Substep 7: Test proposed value
                #if np.log(u) < alpha:
                if np.log(u_ra) < alpha_ra:
                    # Accept and officially updating the accepted "shape sample" and "posterior prob"
                    self.S_mode[n, 4] = proposed_log_shape_prob_ra
                    
                    self.S_mode[n, 0] = self.S[n, 0] = proposal_ra
                    
                    self.accepted[n, 0] += 1
            
                u_rb = uniform(0, 1)
                if np.log(u_rb) < alpha_rb:
                    
                    self.S_mode[n, 5] = proposed_log_shape_prob_rb
                    
                    self.S_mode[n, 1] = self.S[n, 1] = proposal_rb
                        
                    self.accepted[n, 1] += 1   
                    #print("r_b: accepted")

                u_p = uniform(0, 1)
                if np.log(u_p) < alpha_p:
                    
                    self.S_mode[n, 6] = proposed_log_shape_prob_p
                        
                    self.S_mode[n, 2] = self.S[n, 2] = proposal_p
                        
                    self.accepted[n, 2] += 1     
                    #print("p: accepted")   
            
            print(self.accepted)
            
            # Set tuning parameters (hardset for now, can be modified to user-choice later)
            tune_interval = 50
            tune_for = self.num_chains / 2
            
            # Tune every 50 iterations (tune for the first half)
            if self.num_chains > self.current_chain_num and (self.current_chain_num < tune_for):
                
                if (not (self.current_chain_num + 1) % tune_interval):
        
                    # Calculate aceptance rate
                    if self.accepted[n, 3] >= tune_interval:
                        acceptance_rate_ra = (1. * self.accepted[n, 0]) / self.accepted[n, 3]
                        acceptance_rate_rb = (1. * self.accepted[n, 1]) / self.accepted[n, 3]
                        acceptance_rate_p = (1. * self.accepted[n, 2]) / self.accepted[n, 3]
                    
                        # Major axis
                        if acceptance_rate_ra < 0.1:
                            self.S[n, 4] *= 0.9
                        
                        elif acceptance_rate_ra < 0.2:
                            self.S[n, 4] *= 0.95
                        
                        elif acceptance_rate_ra > 0.4:
                            self.S[n, 4] *= 1.05
                        
                        elif acceptance_rate_ra > 0.6:
                            self.S[n, 4] *= 1.1
                      
                        # Minor axis
                        if acceptance_rate_rb < 0.1:
                            self.S[n, 5] *= 0.9

                        elif acceptance_rate_rb < 0.2:
                            self.S[n, 5] *= 0.95
                        
                        elif acceptance_rate_rb > 0.4:
                            self.S[n, 5] *= 1.05
                            
                        elif acceptance_rate_rb > 0.6:
                            self.S[n, 5] *= 1.1
                                
                        # Rotational Angle
                        if acceptance_rate_p < 0.1:
                            self.S[n, 6] *= 0.9
        
                        elif acceptance_rate_p < 0.2:
                            self.S[n, 4] *= 0.95
                        
                        elif acceptance_rate_p > 0.4:
                            self.S[n, 6] *= 1.05
                        
                        elif acceptance_rate_p > 0.6:
                            self.S[n, 6] *= 1.1
        
                        self.accepted = np.array([0,0,0, 0] * self.S.shape[0]).reshape((self.S.shape[0], 4))
                
        print("Step 2 is complete.")
        
        Ellipse = np.array([])
        for s in range(self.S_mode.shape[0]):
                
            info = self.S_mode[s]
                
            centre = self.object_center_array[s]
    
            #not as the mpl.patches.Ellipse document said. It should be (xy, minor axis (y), major axis (x))
            ell = mpl.patches.Ellipse((centre[0], centre[1]), info[1], info[0], 90 + abs(math.degrees(info[2])), color='green', lw = 3, fill = False)
                
            Ellipse = np.append(Ellipse, ell)
                
        # This will not plot Ellipse, since we disabled it, only save.    
        results_analyses(Ellipse, self.upd_imdata.shape, self.upd_imdata, display=True).plot_ellipse()

        
        return (self.S, self.S_mode, self.accepted)
        