# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:28:08 2020

@author: hinsm
"""

#from shapes_functions import shapes_coordinates, shapes_intensities
import numpy as np
from numba import njit, prange
import scipy.ndimage as ndimage
from PIL import Image
import matplotlib.pyplot as plt
from sklearn import mixture
import math
import cv2


import objseg.shapes as shapes
from objseg.rtree_functions import GridPoint
from objseg.box import box_indices_to_coordinates, find_indices_in_box
from objseg.priors import rtree
from objseg.step1_functions import logsumexp, get_normalized_p, generate_shapes_sample_array
from objseg.variational_mf import VMF_SGCP


class data_input:
    
    @staticmethod
    def convert_to_gray_scale(input_im, output_im):
        img = Image.open(input_im).convert('L')
        img.save(output_im)
        
class basic_statistics:

    # Attributes of the array
    #imdata.ndim #3 dimensional
    #imdata.shape #(243, 317, 3)
    #imdata.size #231093
    @staticmethod
    def image_attributes(imdata):
        ndim = imdata.ndim
        shape = imdata.shape
        dtype = imdata.dtype
        pixel_size = imdata.size
        print("The dimension of the image is", ndim, ". The shape of the data is", shape[0], "rows by ", shape[1], "columns. The type of the image is", dtype, ". The pixel size is", imdata.size, ".")
        return (ndim, shape, dtype, pixel_size)
    
    # Statistical Information #
    @staticmethod
    def statistics(imdata):
        mean = imdata.mean() #15.26968
        imax = imdata.max() #184
        imin = imdata.min() #0
        print("The mean value of image intensity is", mean, ". The max intensity value is", imax, "and the min intensity value is", imin, ".")
        return (mean, imax, imin)

class filtering:
        
    # STEP 2: FILTERING/DENOISING - using median filter #
    @staticmethod
    def median_filter(imdata, filter_param):
        noisy = imdata + 0.4 * imdata.std() + np.random.random(imdata.shape)
        med_denoised = ndimage.median_filter(noisy, filter_param)
        return med_denoised

class masking_class:
    
    @staticmethod
    def masking(med_denoised):
        
        #im = ndimage.gaussian_filter(im, sigma=1/(4.*n))
        mask = (med_denoised > med_denoised.mean()).astype(np.float)
        mask += 0.1 * med_denoised
        
        # Return a sample(s) from the "standard normal" distribution
        img = mask + 0.2*np.random.randn(*mask.shape)
        
        return img
        
class clustering:
    
    #STRICTLY FOR 3-dim
    @staticmethod
    def kmeans(processed_mask, K, attempts, print_bool, resize_bool):
        
        img = processed_mask
        #1.0 Preprocessing
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #vectorized = img.reshape((-1,3))
        
        #We will go through the initial preprocessing achieved in the above BGMM function
        #because it does seem to make the objects more clear/obvious.
        
        #im = ndimage.gaussian_filter(im, sigma=1/(4.*n))
        if resize_bool == True:
            X = img.reshape((img.size,1))
            X = np.float32(X)
        elif resize_bool == False:
            X = np.float32(img)
    
        #1.1 Defining criteria (type, max_iteration, epsilon)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 6.0)

        #1.2 Executing the k-means algorithm (ret = compactness, labels, centers)
        #Since K = 2 by default, we would have two centers.
        ret, label, center = cv2.kmeans(X, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)
        
        #1.3 Postprocessing
        #Changing the dtype for center to 'uint8'
        center = np.uint8(center)
        
        #Map the center (for each respective cluster) back to the label.
        #(label.shape[0] == res.shape[0])
        #res is a vectorized version too!
        res = center[label.flatten()]
        
        #1.4 Generating resulting image (this image is thresholded already)
        result_image = res.reshape((X.shape))
        
        if resize_bool == True:
            result_image = result_image.reshape((img.shape))
    
        #normalize the binary image
        #print(result_image)
        result_image = result_image/np.amax(result_image)
    
        if print_bool == True:
            #1.5 displaying original_image and result_image
            figure_size = 15
            plt.figure(figsize=(figure_size,figure_size))
            
            plt.subplot(1,2,1),plt.imshow(img)
            plt.title('Original Image'), plt.xticks([]), plt.yticks([])
            
            plt.subplot(1,2,2),plt.imshow(result_image)
            plt.title('Segmented Image when K = %i' % K), plt.xticks([]), plt.yticks([])
            plt.show()

        return (result_image, label, center)
        
class binarization:
    
    # STEP 4: Binarizing image  and denoising binary image #
    @staticmethod
    def binarize_image(imdata, threshold_bayes):
        binary_image = imdata > threshold_bayes
        return binary_image
    
class denoising:
    
    @staticmethod
    def denoise_image(bin_image):
        eroded_img = ndimage.binary_erosion(bin_image)
        reconstruct_img = ndimage.binary_propagation(eroded_img, mask = bin_image)
        tmp = np.logical_not(reconstruct_img)
        eroded_tmp = ndimage.binary_erosion(tmp)
        reconstruct_final = np.logical_not(ndimage.binary_propagation(eroded_tmp, mask=tmp))
        return reconstruct_final
        
class object_centre_search:
    
    # Edge detection, detecting objects, finding object center coordinates
    @staticmethod
    def object_centre(original_image, data, min_area_thresh, max_area_thresh, boolean):
    
        # Mandatory step for image to have correct data types for cv2.
        data = np.array(data, dtype='uint8')
        o_image = original_image

        # 1st = source_image (binary is better), 2nd = contour retrieval mode, 3rd = contour approx. method
        contours, _ = cv2.findContours(data, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #Finding Contours
        
        # Plot the contours (this does not draw the contours well)
        #image = cv2.drawContours(km_img, contours, -1, (0, 255, 0), 2)
        #plt.imshow(image)
        
        if boolean == True:
            print("No. of original recognized contours: {0}".format(len(contours))) #Finding No. Of Contours Detected i.e, No. of Shapes

        #finding center of the recognized shapes ===========================
        object_centres = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_area_thresh and area < max_area_thresh:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    center = (cx, cy)
                    object_centres.append(center)
                else:
                    cx, cy = 0, 0

                #print("Center coordinate: "+str(center))
                #radius = 3
                #cv2.circle(o_image, (cx,cy), radius, (0, 255, 255), -1)

        object_centres = np.array(object_centres)
        num_objects = object_centres.shape[0]
        
        if boolean == True:
            print("No. of original recognized shapes: {0}".format(num_objects))
            plt.imshow(o_image)
            if (object_centres.size != 0):
                plt.scatter(object_centres[:,0], object_centres[:,1], facecolor='red')
    
        return object_centres, num_objects
        
class plotting:
    
    # This function displays the plot without the axis.
    @staticmethod
    def plot_image(img, t_f_gray):
    
        if t_f_gray == True:
            plt.figure(figsize=(30,30))
            
            plt.subplot(131)
            plt.imshow(img, cmap=plt.cm.gray) # display image in gray scale
            plt.axis('off')
        elif t_f_gray == False:
            plt.figure(figsize=(30,30))
            
            plt.subplot(131)
            plt.imshow(img) # display image in RGB scale
            plt.axis('off')
        else:
            print("WARNING: Unexpected input!")

    #plot_image(rgb_image_with_grid_points, True)
        
class grid_points:

    # Defining grid points and selecting the coordinates (which pixel) are selected to be grid points
    #@numba.njit(cache=True)
    @staticmethod
    def set_grid_points(updated_img, pixels_away):
        
        divisor = pixels_away
        y_pixel, x_pixel = updated_img.shape
        
        if (y_pixel % divisor == 0 and x_pixel % divisor == 0):
            # If a pixel size is 250, then the indices goes from 0 to 249.
            # In that case, the first grid point is at 9, and the last one is 239.
            num_col = int((x_pixel / divisor) - 1)
            num_row = int((y_pixel / divisor) - 1)
            M = num_row * num_col
            
            # Since indices start at 0, if we want 10 indices, then 0+10-1 = 9, which means we get indices from 0~9 (there are 10 of them)
            starting_indice = 0 + divisor - 1 
            
            # Create two 1-dim lists, one is a list of vertical indices, and the other is horizontal indices
            vertical_indices = np.arange(starting_indice, y_pixel - 1, divisor) #an array
            horiz_indices = np.arange(starting_indice, x_pixel - 1, divisor) #an array
            #repeat = np.array(vertical_indices*len(horiz_indices))
            repeat = np.repeat(vertical_indices, len(horiz_indices))
            grid_points_coords_array = np.transpose([repeat, np.tile(horiz_indices, len(vertical_indices))])
            
            grid_points_coords_array[:,[0, 1]] = grid_points_coords_array[:,[1, 0]]
            return (M, grid_points_coords_array)

        else:
            print("WARNING: Your image pixels are not divisible by the number you set. Please use the update_pixel_divisibility function to update your image pixels first.")
            return (0,0)

class intensity:

    @staticmethod
    def label_to_intensity_histogram(img, km_label):
        
        km_label = km_label.reshape((img.shape))
        bg_y, bg_x = np.where(km_label == 0)
        fg_y, fg_x = np.where(km_label == 1)
        
        bg_intensity = img[bg_y, bg_x]
        fg_intensity = img[fg_y, fg_x]
        
        #plt.subplot(1, 2, 1)
        #plt.plot(bg_intensity)
        #plt.subplot(1, 2, 2)
        #plt.plot(fg_intensity)
        #plt.tight_layout()
        
        return (bg_intensity, fg_intensity)

class pixel_calculator:
        
    # Check for pixel size divisbility for blocking and defining grid points
    @staticmethod
    def update_pixel_divisibility(pixel_axis, divisor):
        if pixel_axis % divisor != 0:
            adj_axis = pixel_axis +  (divisor - pixel_axis %  divisor)
            return adj_axis
        elif pixel_axis %  divisor == 0:
            return pixel_axis


class image_pixel_expansion:
        
    # Change binary image from T/F to 1/0, expand pixel size using updated pixels, and fill them with zeros
    # BONUS: THIS FUNCTION WORKS FOR non binary / quantitative images too!!
    @staticmethod
    def update_image(img, adj_y_pixel, adj_x_pixel):
        img = 1*img
        ori_y_pixel, ori_x_pixel = img.shape[0], img.shape[1]
        r_s = (adj_y_pixel - ori_y_pixel, ori_x_pixel)
        c_s = (adj_y_pixel, adj_x_pixel - ori_x_pixel)
        
        if adj_y_pixel - ori_y_pixel != 0:
            # Expand y_pixel size first, by adding extra rows
            new_rows = np.zeros(r_s, dtype = img.dtype)
            #img = np.append(img, new_rows, axis = 0) # axis = 0 refers to rows
            img = np.vstack((img, new_rows))
    
        if adj_x_pixel - ori_x_pixel != 0:
            # Expand x_pixel size, by adding extra columns
            new_cols = np.zeros(c_s, dtype = img.dtype)
            #img = np.append(img, new_cols, axis = 1) # axis = 1 refers to columns
            img = np.hstack((img, new_cols))
            
        return img


def transform_centre_to_Z(centres, original_shape):
    
    Z = np.zeros(original_shape, dtype = 'uint8')

    if centres.ndim == 1:
        x, y = centres[0], centres[1]
        Z[y, x] = 1
    else:
        for c in range(centres.shape[0]):
            coords = centres[c]
            x, y = coords[0], coords[1]
            #print("x" + str(x) + " y" + str(y))
            Z[y, x] = 1
            #print("("+ str(y) + "," + str(x) + ")")
    
    # Vectorize Z
    Z = Z.reshape((original_shape[0]*original_shape[1],1))
    return Z

# Archived (as of Nov-03, 2020)
#@numba.njit(cache=True)
def probability_assignment(img_vector, label_vector, prob):

    element_prob_vector = np.empty((img_vector.size, 1))
    
    for e in range(img_vector.size):
        
        element_prob_vector[e] = prob[e, label_vector[e, 0]]
    
    return element_prob_vector

def intensity_probability(img_vector, n):
    
    # Declare a 3-component GMM
    gmm = mixture.GaussianMixture(n_components = n, covariance_type = "full")

    # Fit the data set using EM algorithm
    #fit = gmm.fit(img_vector)

    # Fit the data set and return the label
    label_vector = gmm.fit_predict(img_vector)
    
    # Predicting probability
    prob = gmm.predict_proba(img_vector)

    if n == 3:
        # In 3-n GMM, 1 = bg, 0 = bleed through (bt), and 2 = fg
        bg_prob_vector = prob[:, 1]
    
        fg_prob_vector = prob[:, 2]
        
        #modified_fg_prob_vector = fg_bt_adjustment(label_vector, prob)

    elif n == 2:
        
        bg_prob_vector = prob[:, 0]
        
        fg_prob_vector = prob[:, 1]

    return (fg_prob_vector, bg_prob_vector)


@njit(cache = True)
def fg_bt_adjustment(label_vector, mixture_3n_prob_matrix):
    
    modified_fg_prob_vector = np.zeros((label_vector.size,))

    prob = mixture_3n_prob_matrix
    
    for i in range(label_vector.size):
        
        if label_vector[i] == 2:
            
            modified_fg_prob_vector[i] = prob[i, 0] + prob[i, 2]
            
        elif label_vector[i] == 0:
            
            modified_fg_prob_vector[i] = prob[i, 2]
        
    return modified_fg_prob_vector


def convert_to_gray_scale(input_im, output_im):
    img = Image.open(input_im).convert('L')
    img.save(output_im)
    
    
    
def generate_valid_indices_coordinates_table(pixel_indices):
    
    pixel_indices_vector = pixel_indices.reshape((pixel_indices.size, ))
    pixel_indices_to_coordinates_table = np.array([pixel_indices_vector, np.ones(pixel_indices.size), np.ones(pixel_indices.size)], dtype = np.int64).T
    
    for i in range(pixel_indices_to_coordinates_table.shape[0]):
        
        y = np.argwhere(pixel_indices == pixel_indices_to_coordinates_table[i, 0])[0][0]
        x = np.argwhere(pixel_indices == pixel_indices_to_coordinates_table[i, 0])[0][1]
        
        pixel_indices_to_coordinates_table[i, 1] = x
        pixel_indices_to_coordinates_table[i, 2] = y
        
    return pixel_indices_to_coordinates_table




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


# This class assumes you have a tree already.
class neighbour_search:
    
    def __init__(self, object_center_tree, M, grid_points_array, object_center_array):
        self.object_center_tree = object_center_tree
        self.M = M
        self.grid_points_array = grid_points_array
        self.object_center_array = object_center_array

    #------------------------------------------------------------------------------
    #@numba.njit(cache=True)
    def nearest_neighbour_grid_oc(self):
    
        nearest_object_distance_array = np.zeros(shape=[self.M, 1], dtype = np.float64)
        
        self.object_center_array = np.array(self.object_center_array)
        
        # Grid points array is in the form of (x,y)
        # no object centers detected
        if self.object_center_array.size == 0: 
            
            # Maybe better to use center of image as initial object center instead.
            self.object_center_array = np.array([[0,0]]) 
            
            rep_center = np.repeat(self.object_center_array, self.M, 0)
            
            dist = np.linalg.norm(self.grid_points_array - rep_center, axis = 1)
            
            nearest_object_distance_array = dist.reshape((self.M, 1))        
        
        # >=2 object centers detected
        elif self.object_center_array.shape[0] >= 2: 
            
            nearest_object_distance_array = rtree_nearest(self.object_center_tree, self.M, self.grid_points_array, nearest_object_distance_array)
        
        # one object center detected
        else: 
            
            rep_center = np.repeat(self.object_center_array, self.M, 0)
            
            dist = np.linalg.norm(self.grid_points_array - rep_center, axis = 1)
            
            nearest_object_distance_array = dist.reshape((self.M, 1))
            
        return nearest_object_distance_array
    
    #------------------------------------------------------------------------------



class basic_preprocessing(neighbour_search):
    
    def __init__(self, bool_img_path, img_path, pa, min_semi_axis, max_semi_axis, obj_min_area_threshold, obj_max_area_threshold, num_cluster, gmm_n, log_p_R_option):
        """
        input: img_path = "C:/Users/hinsm/iCloudDrive/imdata_2d.jpg"
               pa (pixels_away) = pixels_away_list[8]
        """
        self.bool_img_path = bool_img_path
        self.img_path = img_path
        self.pa = pa
        self.min_semi_axis = min_semi_axis
        self.max_semi_axis = max_semi_axis
        self.obj_min_area_threshold = obj_min_area_threshold
        self.obj_max_area_threshold = obj_max_area_threshold
        self.num_cluster = num_cluster
        self.gmm_n = gmm_n
        self.log_p_R_option = log_p_R_option
        
    def basic_image_analyses(self):
        
        # P.01: Input and definitions
        #if imdata.ndim == 3:
        #    imdata = imdata.transpose(2,0,1).reshape(3,-1)
        
        if self.bool_img_path == True:
            imdata = plt.imread(self.img_path)
        else:
            imdata = self.img_path

        # P.01.1: DO GRID_POINTS DEFINITION BEFORE ALL PREPROCESSING
        y_axis, x_axis = imdata.shape
        
        # Check for pixel size divisbility for blocking and defining grid points
        adj_y_axis = pixel_calculator.update_pixel_divisibility(y_axis, self.pa)
        
        adj_x_axis = pixel_calculator.update_pixel_divisibility(x_axis, self.pa)
        
        upd_imdata = image_pixel_expansion.update_image(imdata, adj_y_axis, adj_x_axis)
        
        D = upd_imdata.size # pixel size of the image
        
        # Grid points array is in the form of (x,y)
        M, grid_points_array = grid_points.set_grid_points(upd_imdata, self.pa)
        
        # P.02: Median filtering
        med_denoised = filtering.median_filter(upd_imdata, 5) #5 is optimal, 6 starts to connect objects (for our sample image)
        
        processed_mask = masking_class.masking(med_denoised)
        
        img_vector = processed_mask.reshape((processed_mask.size, 1))
        
        # P.03: 3-component GMM and generating information useful for data likelihood calculation
        fg_prob_vector, bg_prob_vector = intensity_probability(img_vector, self.gmm_n)
        
        
        if self.gmm_n == 2:
            
            log_fg_prob_vector = np.log(fg_prob_vector + 0.0000001)
            log_bg_prob_vector = np.log(bg_prob_vector + 0.0000001)
            
            normalized_log_fg_prob_vector = np.empty((log_fg_prob_vector.size,))
            normalized_log_bg_prob_vector = np.empty((log_fg_prob_vector.size,))
            
            for r in range(D):
                
                log_row = np.array([log_fg_prob_vector[r], log_bg_prob_vector[r]])
                norm_log_row = np.exp(log_row - logsumexp(log_row))
                normalized_log_fg_prob_vector[r] = norm_log_row[0]
                normalized_log_bg_prob_vector[r] = norm_log_row[1]
        
        #if self.gmm_n >= 3:
        #    
        #    # The fg prob and bg prob are normalized in terms of three components. We need to normalize them in terms of 2 components (only fb and bg).
        #    normalized_fg_prob_vector = np.empty((fg_prob_vector.size,))
        #    normalized_bg_prob_vector = np.empty((fg_prob_vector.size,))
        #
        #    for r in range(D):
        #    
        #        # normalizing fg and bg probabilities row-wise.
        #        row = np.array([fg_prob_vector[r], bg_prob_vector[r]])
        #        normalized_row = row / row.sum()
        #        normalized_fg_prob_vector[r] = normalized_row[0]
        #        normalized_bg_prob_vector[r] = normalized_row[1]
        
        # 2-Means Clustering (Oct-19: Keep k-means clustering for the purpose of identifying initial object centers)
        km_img, km_label, km_center = clustering.kmeans(processed_mask, self.num_cluster, 10, True, True)
        
        # Finding object centre and initial number ofF objects
        centres, num_objects = object_centre_search.object_centre(km_img, km_label, self.obj_min_area_threshold, self.obj_max_area_threshold, True)

        # Object Center detection safety catch (insert one object center, construct as 2-dim)
        if centres.size == 0:
            centres = np.array([[int(adj_x_axis/2), int(adj_y_axis/2)]])

        ### Initialization of z_d, N, beta_d  (HOMOGENEOUS CASE) #####################
        # use centres.shape[0], not num_objects. Because if centres was initially detected as empty, the neighbour_search function will add one to it.
        N = centres.shape[0] 
        
        Z = transform_centre_to_Z(centres, upd_imdata.shape)
        
        pixel_indices = np.arange(0, upd_imdata.size, dtype = 'int64')
        pixel_indices = pixel_indices.reshape((pixel_indices.size, 1))
        pixel_indices = pixel_indices.reshape(upd_imdata.shape)
        
        pi_reshaped = pixel_indices.reshape((pixel_indices.size, 1))
        master_Z = np.column_stack((Z, pi_reshaped))
        zdnot0_array = master_Z[master_Z[:,0] != 0]

        pixel_indices_vector = pixel_indices.reshape((pixel_indices.size,))
        mask_set = np.repeat(-1, len(pixel_indices_vector))
        
        #Construct an initial R-tree for calculating spatial distance
        object_center_tree = rtree(grid_points_array, centres, pixel_indices, upd_imdata.shape)
        
        # Spatial Distance Method (Pollard, 1971)
        nearest_object_distance = neighbour_search(object_center_tree, M, grid_points_array, centres).nearest_neighbour_grid_oc() + 0.000001
        

        #pixel_indices_to_coordinates_table = generate_valid_indices_coordinates_table(pixel_indices)
        
        if  self.log_p_R_option == "homo":
            
            beta_d = N/D # beta_d is real number, not vector, homogeneous case.
            
        elif  self.log_p_R_option == "inhomo":
            
            # For the MC integration in the variational mean field
            # We take 80% of the number of pixel size of the image.
            num_integration_points = int(D * 0.80)

            # Inducing points are the grid points (equally spaced).
            # We put inducing points to be 10 pixels apart from each other.
            # This should be okay since the adjusted axes pixels are multiples of 10
            num_inducing_points = int(adj_x_axis/ 10) * int(adj_y_axis / 10)

            ### Data Generation
            S_borders = np.array([[0, upd_imdata.shape[0] - 1 ],
                                  [0, upd_imdata.shape[0] - 1 ]])

            # Just a basic initialization of covariance parameters
            cov_params = [2., np.array([1, 1])]

            X_vec = np.zeros((upd_imdata.shape[0], 2))
            
            for i in range(upd_imdata.shape[0]):
                X_vec[i, 0] = i
                X_vec[i, 1] = i
                
            X_mesh, Y_mesh = np.meshgrid(X_vec[:,0], X_vec[:,1])
            X_grid = np.vstack([X_mesh.flatten(), Y_mesh.flatten()]).T

            # Set filtering threshold to be the mean of image appears to be accurate.
            pi_vec = pixel_indices[upd_imdata >= np.mean(upd_imdata)]
            x_coord_vec = np.zeros((pi_vec.size, ))
            y_coord_vec = np.zeros((pi_vec.size, ))
            
            for i in range(pi_vec.size):
                x_coord_vec[i] = np.argwhere(pixel_indices == pi_vec[i])[0][1]
                y_coord_vec[i] = np.argwhere(pixel_indices == pi_vec[i])[0][0]

            x_coord_vec = x_coord_vec.reshape((x_coord_vec.size, 1))
            y_coord_vec = y_coord_vec.reshape((y_coord_vec.size, 1))

            # ((x,y)) or ((y,x)) depends on whether the author analyses the data using the
            # original way the image is defined, which is ((y,x))
            X = np.hstack((x_coord_vec, y_coord_vec))

            # Fit variational mean field posterior

            # This is where we estimate the Poisson intensity of all the pixels
            var_mf_sgcp = VMF_SGCP(S_borders, X, cov_params, num_inducing_points, 
                                   num_integration_points = num_integration_points, 
                                   update_hyperparams = True, output = 0, conv_crit = 1e-4)

            var_mf_sgcp.run()

            mu_lmbda_vb, var_lmbda_vb = var_mf_sgcp.predictive_intensity_function(X_grid)

            # We do not assume that that the Poisson rate must be between 0 and 1.
            # Actually in the paper, they call it a probability map but their rates was between 0 and 2.
            beta_d = mu_lmbda_vb

        
        # Create GridPoints object (and insert coords, dist, and nearest neighbour)
        GridPoints = np.zeros((grid_points_array.shape[0], 1), dtype=object)

        for g in range(GridPoints.shape[0]):

            GridPoints[g, 0] = GridPoint(grid_points_array[g])
	
        for g in range(GridPoints.shape[0]):

            GridPoints[g, 0].dist = nearest_object_distance[g, 0]
            GridPoints[g, 0].nearest = list(object_center_tree.nearest(tuple(GridPoints[g, 0].coords), 1, objects = 'raw'))[0]
        
        
        ###############################################################################
        # Initial 2: sample {s_n} (s=1,...,N) for every object
        MAX = 50 #not used
        
        # Below is the only way to ensure a random generation every time
        # The last three 1's are the initial S.D. for each shape parameter for adaptive MCMC in Step 2.
        S = np.array([[np.random.uniform(self.min_semi_axis, self.max_semi_axis), np.random.uniform(self.min_semi_axis, self.max_semi_axis), np.random.uniform(-math.pi, math.pi), zdnot0_array[n,1], 1, 1, 1]
                      for n in range(N)])


        return [imdata, upd_imdata, GridPoints, pixel_indices, Z, S, centres, 
         beta_d, M, grid_points_array, normalized_log_fg_prob_vector, normalized_log_bg_prob_vector, object_center_tree, 
         MAX, 'binning', mask_set, self.log_p_R_option, nearest_object_distance, self.min_semi_axis, self.max_semi_axis]
        
