# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:32:19 2020

@author: hinsm
"""

import matplotlib.pyplot as plt
import PIL
from copy import copy
from datetime import datetime
import numpy as np

class results_analyses:
    
    def __init__(self, Ellipse, img_shape, img, display):
        self.Ellipse = Ellipse
        self.img_shape = img_shape
        self.img = img
        self.display = display

    # /////////////// PLOTTING THE ELLIPSE //////////////////////////////////////    
    def plot_ellipse(self):
        
        fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
        
        fig2 = plt.imshow(self.img, cmap=plt.cm.gray)
        
        for ell in self.Ellipse:
            #ax.add_artist(ell)
            
            new_ell = copy(ell)
            
            ax.add_artist(new_ell)
            
            ell.set_clip_box(ax.bbox)
            
            ell.set_alpha(2)

        ax.set_ylim(0, self.img_shape[0])
        
        ax.set_xlim(0, self.img_shape[1])
        
        plt.gca().invert_yaxis()
        
        now = datetime.now()
        date_time = now.strftime("%Y%m%d_%H%M%S")
        
        rand = str(int(np.ceil(np.random.uniform(2)**2*100)))
        
        plt.savefig('../data_output/final_img_' + date_time + "_r" + rand + '.jpg')
        
        if self.display == True:
            plt.show()
    # ///////////////////////////////////////////////////////////////////////////