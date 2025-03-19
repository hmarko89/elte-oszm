import mip
import random
import matplotlib.pyplot as plt

from knapsack import solve_knapsack

from time import perf_counter
from collections import defaultdict

def random_instance( m:int, c:float, T:int, seed:int= 0 ):
    """
    Returns a random cutting stock instance.

    Degraeve, Z., & Peeters, M. (1998). Benchmark results for the cutting stock and bin packing problem. DTEW Research Report 9820, 1-29.

    Args:
        m:    number of items
        c:    fraction from (0,1), e.g., 0.25, 0.5, 0.75
        T:    total demand, e.g., 10*m, 50*m, 100*m
        seed: random seed

    Retruns:
        m:           number of types
        widths:      widths of types
        demands:     demands from types
        max_width:   width of the rolls
    """
    random.seed(seed)

    max_width = 10000
    widths = [ int( random.random() * max_width * c ) for _ in range(m) ]

    R = [ 0.1 + random.random() * 0.8 for _ in range(m) ]

    demands = [ int( R[i] * T / sum(R) ) for i in range(m) ]

    return m, widths, demands, max_width

def __log( model:mip.Model, ncols:int, time:float ) -> None:
    solution_str = f'{model.objective_bound:8.1f} | {"inf":8} | {"inf":4s}'
    if model.status in [ mip.OptimizationStatus.OPTIMAL, mip.OptimizationStatus.FEASIBLE ]:
        solution_str = f'{model.objective_bound:8.1f} | {model.objective_value:8.1f} | {model.gap:4.2f}'

    print( f'{model.name:10s} │ {model.status.name[:10]:10s} │ {model.num_cols:5d} │ {model.num_rows:5d} │ {ncols:5d} | {solution_str} │ {time:6.2f}' )

def solve_cutting_stock_first_fit( m:int, widths:list[int], demands:list[int], max_width:int ) -> list[defaultdict[int,int]]:
    """
    Solves the cutting stock problem with first-fit heuristic.

    Arg:
        - m:         number of types
        - widths:    widths of types
        - demands:   demands from types
        - max_width: width of the rolls

    Returns:
        - rolls: a list of 'width -> quantity' dictionaries
    """
    # initialization
    TYPES = range(m)

    # collect items
    items = sorted( [ widths[i] for i in TYPES for _ in range(demands[i]) ], reverse= True )

    # solve problem
    rolls:list[defaultdict[int,int]] = []

    for item in items:
        roll_found = False

        for roll in rolls:
            if sum( width * quantity for (width,quantity) in roll.items() ) + item <= max_width:
                roll_found = True
                roll[item] += 1
                break

        if not roll_found:
            rolls.append( defaultdict( lambda: 0, { item: 1 } ) )

    return rolls

def solve_cutting_stock_mip( m:int, widths:list[int], demands:list[int], max_width:int, max_stocks:int= None, demand_geq:bool= False, symmetry_breaking:bool= False, initial_solution:list[defaultdict[int,int]]= None, max_seconds= mip.INF ) -> None:
    """
    Solves the cutting stock problem as a MIP with Python-MIP.

    Arg:
        - m:                 number of types
        - widths:            widths of types
        - demands:           demands from types
        - max_width:         width of the rolls
        - max_stocks:        upper bound on the number of stocks
        - demand_geq:        should we use '>=' for demands?
        - symmetry_breaking: should we use symmetry breaking inequalitites?
        - initial_solution:  initial solution for the problem
        - solve_mip:         should we solve the MIP with the resulted column set?
        - max_seconds:       time limit
    """
    # initialization
    N = max_stocks if max_stocks else sum(demands)

    TYPES = range(m)
    ROLLS = range(N)

    # BUILD MODEL
    model = mip.Model( f'M{"-SYM" if symmetry_breaking else ""}{"-INIT" if initial_solution else ""}', sense= mip.MINIMIZE )

    # x-variables
    x = [ [ model.add_var( f'x_{i}_{j}', var_type= mip.INTEGER ) for j in ROLLS ] for i in TYPES ]

    # demand constraints
    for i in TYPES:
        if demand_geq:
            model += mip.xsum( x[i][j] for j in ROLLS ) >= demands[i]
        else:
            model += mip.xsum( x[i][j] for j in ROLLS ) == demands[i]

    # y-variables (with objcetive)
    y = [ model.add_var( f'y_{j}', var_type= mip.BINARY, obj= 1 ) for j in ROLLS ]

    # knapsack constraints
    for j in ROLLS:
        model += mip.xsum( widths[i] * x[i][j] for i in TYPES ) <= max_width * y[j]

    # symmetry breaking
    if symmetry_breaking:
        for j in range(1,N):
            model += y[j] <= y[j-1]

    if initial_solution:
        start = []
        for roll_id, roll in enumerate(initial_solution):
            for i in TYPES:
                start.append( ( x[i][roll_id], roll[widths[i]] ) )

        model.start = start

    # SOLVE PROBLEM
    model.verbose = False
    start = perf_counter()
    model.optimize( max_seconds= max_seconds )
    end = perf_counter()

    __log( model, 0, end-start )

