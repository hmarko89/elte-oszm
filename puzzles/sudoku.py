import itertools as it

def __decode_sudoku_string( task:str ) -> list[list[int]]:
    """
    Decodes the given instance for Sudoku.
    
    Args:
        - task: an instance for Sudoku encoded as a string

    Returns:
        - the grid as a list of row-lists
    """
    cells = []

    for char in task:
        if char.isnumeric():
            cells.append( int(char) )
        elif char.isalpha():
            cells.extend( None for _ in range(96,ord(char)) )

    assert len(cells) == 81, f'could not decode task "{task}" succesfully'

    return [ cells[9*i:9*(i+1)] for i in range(9) ]

def __encode_sudoku_grid( grid:list[list[int]]) -> str:
    """
    Encodes the given instance/solution for Sudoku as a string.

    Args:
        - grid: the grid as a list of row-lists

    Returns:
        - the string that encodes the grid
    """
    string = ''

    nonempties = 0
    for (i,j) in it.product(range(9),range(9)):
        if grid[i][j] == None:
            nonempties += 1
            continue
            
        if 0 < nonempties:
            string += chr(96+nonempties)
            nonempties = 0

        string += f'{grid[i][j]}'
    
    if 0 < nonempties:
        string += chr(96+nonempties)

    return string

def __print_sudoku( grid:list[list[int]] ) -> None:
    """
    Prints the given instance/solution for Sudoku.
    
    Args:
        - grid: the instance/solution grid (as a list of row-lists) for Sudoku
    """
    CHARS = '·' # empty 

    for i in range(10):
        if i == 0:
            print( '┌───────┬───────┬───────┐' )

        elif i in [3,6]:
            print( '├───────┼───────┼───────┤' )

        elif i == 9:
            print( '└───────┴───────┴───────┘' )
            break

        for j in range(10):
            if j == 0:
                print( '│', end= '' )

            elif j in [3,6]:
                print( ' │', end= '' )

            elif j == 9:
                print( ' │' )
                break

            print( f' {grid[i][j] if grid[i][j] != None else CHARS[0]}', end= '' )

def __solve_sudoku( grid:list[list[int]] ) -> list[list[int]]:
    """
    Solves Sudoku.

    Args:
        - grid: the instance grid (as a list of row-lists) for Sudoku

    Returns:
        - the solution grid (as a list of row-lists)
    """
    from ortools.sat.python import cp_model

    n = 3 
    N = range(0,n*n)

    assert len(grid) == n*n, 'invalid matrix size!'

    # BUILD MODEL
    model = cp_model.CpModel()

    # variables: x[i][j] = the number written into cell (i,j)
    x = [ [ model.new_int_var( 1, n*n, f'x_{i}_{j}' ) for j in N ] for i in N ]

    # constraints: pre-given numbers
    for (i,j) in it.product(N,N):
        if grid[i][j] != None:
            model.add( x[i][j] == grid[i][j] )
    
    # constraints: each number occurs exactly once in a row
    for i in N:
        model.add_all_different( x[i][j] for j in N )

    # constraints: each number occurs exactly once in a column
    for j in N:
        model.add_all_different( x[i][j] for i in N )

    # constraints: each number occurs exactly once in a 3x3 subgrid
    for (p,q) in it.product(range(n),range(n)):
       model.add_all_different( x[i+n*p][j+n*q] for (i,j) in it.product(range(n),range(n)) )

    # SOLVE PROBLEM
    solver = cp_model.CpSolver()
    status = solver.solve( model )
    assert status == cp_model.OPTIMAL, f'status: {solver.status_name(status)}'

    # return solution
    return [ [ solver.value(x[i][j]) for j in N ] for i in N ]

def solve_sudoku( task:str, print_task:bool= False, print_solution:bool= False ) -> str:
    """
    Solves Sudoku.
    
    Args:
        - task:           instance for Sudoku encoded as a string
        - print_task:     should we print the task?
        - print_solution: should we print the solution?

    Returns:
        - the solution encoded as a string
    """
    # process (and print) task
    grid = __decode_sudoku_string( task )
    if print_task:
        __print_sudoku( grid )

    # solve problem (and print solution)
    solution = __solve_sudoku( grid )
    if print_solution:
        __print_sudoku( solution )

    return __encode_sudoku_grid( solution )

if __name__ == '__main__':
    TASKS = [
        'b4_6b3_5f4b7_8b5d2_1a5_3c6k3c1_2a4_7d3b1_3b9f2_1b5_8b',
        'a9a3a1c8b5_6_4e6c4b3_8b7b6_1a6a1a3a2a1_7b5b3_4b9c3e9_3_7b2c6a5a7a',
        '4a6_2_8c1c1_4a8b2d7a6a9_8d3b3_7e5_6b2d4_8a2a4d5b1a7_3c7c6_2_1a3',
        'b4c5c8a9a2a6a6b1a8b7a3_6c7_2e7e7_9c4_1a8b3a4b6a6a2a7a5c7c1b',
        '9g5c4_6_5d7a8a9a2b1e6a7_5a6a2a8_3b4_1a8_5k1g8_5a6_2a4_3a9',
        'a7a5_6e4_2b7a6_3d3b9b5f1_1a7c9a8_3f2b3b1d7_6a3b2_8e4_6a1a',
        'b3e6e5a2a8_5d3a4_1a7a6d3g8b6_2c1a4b6d5b2_1a8e8_9_4_7c',
        '8a3a6a2d4b1b3a2d9g2_1_3a2a1_9a3_8a5a3_9_5g2d8a9b1b3d7a3a4a2',
    ]

    task = TASKS[0]

    solution = solve_sudoku( task, print_task= True, print_solution= True )
    
    print( f'task     = \'{task}\'')
    print( f'solution = \'{solution}\'' )
