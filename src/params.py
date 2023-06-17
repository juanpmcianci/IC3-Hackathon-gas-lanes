#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:35:39 2023

@author: juanpablomadrigalcianci
"""

def env_params():
    env_params={
        'N_lanes':2,
        'N_steps':2880,
        'lane_widths':[6e9,4e9],
        'lane_targets':[3e9,2e9],
        'initial_base_fee':[1e-10,1e-10],
        'min_fee':[1e-16,1e-16]
        }
    return env_params

def gas_lanes_params():
    '''each lane need to be instantiated with the following parameters:
      Id: int, 
      base_fee: float, 
      min_fee: float,
      target: float, 
      capacity: float)
    '''
    
    P=env_params()
    
    lane_params=[]
    for i in range(P['N_lanes']):
        lane_params.append(
            [i,
                P['initial_base_fee'][i],
                P['min_fee'][i],
                P['lane_targets'][i],
                P['lane_widths'][i]
                ]
            )
        
    
    
    

    
    return lane_params
    
    

    


def eth_opcodes():
    ''' This is a list of eth opcodes, multiplied by 222, a rough esitmate of the 
    equivalency there'''
    
    opcode_gas_limits = {
        "STOP": 0,
        "ADD": 666,
        "MUL": 1110,
        "SUB": 666,
        "DIV": 1110,
        "SDIV": 1110,
        "MOD": 666,
        "SMOD": 1110,
        "ADDMOD": 1776,
        "MULMOD": 1776,
        "EXP": 2220,
        "SIGNEXTEND": 1110,
        "LT": 666,
        "GT": 666,
        "SLT": 666,
        "SGT": 666,
        "EQ": 666,
        "ISZERO": 666,
        "AND": 666,
        "OR": 666,
        "XOR": 666,
        "NOT": 666,
        "BYTE": 666,
        "SHL": 666,
        "SHR": 666,
        "SAR": 666,
        "SHA3": 6660,
        "ADDRESS": 444,
        "BALANCE": 88800,
        "ORIGIN": 444,
        "CALLER": 444,
        "CALLVALUE": 444,
        "CALLDATALOAD": 666,
        "CALLDATASIZE": 444,
        "CALLDATACOPY": 666,
        "CODESIZE": 444,
        "CODECOPY": 666,
        "GASPRICE": 444,
        "EXTCODESIZE": 155400,
        "EXTCODECOPY": 155400,
        "RETURNDATASIZE": 444,
        "RETURNDATACOPY": 666,
        "EXTCODEHASH": 88800,
        "BLOCKHASH": 4440,
        "COINBASE": 444,
        "TIMESTAMP": 444,
        "NUMBER": 444,
        "DIFFICULTY": 444,
        "GASLIMIT": 444,
        "CHAINID": 444,
        "SELFBALANCE": 1110,
        "BASEFEE": 444,
        "POP": 444,
        "MLOAD": 666,
        "MSTORE": 666,
        "MSTORE8": 666,
        "SLOAD": 11100,
        "SSTORE": 4440000,
        "JUMP": 1776,
        "JUMPI": 2220,
        "PC": 444,
        "MSIZE": 444,
        "GAS": 444,
        "JUMPDEST": 222,
        "PUSH1": 666,
        "PUSH2": 666,
        "PUSH3": 666,
        "PUSH4": 666,
        "PUSH5": 666,
        "PUSH6": 666,
        "PUSH7": 666,
        "PUSH8": 666,
        "PUSH9": 666,
        "PUSH10": 666,
        "PUSH11": 666,
        "PUSH12": 666,
        "PUSH13": 666,
        "PUSH14": 666,
        "PUSH15": 666,
        "PUSH16": 666,
        "PUSH17": 666,
        "PUSH18": 666,
        "PUSH19": 666,
        "PUSH20": 666,
        "PUSH21": 666,
        "PUSH22": 666,
        "PUSH23": 666,
        "PUSH24": 666,
        "PUSH25": 666,
        "PUSH26": 666,
        "PUSH27": 666,
        "PUSH28": 666,
        "PUSH29": 666,
        "PUSH30": 666,
        "PUSH31": 666,
        "PUSH32": 666,
        "DUP1": 666,
        "DUP2": 666,
        "DUP3": 666,
        "DUP4": 666,
        "DUP5": 666,
        "DUP6": 666,
        "DUP7": 666,
        "DUP8": 666,
        "DUP9": 666,
        "DUP10": 666,
        "DUP11": 666,
        "DUP12": 666,
        "DUP13": 666,
        "DUP14": 666,
        "DUP15": 666,
        "DUP16": 666,
        "SWAP1": 666,
        "SWAP2": 666,
        "SWAP3": 666,
        "SWAP4": 666,
        "SWAP5": 666,
        "SWAP6": 666,
        "SWAP7": 666,
        "SWAP8": 666,
        "SWAP9": 666,
        "SWAP10": 666,
        "SWAP11": 666,
        "SWAP12": 666,
        "SWAP13": 666,
        "SWAP14": 666,
        "SWAP15": 666,
        "SWAP16": 666,
        "LOG0": 83250,
        "LOG1": 166500,
        "LOG2": 249750,
        "LOG3": 333000,
        "LOG4": 416250,
        "CREATE": 7104000,
        "CALL": 155400,
        "CALLCODE": 155400,
        "RETURN": 0,
        "DELEGATECALL": 155400,
        "CREATE2": 7104000,
        "STATICCALL": 155400,
        "REVERT": 0,
        "INVALID": 0,
        "SELFDESTRUCT": 1110000
    }
    
    for opcode in opcode_gas_limits:
        opcode_gas_limits[opcode] += 100000000

    return opcode_gas_limits

