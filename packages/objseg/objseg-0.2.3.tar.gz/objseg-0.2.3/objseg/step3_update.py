# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:20:03 2020

@author: hinsm
"""

class step3_update:

    def __init__(self, param, new_Z, new_S, new_centres, new_nod, new_object_center_tree):
        self.param = param
        self.new_Z = new_Z
        self.new_S = new_S
        self.new_centres = new_centres
        self.new_nod = new_nod
        self.new_object_center_tree = new_object_center_tree
        
    def step3_prob(self):
    
        self.param[4] = self.new_Z
        self.param[5] = self.new_S
        self.param[6] = self.new_centres
        self.param[12] = self.new_object_center_tree
        self.param[17] = self.new_nod
        #no need to return anything
    
    # For blocked, we still need to calculate the likelihood and everything, but 
    # our R will be just 1 element, i.e. r_1