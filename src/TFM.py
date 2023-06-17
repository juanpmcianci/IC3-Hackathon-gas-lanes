#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 11:24:41 2023

@author: juanpablomadrigalcianci
"""

from typing import List, Tuple


class EIP1559TFM:
    def __init__(self, Id: int, base_fee: float, min_fee: float, target: float, capacity: float):
        """
        Initializes the EIP1559-like Transaction Fee Market (TFM).

        Args:
            base_fee: Base fee for the TFM.
            min_fee: Minimum fee for the TFM.
            target: Target for the TFM.
            capacity: Capacity (block space) of the TFM.
        """
        assert target > 0
        assert capacity > target

        self.Id = Id
        self.base_fee = base_fee
        self.base_fee_list = [self.base_fee]
        self.min_fee = min_fee
        self.target = target
        self.capacity = capacity

    def update_fee(self, gas_used: float) -> float:
        """
        Calculates the fee based on the demand for block space.

        Args:
            gas_used: Gas used in the block.

        Returns:
            The calculated fee.
        """
        increment = (gas_used - self.target) / self.target

        self.base_fee *= (1 + increment / 8)
        self.base_fee = max(self.base_fee, self.min_fee)

        self.base_fee_list.append(self.base_fee)

        return self.base_fee


class EIP1559MultiDimensionalMechanism:
    def __init__(self, dimensions: List[Tuple[int, float, float, float, float]]):
        """
        Initializes the Multi-Dimensional EIP1559 Mechanism.

        Args:
            dimensions: A list of tuples representing the dimensions of each block.
                Each tuple contains the Id, base fee, min fee, target, and capacity of a block's TFM.
        """
        self.tfms = [EIP1559TFM(Id, base_fee, min_fee, target, capacity) for Id, base_fee, min_fee, target, capacity in dimensions]

    def update_fees(self, gas_used: List[float]) -> List[float]:
        """
        Calculates the fees for each block based on the gas used in each block.

        Args:
            gas_used: A list of gas used in each block.

        Returns:
            A list of calculated fees for each block.
        """
        return [tfm.update_fee(gas) for tfm, gas in zip(self.tfms, gas_used)]

    def get_fees(self):
        return [self.tfms[i].base_fee for i in range(len(self.tfms))]


if __name__=='__main__':
    import matplotlib.pyplot as plt
    
    dimensions = [(1, 1.0, 0.5, 50.0, 100.0), 
                  (2, 0.5, 0.2, 30.0, 80.0), 
                  (3, 0.2, 0.1, 20.0, 50.0)]
    eip1559_mechanism = EIP1559MultiDimensionalMechanism(dimensions)
    
    num_epochs = 100
    epoch_gas_used = [70.0, 35.0, 15.0]
    
    base_fee_evolution = [[] for _ in range(len(dimensions))]  # List to store the base fee evolution for each block
    
    for epoch in range(num_epochs):
        fees = eip1559_mechanism.update_fees(epoch_gas_used)
    
        for i, fee in enumerate(fees):
            base_fee_evolution[i].append(fee)
    
        # Update epoch_gas_used for the next epoch (for demonstration purposes)
        epoch_gas_used = [gas * 0.9 for gas in epoch_gas_used]
    
    # Plot the base fee evolution for each block
    for i, base_fee_history in enumerate(base_fee_evolution):
        block_id = dimensions[i][0]
        plt.plot(range(num_epochs), base_fee_history, label=f"Block {block_id}")
    
    plt.xlabel("Epochs")
    plt.ylabel("Base Fee")
    plt.title("Evolution of Base Fee")
    plt.legend()
    plt.grid(True)
    plt.show()













