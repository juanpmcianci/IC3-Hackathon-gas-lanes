#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:09:03 2023

@author: juanpablomadrigalcianci
"""
from params import eth_opcodes
from aux import classify

ETH_OPCODES=eth_opcodes()


class Opcode:
    def __init__(self, id: int=None, name: str=None, gas_used: float=0):
        """
        Represents an opcode in a message.

        Args:
            id (int): The unique identifier of the opcode.
            name (str): The name or identifier of the opcode.
            gas_used (float): The amount of gas consumed by the opcode.
        """
        self.id = id
        self.name = name
        
        if name in ETH_OPCODES:
            self.gas_used = ETH_OPCODES[name]
        else:
            self.gas_used=gas_used
        
        self.belongs_to_lane=classify(self.name,self.id)
    
        
    
        
        



    
