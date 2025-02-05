import itertools as it

def __decode_skyscrapers_string( task:str ) -> tuple[int,list[int],list[int],list[int],list[int],list[list[int]]]:
    """
    Decodes the given instance for Skyscrapers.

    Args:
        - task: an instance for Skyscrapers encoded as a string

    Returns:
        - size of the grid, i.e., the number of rows (= the number of columns)
        - list of the top side numbers for columns (left to right)
        - list of the bottom side numbers for columns (left to right)
        - list of the left side numbers for rows (up to bottom)
        - list of the right side numbers for rows (up to bottom)
        - the grid with pre-given numbers (as a list of row-lists)
    """
    split = task.split(',')

    around = list( map( lambda x : int(x) if x != '' else None, split[0].split('/') ) )
    n = len( around ) // 4
    top , bottom, left, right = around[0:n], around[n:2*n], around[2*n:3*n], around[3*n:4*n]

    grid = None

    if 1 < len(split): # grid may be not given
        cells = []

        for char in split[1]:
            if char.isnumeric():
                cells.append( int(char) )
            elif char.isalpha():
                cells.extend( None for _ in range( 96, ord(char) ) )

        assert len(cells) == n*n, f'could not parse task "{task}" succesfully'

        grid = []
        for i in range(n):
            grid.append( cells[n*i:n*(i+1)] )

    else:
        grid = [ [ None ] * n for _ in range(n) ]

    return n, top, bottom, left, right, grid

def __encode_skyscrapers_grid( grid:list[list[int]] ) -> str:
    """
    Encodes the given grid for Skyscrapers.
    
    Args:
        - a grid (as a list of row-lists) for Skyscrapers

    Returns:
        - the grid encoded as a string
    """
    N = range(len(grid))

    string = ''

    nonempties = 0
    for (i,j) in it.product(N,N):
        if grid[i][j] != None:
            if 0 < nonempties:
                string += chr(96+nonempties)
                nonempties = 0

            string += f'{grid[i][j]}'
        else:
            nonempties += 1
    
    if 0 < nonempties:
        string += chr(96+nonempties)

    return string

def __print_skyscrapers( n:int, top:list[int], bottom:list[int], left:list[int], right:list[int], grid:list[list[int]] ) -> None:
    """
    Prints the given instance/solution for Skyscrapers.
    
    Args:
        - size of the grid, i.e., the number of rows (=the number of columns)
        - list of the top side numbers for columns (left to right)
        - list of the bottom side numbers for columns (left to right)
        - list of the left side numbers for rows (up to bottom)
        - list of the right side numbers for rows (up to bottom)
        - the grid with pre-given numbers (as a list of row-lists)
    """    
    CHARS = '·' # empty

    print( f'    {" ".join( map( lambda num : str(num) if num != None else " ", top ) )}     ' )
    print( f'  ┌{"─"*(2*n+1)}┐  ' )

    for i in range(n):
        print( f'{left[i] if left[i] != None else " "} │ {" ".join( map( lambda num : str(num) if num != None else CHARS[0], grid[i] ) )} │ {right[i] if right[i] != None else " "}' )

    print( f'  └{"─"*(2*n+1)}┘  ' )
    print( f'    {" ".join( map( lambda num : str(num) if num != None else " ", bottom ) )}     ' )

def __solve_skyscrapers( n:int, top:list[int], bottom:list[int], left:list[int], right:list[int], grid:list[list[int]] ) -> list[list[int]]:
    """
    Solves the given instance for Skyscrapers.
    
    Args:
        - size of the grid, i.e., the number of rows (=the number of columns)
        - list of the top side numbers for columns (left to right)
        - list of the bottom side numbers for columns (left to right)
        - list of the left side numbers for rows (up to bottom)
        - list of the right side numbers for rows (up to bottom)
        - the grid with pre-given numbers (as a list of row-lists)

    Returns:
        - the filled grid (as a list of row-lists)
    """
    print( '!!! todo !!!')

    return grid

def solve_skyscrapers( task:str, print_task:bool= False, print_solution:bool= False ) -> str:
    """
    Solves Skyscrapers.
    
    Parameters:
        - task:           encoded instance for Skyscrapers
        - print_task:     should we print task?
        - print_solution: should we print solution?

    Returns:
        - solution encoded as a string
    """

    # process (and print) task
    n, top, bottom, left, right, grid = __decode_skyscrapers_string( task )
    if print_task:
        __print_skyscrapers( n, top, bottom, left, right, grid )

    # solve (and print) task
    solution = __solve_skyscrapers( n, top, bottom, left, right, grid )
    if print_solution:
        __print_skyscrapers( n, top, bottom, left, right, solution )

    return __encode_skyscrapers_grid( solution )

if __name__ == '__main__':
    TASKS = [
        '///2//3///2//4//////4///,s1b2b',
        '1/2/2/3/2/2/3/1/1/2/2/2/4/2/3/1',
        '/3//1/////3/1//////3',
        '////3/2///////4///,e4j',
        '3/5/2/1/2/2/1/2/3/2/3/2/1/3/2/2/1/3/2/2',
        '3//1//3///3//////2/4////4/',
        '4//3///////4//3//3/////2/4',
        '4/3/2/3/2/1/1/2/3/2/3/2/4/2/3/2/4/1/1/4/2/2/3/2,b1i2i1b2j',
        '4/3////3///4//4////2//3/2///3///2,a3ze3b',
        '/3/4/3//3//////2///4///2//4//2/4/,v1f1c2b',
    ]
    
    task = TASKS[0]
    
    solution = solve_skyscrapers( task, print_task= True, print_solution= True )
    
    print( f'task     = \'{task}\'')
    print( f'solution = \'{solution}\'' )
    