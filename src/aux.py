#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 12:12:43 2023

@author: juanpablomadrigalcianci
"""

from params import eth_opcodes
ETH_OPCODES = eth_opcodes()


def classify(name: str = None, opcode_id: int = None):
    """
    Classify an opcode into a specific group.

    Args:
        name (str): The name of the opcode.
        opcode_id (int): The identifier of the opcode.

    Returns:
        int: The lane number representing the opcode group.
    """
    if name is not None:
        # TODO: Model only considers 2 lanes at the moment, this needs to change
        if name in ETH_OPCODES:
            lane = 0
        else:
            lane = 1

    else:
        raise ValueError("Opcode name must be provided")

    return lane


    
    
    
