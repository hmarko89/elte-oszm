from mip import Model, xsum, maximize, BINARY, INTEGER, OptimizationStatus

import random

def random_knapsack_instance( nitems:int, seed:int= 0 ):
    """
    A simple instance generator for knapsack problem.

    Args:
        - nitems: number of items to generate
        - seed:   random seed

    Returns:
        - list of items' profit
        - list of items' weight
        - capacity of the knapsack
    """
    assert 0 < nitems, 'number of items should be positive!'

    random.seed( seed )

    profits = [ random.randint(20,50) for _ in range(nitems) ]
    weights = [ random.randint(20,50) for _ in range(nitems) ]
    capacity = sum( weights ) * 0.75

    return profits, weights, capacity

def solve_knapsack( profits:list, weights:list, capacity:float, binary:bool= False ):
    """
    Solves the binary/integer knapsack problem.

    Args:
        - profits:  list of profits
        - weights:  list of items' weight
        - capacity: capacity of the knapsack
        - binary:   indicates whether items can be selected more than once

    Returns:
        - objective value
        - list of items' multiplication in the knapsack
    """
    assert len(profits) == len(weights), 'the lists are of different lengths!'

    # initialize
    nitems = len(profits)
    ITEMS = range(nitems)

    # BUILD MODEL
    model = Model( 'knapsack' )

    # variables: x[i] = the multiplicity of item i in the knapsack
    x = [ model.add_var( var_type= BINARY if binary else INTEGER, name = f'x_{i}' ) for i in ITEMS ]

    # constraint: total weight of selected items must respect the capacity limit
    model += xsum( weights[i] * x[i] for i in ITEMS ) <= capacity, 'capacity'
    #model.add_constr( xsum( weights[i] * x[i] for i in ITEMS ) <= capacity, 'capacity' ) # equivalent

    # objective: maximize the profit
    model.objective = maximize( xsum( profits[i] * x[i] for i in ITEMS ) )

    # SOLVE PROBLEM
    model.write( 'knapsack.lp' )
    model.verbose = False
    model.optimize()

    assert model.status == OptimizationStatus.OPTIMAL, f'could not solve problem to optimality (status= {model.status})'

    # return objective value and the solution (i.e., the multiplicity of the items)
    return model.objective.x, [ x[i].x for i in ITEMS ]

if __name__ == '__main__':
    profits, weights, capacity = [10, 13, 18, 31, 7, 15], [11, 15, 20, 35, 10, 33], 47    
    #profits, weights, capacity = random_knapsack_instance( 20 )
    value, solution = solve_knapsack( profits, weights, capacity, True )

    print( f'objective: {value}' )
    print( f'solution : {solution}' )
