#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 12:21:27 2023

@author: juanpablomadrigalcianci
"""

import numpy as np
from message import Message
from mempool import Mempool
from miner import Miner
from opcodes import Opcode
import params
from TFM import EIP1559MultiDimensionalMechanism 
ENV_PARAMS=params.env_params()
LANE_PARAMS=params.gas_lanes_params()
N_steps=ENV_PARAMS['N_steps']


# Instantiates the code
mempool=Mempool()
miner=Miner(account_balance=0)
opcodes_names=list(params.eth_opcodes().keys())



def generate_random_messages(base_fees, rate_messages,rate_opcodes):
        #TODO: This is a placeholder

        N_messages=np.random.poisson(rate_messages)
        list_of_messages=[]
        for n in range(N_messages):
            oc_list=[]
            K=np.random.poisson(rate_opcodes)
            sampled_opcodes = np.random.choice(opcodes_names,K)
            
            aux_list=list(sampled_opcodes)
            oc_list=[Opcode(name=a) for a in aux_list]
            
            MESSAGE_NAME = 'msg1'
            gas_fee_cap=[bf*(1+0.2*np.random.random()) for bf in base_fees]
            gas_premium=[gas_fee_cap[i]-base_fees[i] for i in range(len(base_fees))]
            
            list_of_messages.append(Message(MESSAGE_NAME, gas_fee_cap, gas_premium, oc_list))
        return list_of_messages
    
B0=ENV_PARAMS['initial_base_fee']
A=generate_random_messages(B0,100,10)


