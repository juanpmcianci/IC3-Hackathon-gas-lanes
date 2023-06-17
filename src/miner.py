#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 14:55:04 2023

@author: juanpablomadrigalcianci
"""
from user import User
from knapsack import multidimensional_knapsack_approx,multidimensional_knapsack
import params

env_params = params.env_params()
N_lanes = env_params['N_lanes']
lane_widths= env_params['lane_widths']


class Miner(User):
    def __init__(self, account_balance: float):
        super().__init__()
        self.account_balance = account_balance
    def propose_block(self,mempool,capacity):
        values,weights=mempool.get_parameters_for_knapsack()
        list_of_messages=multidimensional_knapsack_approx(values=values,
                                                          weights=weights,
                                                          capacity=capacity) 
        
        
        return list_of_messages
    
    
        
        
        
        
        
            
            
        
        
        
        
        
        
        
        

    