def solve_cutting_stock_column_generation( m:int, widths:list, demands:list, max_width:float, draw_states:bool= False, solve_mip:bool= True ) -> None:
    """
    Solves the LP-relaxation of the cutting stock problem.

    Arg:
        - m:           number of types
        - widths:      widths of types
        - demands:     demands from types
        - max_width:   width of the rolls
        - draw_states: should we draw states?
        - solve_mip:   should we solve the MIP with the resulted column set?
    """
    # INITIALIZATION
    TYPES = range(m)

    # initial patterns
    patterns = [ [ int(max_width / widths[i]) if i==t else 0 for i in TYPES ] for t in TYPES ]

    # BUILD MODEL
    model = mip.Model( 'COLGEN', sense= mip.MINIMIZE )
    model.verbose = 0

    # initial variables
    x = [ model.add_var( name= f'x_{i}', var_type= mip.INTEGER, obj= 1 ) for i in range(len(patterns)) ]

    # initial constraints
    conss = [ model.add_constr( demands[t] <= mip.xsum( x[i] * patterns[i][t] for i in range(len(patterns)) ), name= f'demand_{t}' ) for t in TYPES ]

    # COLUMN GENERATION
    start = perf_counter()
    states = []

    # solve LP iteratively
    while True:
        # solve the LP-relaxation of the problem
        model.optimize( relax= True )

        # get dual values
        master_objval = model.objective.x
        dual_values = [ conss[t].pi for t in TYPES ]

        # solve subproblem (pricing problem)
        sub_objval, pattern = solve_knapsack( dual_values, widths, max_width )

        states.append( master_objval )

        # add new pattern to the problem, if any
        if sub_objval <= 1 + model.opt_tol:
            break

        column = mip.Column( conss, pattern ) # create column from pattern
        x.append( model.add_var( name= f'x_{len(patterns)}', var_type= mip.INTEGER, obj= 1, column= column ) ) # create variable based on column
        patterns.append( pattern )

    # solve MIP
    if solve_mip:
        model.optimize()
    end = perf_counter()

    __log( model, 0, end-start )

    # draw states
    if draw_states:
        plt.plot( states )
        plt.xlabel( 'Iterations' )
        plt.ylabel( 'Objective' )
        plt.show()

    return model.objective.x

if __name__ == '__main__':
    # m         = 15
    # widths    = [ 6,11,17,21,24, 28,30,33,42,49, 56,69,74,87,91 ]
    # demands   = [ 9, 6,20,30,17, 19,25,12, 8,20,  5,14,15,18,10 ]
    # max_width = 100

    n = 15    # 10, 20, 30, 40, 50, 75, 100
    c = 0.25  # 0.25, 0.50, 0.75, 1
    T = 50    # 10, 50, 100
    m, widths, demands, max_width = random_instance( n, c, T*n )

    N1 = sum( demands )
    N2 = 2 * ( int( sum( widths[i] * demands[i] for i in range(m) ) / max_width ) + 1 )

    ff_rolls = solve_cutting_stock_first_fit( m, widths, demands, max_width )
    NFF = len(ff_rolls)

    print( f'  number of types: {m}' )
    print( f'N1 (total demand): {N1}' )
    print( f'               N2: {N2}' )
    print( f'        FIRST-FIT: {NFF}' )

    max_seconds = 10

    print( '───────────┬────────────┬───────┬───────┬───────┬──────────┬──────────┬──────┬───────' )
    print( 'model      │ status     │  vars │ conss │  cuts │   obj lb │   obj ub │  gap │   time' )
    print( '───────────┼────────────┼───────┼───────┼───────┼──────────┼──────────┼──────┼───────' )

    print( '== demand' )
    solve_cutting_stock_mip( m, widths, demands, max_width, N1, max_seconds= max_seconds )
    solve_cutting_stock_mip( m, widths, demands, max_width, N2, max_seconds= max_seconds )
    solve_cutting_stock_mip( m, widths, demands, max_width, N2, max_seconds= max_seconds, symmetry_breaking= True )
    solve_cutting_stock_mip( m, widths, demands, max_width, NFF, max_seconds= max_seconds, symmetry_breaking= True, initial_solution= ff_rolls )

    print( '>= demand' )
    solve_cutting_stock_mip( m, widths, demands, max_width, N1, max_seconds= max_seconds, demand_geq= True )
    solve_cutting_stock_mip( m, widths, demands, max_width, N2, max_seconds= max_seconds, demand_geq= True )
    solve_cutting_stock_mip( m, widths, demands, max_width, N2, max_seconds= max_seconds, symmetry_breaking= True, demand_geq= True )
    solve_cutting_stock_mip( m, widths, demands, max_width, NFF, max_seconds= max_seconds, symmetry_breaking= True, demand_geq= True, initial_solution= ff_rolls )

    # print( 'column generation' )
    # solve_cutting_stock_column_generation( m, widths, demands, max_width, draw_states= True )

    print( '───────────┴────────────┴───────┴───────┴───────┴──────────┴──────────┴──────┴───────' )
