from pulp import *
from typing import List, Optional

def multidimensional_knapsack(values: List[float], weights: List[List[float]], capacity: List[float]) -> Optional[List[str]]:
    """
    Solves the multidimensional knapsack problem using linear programming.

    Given a set of items with values and weights in multiple dimensions,
    and a capacity for each dimension, this function finds the optimal
    combination of items to maximize the total value while respecting
    the capacity constraints.

    Args:
        values: A list of values for each item.
        weights: A list of lists representing the weights of each item in each dimension.
        capacity: A list of capacities for each dimension.

    Returns:
        A list of strings representing the indices of the chosen items,
        or None if no optimal solution is found.
    """
    num_items = len(values)
    num_dimensions = len(capacity)

    # Create the 'prob' variable to contain the problem data
    prob = LpProblem("Multidimensional Knapsack Problem", LpMaximize)

    # Create decision variables
    item_vars = LpVariable.dicts("Chosen", range(num_items), cat=LpBinary)

    # The objective function is added to 'prob'
    prob += lpSum(values[i] * item_vars[i] for i in range(num_items)), "Total value of items"

    # The capacity constraints are added to 'prob'
    for d in range(num_dimensions):
        prob += lpSum(weights[i][d] * item_vars[i] for i in range(num_items)) <= capacity[d], f"weight_{d}"

    # The problem is solved using PuLP's choice of Solver
    prob.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[prob.status])

    # The solution is printed if it is optimal
    if LpStatus[prob.status] == "Optimal":
        chosen_items = [i for i, var in item_vars.items() if var.varValue > 0]
        return chosen_items
    else:
        return None


def multidimensional_knapsack_approx(values: List[float], weights: List[List[float]], capacity: List[float]) -> List[str]:
    """
    Approximate solution to the multidimensional knapsack problem using a greedy algorithm.

    Given a set of items with values and weights in multiple dimensions,
    and a capacity for each dimension, this function finds an approximate
    combination of items to maximize the total value while respecting the
    capacity constraints. It sorts the items by the value-to-weight ratio
    and greedily adds them to the solution if the capacity allows.

    Args:
        values: A list of values for each item.
        weights: A list of lists representing the weights of each item in each dimension.
        capacity: A list of capacities for each dimension.

    Returns:
        A list of strings representing the indices of the chosen items.
    """
    num_items = len(values)
    num_dimensions = len(capacity)

    # Calculate value-to-weight ratio for each item for each dimension
    # And take the minimum ratio (considering it as the bottleneck)
    ratio = [min(values[i] / (weights[i][d]+1) for d in range(num_dimensions)) for i in range(num_items)]

    # Sort the items by value-to-weight ratio
    items = sorted(range(num_items), key=lambda i: -ratio[i])

    # Initialize the solution
    chosen_items = [0] * num_items
    current_capacity = [0] * num_dimensions

    # Greedily add items to the solution
    for item in items:
        if all(current_capacity[d] + weights[item][d] <= capacity[d] for d in range(num_dimensions)):
            chosen_items[item] = 1
            for d in range(num_dimensions):
                current_capacity[d] += weights[item][d]

    # Return the indices of the chosen items
    return [i for i in range(num_items) if chosen_items[i] == 1]

if __name__=='__main__':
    import time
    t0=time.time()
    values = [60, 100, 100020]
    weights = [[10, 20], [20, 30], [30, 40]]
    capacity = [50, 60]
    
    chosen_items = multidimensional_knapsack(values, weights, capacity)
    print("Chosen items:", chosen_items)
    print(f'computation time {time.time()-t0}')
    
    t0=time.time()
    
    chosen_items = multidimensional_knapsack_approx(values, weights, capacity)
    print("Chosen items:", chosen_items)
    print(f'computation time {time.time()-t0}')