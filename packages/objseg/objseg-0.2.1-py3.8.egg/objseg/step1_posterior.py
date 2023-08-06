# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:21:32 2020

@author: hinsm
"""


import numpy as np
#from numba import njit


import objseg.shapes as shapes
from objseg.priors import priors
from objseg.box import box_indices_to_coordinates, find_indices_in_box
from objseg.object_center_position_search import oc_pos_search
from objseg.step1_functions import logsumexp, generate_shapes_sample_array
from objseg.rtree_functions import insert, remove


def current_zd_1_calculations(log_prior_same, log_prior_less, combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, pixel_indices_vector, current_coord, object_center_array_less, shapes_array_less, pos, mask_set):
                    
    combined_indices_in_shapes_less = shapes.check_indices_in_existing_shapes(box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, box_region_indices_array, pixel_indices, object_center_array_less, shapes_array_less)
                    
    log_likelihood_less = shapes.same_state_log_likelihood(combined_indices_in_shapes_less, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, pixel_indices_vector, mask_set)

    # --------- I.1.2 Calculating same state log likelihood
    log_likelihood_same = shapes.same_state_log_likelihood(combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, pixel_indices_vector, mask_set)
                        
    # I.2 Calculating Posteriors 
    log_joint_same = log_prior_same + log_likelihood_same
                    
    log_joint_less = log_prior_less + log_likelihood_less
    
    return log_joint_same, log_joint_less



def current_zd_0_calculations(num, log_prior_greater, log_prior_same, combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, pixel_indices_vector, current_coord, min_semi_axis, max_semi_axis, mask_set):

    # II.1 Calculating Log Likelihood
    # --------- II.1.01 Sample 300 shapes from shape_prior (three columns for maj,min axis and angle + 1 column for likelihood)
    shapes_sample_array = generate_shapes_sample_array(min_semi_axis, max_semi_axis, num)

    # --------- II.1.02 Calculate the likelihood for 300 shapes sample. Return as an array.
    shapes_sample_log_likelihood_array = shapes.shapes_sample_log_likelihood(num, combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, current_coord, shapes_sample_array, mask_set)
    
    # --------- II.1.03  Sum the 300 likelihood and divide by 300. (Averaging). This is the integral.
    log_likelihood_greater = np.mean(shapes_sample_log_likelihood_array)
    
    # --------- II.1.04 For "same state" with no object center, calculate the same state log likelihood.
    log_likelihood_same = shapes.same_state_log_likelihood(combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, pixel_indices_vector, mask_set)
    
    # II.2 Calculating Posteriors
    log_joint_greater = log_prior_greater + log_likelihood_greater
                    
    log_joint_same = log_prior_same + log_likelihood_same
    
    return log_joint_greater, log_joint_same, log_likelihood_greater, shapes_sample_log_likelihood_array, shapes_sample_array



class step1_posterior:

    def __init__(self, param, S_mode, current_chain_num, accepted, pixels_to_skip=None):
        self.param = param
        self.S_mode = S_mode
        self.current_chain_num = current_chain_num
        self.accepted = accepted
        self.pixels_to_skip = pixels_to_skip
     

    def step1_prob(self):
        
        # Ground truth. Parameters that never changes.
        upd_imdata = self.param[1]
        pixel_indices = self.param[3]
        M, grid_points_array = self.param[8], self.param[9]
        min_semi_axis, max_semi_axis = self.param[18], self.param[19]
        log_normalized_fg_prob_vector, log_normalized_bg_prob_vector = self.param[10], self.param[11]
        object_center_tree = self.param[12]
        log_p_R_option = self.param[16]
        
        # Below parameters get updated at every chain/iteration
        Z = self.param[4]
        S = self.param[5]
        object_center_array = self.param[6]
        beta_d, nearest_object_distance = self.param[7], self.param[17]
        GridPoints = self.param[2]
        mask_set = self.param[15]
        
        #--------------------------------------------------------------------------
        # 0. Pre-Processing
        #--------------------------------------------------------------------------
        pi_reshaped = pixel_indices.reshape((pixel_indices.size, 1))
        master_Z = np.column_stack((Z, pi_reshaped))
        D = Z.shape[0]
        max_x = upd_imdata.shape[1]
        max_y = upd_imdata.shape[0]
        img_shape = upd_imdata.shape
        pixel_indices_vector = pixel_indices.reshape((pixel_indices.size,))
        
        #--------------------------------------------------------------------------
        # I. Scan through each pixel 
        #--------------------------------------------------------------------------
        for d in range(D):
            #print(d)
            
            # Below condition is activated automatically if pixels_to_skip is array, meaning this is a BLOCKED GIBBS SCAN.
            if type(self.pixels_to_skip) == type(upd_imdata):
                
                if d in self.pixels_to_skip:
                    
                    continue
                   
            # Below is the condition for probabilistically deciding whether or not to analyze pixel that has a higher background probability   
            if log_normalized_bg_prob_vector[d] > log_normalized_fg_prob_vector[d]:
                
                x_disc = np.array([0, 1])
                    
                prob = np.array([log_normalized_bg_prob_vector[d], log_normalized_fg_prob_vector[d]])
                                    
                decision = np.random.choice(x_disc, 1, p = prob)[0]
                
                if decision == 0:
                    
                    continue

            #if bool(km_label[d, 0] == 1) is True:
            current_zd =  master_Z[d, 0]
            
            current_pix = master_Z[d, 1]
            
            current_coord = np.argwhere(pixel_indices == current_pix)[0]
            
            current_coord[[0,1]] = current_coord[[1,0]]  # (y,x) convert to (x,y)
            #-----------------------------------------------------------------------------------------------------------------------------------------------
            #same_state_ll = whole_likelihood(S).model()
            # safety catch when Step 1 is run by blocked gibbs
            if object_center_array.size == 0:

                object_center_array = np.array([[int(max_x / 2), int(max_y / 2)]]) #[x midpoint of image, y midpoint of image]
            
            # Object Center == 1  ("Same state" and "Less state")
            else:
                #np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)       
                
                box_region_indices_array = find_indices_in_box(current_coord, max_semi_axis, pixel_indices)
                
                coords = box_indices_to_coordinates(current_coord, max_semi_axis, pixel_indices)
                
                box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector = coords[0], coords[1]
                
                combined_indices_in_shapes = shapes.check_indices_in_existing_shapes(box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, box_region_indices_array, pixel_indices, object_center_array, S)
                
                print("Current chain number: " + str(self.current_chain_num) + "; current pixel number is: " + str(d))
                
                
                if current_zd == 1:
                    
                    # I.0 Calculating Log Prior Probabilities
                    log_prior_same = priors(1, current_zd, current_coord, current_pix, D, img_shape, beta_d, M, grid_points_array, object_center_array, object_center_tree, GridPoints, log_p_R_option).cprob_z_R()
                
                    log_prior_less = priors(0, current_zd, current_coord, current_pix, D, img_shape, beta_d, M, grid_points_array, object_center_array, object_center_tree, GridPoints, log_p_R_option).cprob_z_R()
                    
                    # I.1 Calculating Log Likelihood
                    # --------- I.1.1 Less State (whole likelihood excluding current shape)
                    pos = oc_pos_search(object_center_array, current_coord)
                    
                    shapes_array_less = np.delete(S, pos, 0)
                    
                    object_center_array_less = np.delete(object_center_array, pos, 0)
                
                    log_joint_same, log_joint_less = current_zd_1_calculations(log_prior_same, log_prior_less, combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, 
                                                                                       box_region_indices_array, box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, pixel_indices, pixel_indices_vector, 
                                                                                       current_coord, object_center_array_less, shapes_array_less, pos, mask_set)
                    
                    # (I.3) Object Center >= 2 ("Same state" and "Less state") 
                    # (THIS PART IS FROZEN! WE WILL COME BACK TO IT LATER ON WHEN WE ADVANCE OUR CODE!!!)

                if current_zd == 0:
                    
                    # II.0 Calculating Log Prior Probabilities
                    log_prior_same = priors(0, 0, current_coord, current_pix, D, img_shape, beta_d, M, grid_points_array, object_center_array, object_center_tree, GridPoints, log_p_R_option).cprob_z_R()
                    
                    log_prior_greater = priors(1, 0, current_coord, current_pix, D, img_shape, beta_d, M, grid_points_array, object_center_array, object_center_tree, GridPoints, log_p_R_option).cprob_z_R()
                    
                    
                    if self.current_chain_num < 100:
                        num = 10
                        
                    elif self.current_chain_num >= 100:
                        num = 300
                        
                    log_joint_greater, log_joint_same, log_likelihood_greater, shapes_sample_log_likelihood_array, shapes_sample_array = current_zd_0_calculations(num, log_prior_greater, log_prior_same, 
                                                                                                                                                                           combined_indices_in_shapes, log_normalized_fg_prob_vector, 
                                                                                                                                                                           log_normalized_bg_prob_vector, box_region_indices_array, 
                                                                                                                                                                           box_indices_coordinates_y0_vector, box_indices_coordinates_x0_vector, 
                                                                                                                                                                           pixel_indices, pixel_indices_vector, current_coord, min_semi_axis, 
                                                                                                                                                                           max_semi_axis, mask_set)
                    #log_posterior_greater, log_posterior_same = current_zd_0_calculations2(d, log_prior_greater, log_prior_same, shapes_sample_array, log_likelihood_greater_array, combined_indices_in_shapes, log_normalized_fg_prob_vector, log_normalized_bg_prob_vector, box_region_indices_array, pixel_indices_vector)
                    
                    
                # Create a discrete probability distribution; sample a new z_k value; Normalize the probabilities
                if current_zd == 0:
                    
                    x_disc = np.array([0, 1])
                    
                    log_joint_vec = np.array([float(log_joint_same), float(log_joint_greater)])
                    
                    log_posterior_vec = np.exp(log_joint_vec - logsumexp(log_joint_vec))
                    
                    #print(p_disc)
                    
                if current_zd == 1: 
                    
                    x_disc = np.array([0, 1])
                    
                    log_joint_vec = np.array([float(log_joint_less), float(log_joint_same)])
                    
                    log_posterior_vec = np.exp(log_joint_vec - logsumexp(log_joint_vec))
                    
    
                #else:
                #    x_disc = np.array([current_zd - 1, current_zd, current_zd + 1])
                
                new_zd = np.random.choice(x_disc, 1, p = log_posterior_vec)[0]
                
                #  Addition of a point (if k = k^t + 1)
                if new_zd == current_zd + 1:
                    
                    # Updated Z matrix at current pixel, set to 1
                    master_Z[d, 0] = 1
                    
                    # Add current coordinate to object center array
                    object_center_array = np.row_stack((object_center_array, current_coord))
                    
                    # Add current coordinate to object center tree
                    insert(GridPoints, current_pix, current_coord, object_center_tree)
                    #object_center_tree.insert(current_pix, [x0, y0, x0 + 1, y0 + 1], tuple(current_coord))

                    #maj_axis_max, min_axis_max = s_n1[0], s_n1[1]
                    # V.1.01 Normalize the likelihood column from shapes sample array.
                    
                    if num != 1:
                        
                        # Classical Method
                        likelihood_x = np.arange(0, num, 1)
                        likelihood_p = np.exp(shapes_sample_log_likelihood_array - logsumexp(shapes_sample_log_likelihood_array))
                    
                        #[0] is to do dimension reduction.
                        likelihood_p = likelihood_p.reshape((1, likelihood_p.shape[0]))[0]
                        
                        # V.2.02 Sample a shape parameter from it.
                        new_ss_index = np.random.choice(likelihood_x, 1, p = likelihood_p)[0]
                    
                        new_shape_sample = shapes_sample_array[new_ss_index]
                        
                    
                    else:
                        
                        new_shape_sample = shapes_sample_array[0]
                        #new_shape_sample = generate_shapes_sample_array(min_semi_axis, max_semi_axis, 1)[0]
                    
                    # V.2.03 Append [current_pix_index, 1,1,1] (used in Step 2) to the shape parameters vector.
                    new_S_sample = np.concatenate((new_shape_sample, np.array([current_pix, 1, 1, 1])))
                    new_S_mode_sample = np.concatenate((new_shape_sample, np.array([current_pix, log_likelihood_greater, log_likelihood_greater, log_likelihood_greater])))
                    
                    # V.2.04 Append to S.
                    S = np.row_stack((S, new_S_sample))
                    
                    # V.2.05 Append to S_mode.
                    #s_mode_n1 = np.append(s_n1[0:4], np.array([1,1,1]))
                    self.S_mode = np.row_stack((self.S_mode, new_S_mode_sample))
                    
                    self.accepted = np.row_stack((self.accepted, [0,0,0, 0]))
                    
                # Deletion of a point (if k < k^t)
                elif new_zd < current_zd:
                    
                    if object_center_array.shape[0] > 1:
                    
                        # Updated Z matrix at current pixel, set to 0
                        master_Z[d, 0] = 0
                    
                        # Delete current coordinate from object center array
                        object_center_array = object_center_array_less
                    
                        # Delete current coordinate from object center tree
                        remove(GridPoints, current_pix, current_coord, object_center_tree)
                        #object_center_tree.delete(current_pix, [x0, y0, x0 + 1, y0 + 1])

                        # Remove shapes from S, just use shapes array less
                        S = shapes_array_less
                    
                        # Remove shapes from S_mode    
                        self.S_mode = np.delete(self.S_mode, pos, 0)
                        
                        self.accepted = np.delete(self.accepted, pos, 0)
                
                print("Updated number of object centers:" + str(np.sum(master_Z[:,0])))

        #--------------------------------------------------------------------------
        # III. UPDATE INFO and RETURN UPDATED RESULTS!
        #--------------------------------------------------------------------------
        Z = master_Z[:,0].reshape((D,1))
        
        return(Z, S, object_center_array, nearest_object_distance, object_center_tree, self.S_mode, self.accepted)



    