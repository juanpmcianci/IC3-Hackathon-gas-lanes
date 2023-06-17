#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:31:57 2023

@author: juanpablomadrigalcianci
"""
from message import Message
class Mempool:
    def __init__(self):
        """
        Represents a mempool that holds a collection of messages.
        """
        self.messages = []

    def add_message(self, message):
        """
        Add a message to the mempool.

        Args:
            message (Message): The message to be added.
        """
        self.messages.append(message)

    def remove_message(self, message):
        """
        Remove a message from the mempool.

        Args:
            message (Message): The message to be removed.
        """
        self.messages.remove(message)

    def calculate_total_gas_used(self):
        """
        Calculate the total gas used in the mempool.

        Returns:
            float: The total gas used in the mempool.
        """
        total_gas_used = sum(message.gas_used for message in self.messages)
        return total_gas_used
    
    def get_parameters_for_knapsack(self):
        
        values=[]
        weights=[]
        
        for m in self.messages:
            values.append(m.gas_premium())
            weights.append(m.gas_limit)
        return values,weights