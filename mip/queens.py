import mip

from time import perf_counter

def solve_queens( n:int ) -> None:
    """
    Solves the n-queens puzzle as a MIP with Python-MIP.
    
    Args:
        - n: size of the board (and the number of queens)
    """
    # initialize
    N = range(n)

    # BUILD MODEL
    model = mip.Model( f'{n}-queens' )

    # variables: x[i][j] == 1 if and only if there is a queen on square (i,j)
    x = [ [ model.add_var( name= f'x_{i}_{j}', var_type= mip.BINARY ) for j in N ] for i in N ]

    # constraints: exactly one queen per rows
    for i in N:
        model += mip.xsum( x[i][j] for j in N ) == 1, f'row_{i}'

    # constraints: exactly one queen per columns
    for j in N:
        model += mip.xsum( x[i][j] for i in N ) == 1, f'column_{j}'

    # constraints: at most one queen per / diagonals
    # NOTE: for each / diagonal, the sum of indices (i.e., i+j) is constant
    for s in range(0,2*n-1):
        model += mip.xsum( x[i][j] for i in N for j in N if i + j == s ) <= 1, f'sdiag_{s}'

    # constraints: at most one queen per \ diagonals
    # NOTE: for each \ diagonal, the difference of indices (i.e., i-j) is constant
    for d in range(-(n-1),n):
        model += mip.xsum( x[i][j] for i in N for j in N if i - j == d ) <= 1, f'ddiag_{d+n}'

    # no objective (feasibility problem)
    model.objective = 0

    # SOLVE PROBLEM
    model.verbose = 0
    opt_start = perf_counter()
    model.optimize()
    opt_end = perf_counter()

    print( f'status: {model.status.name} | total time: {opt_end-opt_start:.2f}' )

    # print solution
    if model.status in [ mip.OptimizationStatus.OPTIMAL, mip.OptimizationStatus.FEASIBLE ]:
        CHARS = '·×' # empty | queen
        for i in N:
            print( ' '.join( [ CHARS[1] if 0.5 < x[i][j].x else CHARS[0] for j in N ] ) )

# EXERCISES
# 1. Modify function solve_queens to get ALL feasible solutions.
#    (Hint: how can we discard a specific solution?)

if __name__ == '__main__':
    solve_queens( 5 )
