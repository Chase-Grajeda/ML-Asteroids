import pygame
import numpy as np 
import math 
import scipy.special 

MUTATION_CHANCE = 0.2
MUTATION_MIX_PERC = 0.5
MUTATION_CUTOFF = 0.4 
MUTATION_BAD_KEEP = 0.2
MUTATION_CHANCE_LIMIT = 0.4

class Network(): 
    def __init__(self, num_input, num_h1, num_h2, num_output): 
        self.num_input = num_input 
        self.num_h1 = num_h1   
        self.num_h2 = num_h2 
        self.num_output = num_output 
        
        self.weight_input_h1 = np.random.uniform(-0.5, 0.5, size=(self.num_h1, self.num_input)) 
        self.weight_input_h2 = np.random.uniform(-0.5, 0.5, size=(self.num_h2, self.num_h1)) 
        self.weight_output = np.random.uniform(-0.5, 0.5, size=(self.num_output, self.num_h2))  
        
        self.activation_func = lambda x: scipy.special.expit(x) 
        
    def get_outputs(self, inputs_list): 
        inputs = np.array(inputs_list, ndmin=2).T 
        
        h1_inputs = np.dot(self.weight_input_h1, inputs) 
        h1_outputs = self.activation_func(h1_inputs) 
        
        h2_inputs = np.dot(self.weight_input_h2, h1_outputs) 
        h2_outputs = self.activation_func(h2_inputs) 
        
        final_inputs = np.dot(self.weight_output, h2_outputs) 
        final_outputs = self.activation_func(final_inputs) 
        
        return final_outputs 
        
    def get_max_value(self, inputs_list): 
        outputs = self.get_outputs(inputs_list) 
        return np.max(outputs) 
    
    def modify_weights(self): 
        self.modify_array(self.weight_input_h1) 
        self.modify_array(self.weight_input_h2) 
        self.modify_array(self.weight_output) 
        
    def create_mixed_weights(self, pop1, pop2): 
        self.weight_input_h1 = self.getMixedArrs(pop1.network.weight_input_h1, pop2.network.weight_input_h1) 
        self.weight_input_h2 = self.getMixedArrs(pop1.network.weight_input_h2, pop2.network.weight_input_h2) 
        self.weight_output = self.getMixedArrs(pop1.network.weight_output, pop2.network.weight_output) 
    
    def modify_array(self, array): 
        for i in np.nditer(array, op_flags=['readwrite']): 
            if np.random.random() < MUTATION_CHANCE: 
               i[...] = np.random.random_sample() - 0.4
        
    def getMixedArrs(self, arr1, arr2): 
        total_entries = arr1.size 
        num_rows = arr1.shape[0] 
        num_cols = arr1.shape[1] 
        
        num_to_take = total_entries - int(total_entries * MUTATION_MIX_PERC) 
        idx = np.random.choice(np.arange(total_entries), num_to_take, replace=False) 
        
        res = np.random.rand(num_rows, num_cols) 
        
        for row in range(0, num_rows): 
            for col in range(0, num_cols): 
                index = row * num_cols + col 
                if index in idx: 
                    res[row][col] = arr1[row][col]
                else: 
                    res[row][col] = arr2[row][col]

        return res 
    
    def fillArray(self, file): 
        weights = file.readlines() 
        idx = 0 

        for i in np.nditer(self.weight_input_h1, op_flags=["readwrite"]): 
            i[...] = float(weights[idx]) 
            idx += 1
        for i in np.nditer(self.weight_input_h2, op_flags=["readwrite"]): 
            i[...] = float(weights[idx])
            idx += 1
        for i in np.nditer(self.weight_output, op_flags=["readwrite"]): 
            i[...] = float(weights[idx]) 
            idx += 1