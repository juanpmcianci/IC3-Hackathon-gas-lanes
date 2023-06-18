#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the message module
"""
import numpy as np
import params 

env_params = params.env_params()
N_lanes = env_params['N_lanes']

class Message:
    def __init__(self, ID: str, gas_fee_cap: list, gas_premium: list, opcode_list: list, params: list = None):
        """
        Represents a message included in the blockchain.

        Args:
            ID (str): The identifier for the message.
            gas_fee_cap (float): The maximum fee that the sender is willing to pay.
            gas_premium (float): The additional fee that the sender is willing to pay to get the transaction included
                in a block quickly.
            opcode_list (list): List of opcode instances representing the operations in the message.
            params (list, optional): Additional parameters for the message. Defaults to None.
        """
        self.ID = ID
        self.gas_fee_cap = gas_fee_cap
        self.gas_premium = gas_premium
        self.opcode_list = opcode_list
        self.gas_used = self.get_gas_used()
        self.gas_limit = self.calculate_gas_limit()
        self.params = params

    def get_gas_used(self) -> list:
        """
        Calculates the total gas used for each lane by summing up the gas used by each opcode in the opcode list.

        Returns:
            list: The gas used for each lane.
        """
        gas_used = [ 0 for i in range(N_lanes)]
        for opcode in self.opcode_list:
            if len(gas_used)>1:
                lane = opcode.belongs_to_lane
            else:
                lane=0
            gas_used[lane] += opcode.gas_used

        return gas_used

    def calculate_gas_limit(self) ->list:
        """
        Calculates the gas limit for each lane by adding a random factor to the gas used.

        Returns:
            list: The calculated gas limit for each lane.
        """
        gas_limit = [ 0 for i in range(N_lanes)]

        for l in range(N_lanes):
            overestimation_factor=(1 + 0.2*np.random.random())
            gas_limit[l]=int(self.gas_used[l]*overestimation_factor)

        return gas_limit
    
if __name__ == '__main__':
    from opcodes import Opcode

    opcode1 = Opcode(1, "ADD")
    opcode2 = Opcode(2, "SUB")
    opcode3 = Opcode(3, "MUL")
    opcode4 = Opcode(4, "foreign_opcode", 100)

    opcode_list = [opcode1, opcode2, opcode3, opcode4]
    MESSAGE_NAME = 'msg1'
    message1 = Message(MESSAGE_NAME, [100.0,100], [50.0,50], opcode_list)
    print(f'Message {MESSAGE_NAME} has a gas usage of {message1.gas_used} and a gas limit of {message1.gas_limit}')
