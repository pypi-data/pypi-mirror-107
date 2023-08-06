# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:33:15 2020

@author: hinsm
"""

#from line_profiler import LineProfiler
import math
import numpy as np
from rtree import index
from numba import njit, prange


from objseg.rtree_functions import test_do_nothing, test_insert, test_remove
from objseg.object_center_position_search import oc_pos_search
from objseg.step1_functions import logsumexp


#@numba.njit(cache=True)
def rtree(grid_points_array, object_center_array, pixel_indices, img_shape):
    
    #Convert to tuples
    oc = [tuple(row) for row in object_center_array]
        
    # Create an index
    idx = index.Rtree()
        
    # Add points to tree
    for j,k in enumerate(oc):

        #print(pixel_indices[oc[j][1], oc[j][0]])
        y0 = oc[j][1]
        x0 = oc[j][0]
        
        # insert(id_unique (use pixel_indices), coordinates = [min_x, min_y, max_x , max_y], obj_center = (50,50))
        idx.insert(pixel_indices[y0, x0], [x0, y0, x0 + 1, y0 + 1], k)

    return idx

#@njit(parallel=True)
def rtree_nearest(object_center_tree, M, grid_points_array, nearest_object_distance_array):
    
    for gp in prange(M):
        
        # Find 1-nearest object ([0] at the end to reduce unncessary dimension)
        tup = tuple(grid_points_array[gp])
        
        ref = list(object_center_tree.nearest(tup, 1, objects = 'raw'))[0]
        
        ref = np.asarray(ref)
        
        # Compute the distance and add to nearest_object_distance array (TO BE FIXED)
        nearest_object_distance_array[gp] = np.linalg.norm(grid_points_array[gp] - ref)

    return nearest_object_distance_array


@njit(cache = True, parallel=True)
def pgd_sub_func(current_coord_array, grid_points_array):
    
    diff = current_coord_array - grid_points_array
    
    point_to_grid_distance = np.empty((diff.shape[0], 1), dtype = np.float64)
    
    for i in prange(diff.shape[0]):
        
        point_to_grid_distance[i] = np.linalg.norm(diff[i], ord = None)
    
    point_to_grid_distance = point_to_grid_distance.reshape((diff.shape[0], 1))
    
    return point_to_grid_distance


@njit(cache = True, parallel = True, fastmath = True)
def power(base_vertical_vector, exponent_horizontal_vector):
    
    # Sokn 1:
    #exp_nod_squared_exp_beta_d1 = exp_nod_squared ** proportion_beta_vector
    #print(exp_nod_squared_exp_beta_d1)
    
    # Soln 2: 
    #exp_nod_squared_exp_beta_d2 = np.power(exp_nod_squared, proportion_beta_vector)
    #print(exp_nod_squared_exp_beta_d2)
    
    # Soln 3: 
    base_vertical_vector_repeats = np.repeat(base_vertical_vector, exponent_horizontal_vector.size)
    
    base_vertical_vector_repeats = base_vertical_vector_repeats.reshape((base_vertical_vector.size, exponent_horizontal_vector.size))

    exponent_horizontal_vector_repeats = np.ones((base_vertical_vector.size, 1))*exponent_horizontal_vector
    
    powered_matrix = base_vertical_vector_repeats ** exponent_horizontal_vector_repeats
   
    return powered_matrix



@njit(cache = True, fastmath = True)
def likelihood_R_inhomogeneous(nearest_object_distance_array, D, img_shape0, img_shape1, beta_d):

    #beta_matrix = beta_d.reshape((img_shape0, img_shape1))
    #img_size = img_shape[0] * img_shape[1]
    nearest_object_distance_array = nearest_object_distance_array.reshape((nearest_object_distance_array.shape[0], 1))

    proportion_beta_vector = (2 * math.pi * beta_d / D).reshape((1, D))
    
    neg_pi_nod_squared = - math.pi * nearest_object_distance_array * nearest_object_distance_array
    
    exp_neg_pi_nod_squared_beta_d = np.exp(neg_pi_nod_squared * beta_d)
    
    exp_neg_pi_nod_squared_beta_d_transposed = exp_neg_pi_nod_squared_beta_d.T
    
    sum_log_sum = np.sum(np.log(np.dot(proportion_beta_vector, exp_neg_pi_nod_squared_beta_d_transposed)))
    
    sum_log_nodarr = np.sum(np.log(nearest_object_distance_array + 0.000001))
    
    return sum_log_sum + sum_log_nodarr




class priors:
    
    def __init__(self, new_zd, current_zd, current_coord, current_pix, D, img_shape, beta_d, M, grid_points_array, object_center_array, object_center_tree, GridPoints, log_p_R_option):
        
        self.new_zd = new_zd
        self.current_zd = current_zd
        self.current_coord = current_coord
        self.current_pix = current_pix
        self.D = D
        self.img_shape = img_shape
        self.beta_d = beta_d
        self.M = M
        self.grid_points_array = grid_points_array
        self.object_center_array = object_center_array
        self.object_center_tree = object_center_tree
        self.GridPoints = GridPoints
        self.log_p_R_option = log_p_R_option
    
    #STATIC METHOD
    @staticmethod
    def likelihood_R_homogeneous(nod_input, beta):
        
    # Calculating log distance likelihood p(R) (assuming a homogeneous case)
        nod_input = nod_input + 0.000001
        
        M = nod_input.shape[0]
        
        log_p_of_R = M * np.log(2 * np.pi * beta) + (-np.pi * beta * np.sum(nod_input**2) ) + np.sum(np.log(nod_input))
        
        #p_of_R = (2 * np.pi * beta)**M * np.exp(-np.pi * beta * np.sum(nod_input**2)) * np.prod(nod_input)
        
        return log_p_of_R

    @staticmethod
    def likelihood_R(nearest_object_distance_array, D, img_shape, beta_d, option="inhomo"):
        
        if option == "inhomo":
            
            log_p_R = likelihood_R_inhomogeneous(nearest_object_distance_array, D, img_shape[0], img_shape[1], beta_d)
            
        elif option == "homo":
            
            log_p_R = priors.likelihood_R_homogeneous(nearest_object_distance_array, beta_d)
            
        return log_p_R
        
    ###############################################################################
    ###############################################################################    
    
    #@numba.njit(cache=True)
    def cprob_R(self):
        #beta_d = beta_d[d]
        # z_d_coord is in object_center_array (which means the truth z_d > 0):
        # format: current_coord = array([0,0])
        #N = self.object_center_array.shape[0]
        #x0 = self.current_coord[0]
        #y0 = self.current_coord[1]
    
        # z_d_coord is not in object_center_array (which means the truth z_d = 0):
        pos = oc_pos_search(self.object_center_array, self.current_coord)
        
        # Case 1: Where current coordinate is not an object center
        if pos == 'No':
            
            # Calculate log(prob(R_0)) (for z_d = 0)
            nod = np.array(test_do_nothing(self.GridPoints))
            
            log_p_R_0 = priors.likelihood_R(nod, self.D, self.img_shape, self.beta_d, self.log_p_R_option)            
            
            #log_p_R_0 = priors.likelihood_R(nod, self.beta_d)
            
            # Calculate log(prob(R_not0)) (for z_d > 0)
            ### Add current coordinate to R-tree (object center tree)
            nod_not0 = np.array(test_insert(self.GridPoints, self.current_coord))
            
            log_p_R_not0 = priors.likelihood_R(nod_not0, self.D, self.img_shape, self.beta_d, self.log_p_R_option)

            #log_p_R_not0 = priors.likelihood_R(nod_not0, self.beta_d)

            ### Return the tuple for likelihood_R 
            if self.log_p_R_option == "inhomo":
                
                beta_d_scalar = self.beta_d[self.current_pix]
                
            elif self.log_p_R_option == "homo":
                
                beta_d_scalar = self.beta_d
                
            return (log_p_R_0, log_p_R_not0, beta_d_scalar)        

        # Case 2: where current coordinate is an object center
        else:
            
            # Calculate log(prob(R_not0)) (for z_d > 0)
            nod = np.array(test_do_nothing(self.GridPoints))
            
            log_p_R_not0 = priors.likelihood_R(nod, self.D, self.img_shape, self.beta_d, self.log_p_R_option)

            #log_p_R_not0 = priors.likelihood_R(nod, self.beta_d)

            # Calculate log(prob(R_0)) (for z_d = 0)
            ### Remove current coordinate from R-tree (object center tree)
            nod_0 = np.array(test_remove(self.GridPoints, self.current_coord, self.object_center_tree))
            
            log_p_R_0 = priors.likelihood_R(nod_0, self.D, self.img_shape, self.beta_d, self.log_p_R_option)

            #log_p_R_0 = priors.likelihood_R(nod_0, self.beta_d)

            ### Return the tuple for likelihood_R
            if self.log_p_R_option == "inhomo":
                
                beta_d_scalar = self.beta_d[self.current_pix]
                
            elif self.log_p_R_option == "homo":
                
                beta_d_scalar = self.beta_d
                
            return (log_p_R_0, log_p_R_not0, beta_d_scalar)      


    def H_prob(self, log_p_R_tuple):
        #beta_d = beta_d[d]
        k, k_t = self.new_zd, self.current_zd
        
        p_R_0, p_R_not0 = math.exp(log_p_R_tuple[0]), math.exp(log_p_R_tuple[1])
        beta_d = log_p_R_tuple[2]
    
        if k == 0 and k_t == 0 or k == 1 and k_t == 1:
            
            output = ( p_R_0 - p_R_not0 ) * math.exp(- beta_d) + p_R_not0
            
            #output = p_R_0 * math.exp(-log_p_R_tuple[2]) + p_R_not0 * (1 - math.exp(-log_p_R_tuple[2]))
            
        elif k == 0 and k_t == 1 or k == 1 and k_t == 0:
            
            output = ( p_R_0 - p_R_not0 ) * math.exp(- beta_d) + p_R_not0
            
            #output = p_R_0 * math.exp(-log_p_R_tuple[2]) + p_R_not0 * (1 - math.exp(-log_p_R_tuple[2]))
            
        return output
    
    ###############################################################################
    ###############################################################################

    #@numba.njit(cache=True)
    def cprob_z_R(self):
        #beta_d = beta_d[d]
        k = self.new_zd
        
        k_t = self.current_zd
        
        log_p_R_tuple = self.cprob_R()
        
        #print("log_p_R_tuple: " + str(log_p_R_tuple))
        
        H = priors.H_prob(self, log_p_R_tuple) + 0.000001
        
        #print("H: " + str(H))
        
        # This means "same state"
        if k == 0 and k_t == 0:
            
            output = log_p_R_tuple[0] - np.log(H) - log_p_R_tuple[2]
            #output = ( 1/H ) * p_R_tuple[1] * math.e**(-p_R_tuple[2])
            
        # This means "less state"
        elif k == 0 and k_t == 1:
            
            output = log_p_R_tuple[0] - np.log(H) - log_p_R_tuple[2]
            #output = ( 1/H ) * p_R_tuple[1] * math.e**(-p_R_tuple[3])
            
        #elif k > 0:
        # This means "greater state"
        elif k == 1 and k_t == 0:
            
            # Since there is a change of state, we have to use log_p_R_tuple[3] == updated beta_d
            output = log_p_R_tuple[1] - np.log(H) - log_p_R_tuple[2] + np.log(log_p_R_tuple[2]) 
            
            # Below is a general formula, to be used in future, when k can be >= 2
            #output = np.log(1/H) + log_p_R_tuple[1] - log_p_R_tuple[2] + ( k * np.log(log_p_R_tuple[2]) ) - np.log(math.factorial(k))
          
            
        # This means "same state"
        elif k == 1 and k_t == 1:
            
            output = log_p_R_tuple[1] - np.log(H) - log_p_R_tuple[2] + np.log(log_p_R_tuple[2])
            # Below is a general formula, to be used in future, when k can be >= 2
            #output = np.log(1/H) + log_p_R_tuple[1] - log_p_R_tuple[2] + ( k * np.log(log_p_R_tuple[2]) ) - np.log(math.factorial(k))
            
    
        #else:
        #    print("WARNING: k value is invalid.")
        return output
