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
    
    
    # For the love of god do not run this 
    # This needs to be adapted to the main program 
    # Uses pseudo code, so be careful 
#    def evolve(self, populations): 
#        cutoff = int(len(populations) * MUTATION_CUTOFF) 
#        good_ships = populations[0:cutoff] 
#        bad_ships = populations[cutoff:] 
#        num_bad_to_take = int(len(populations) * MUTATION_BAD_KEEP) 
#        
#        for b in bad_ships: 
#            b.modify_weights() 
#        
#        new_birds = []
#        
#        idx_bad_to_take = np.random.choice(np.arange(len(bad_ships)), num_bad_to_take, replace=False)
#        
#        for index in idx_bad_to_take: 
#            new_birds.append(bad_ships[index]) 
#            
#        new_birds.extend(good_ships) 
#        
#        children_needed = len(populations) - len(new_birds) 
#        
#        while len(new_birds) < len(populations): 
#            idx_to_breed = np.random.choice(np.arange(len(good_ships)), 2, replace=False) 
#            if idx_to_breed[0] != idx_to_breed[1]: 
#                new_ship = Network.createOffspring(good_ships[idx_to_breed[0]], good_ships[idx_to_breed[1]]) 
#                if np.random.random() < MUTATION_CHANCE_LIMIT: 
#                    new_ship.network.modify_weights() 
#                new_birds.append(new_ship) 
    

#def test1(): 
    #net = Network(9, 9, 6, 3) 
    #inputs = [0.2, 0.3, 0.4, 0.5, 0.6, 0.1, 0.3, 0.6, 0.7] 
    #output = net.get_max_value(inputs) 
    #print("Output", output, sep='\n')

#def test():  
#    net = Network(9, 9, 6, 3)
#    ar1 = np.random.uniform(-0.5, 0.5, size=(3,4)) 
#    ar2 = np.random.uniform(-0.5, 0.5, size=(3,4)) 
#    print("ar1.size", ar1.size, sep='\n') 
#    print("ar1", ar1, sep='\n') 
#    
#    net.modify_array(ar1) 
#    print("ar1", ar1, sep='\n') 
#    
#    print("") 
#    
#    print("ar1", ar1, sep='\n') 
#    print("ar2", ar2, sep='\n') 
#    
#    mixed = net.getMixedArrs(ar1, ar2) 
#    print("Mixed", mixed, sep='\n') 
    
# test()  