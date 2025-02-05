from math import sqrt

import itertools as it

def __decode_futoshiki_string( task:str ) -> tuple[int,list[list[int]],list[tuple[int,int]]]:
    """
    Decodes the given instance for Futoshiki.
    
    Args:
        task: an instance for Futoshiki encoded as a string

    Returns:
        n:           the size of the grid, i.e., number of rows (= number of columns)
        grid:        the grid (as a list of row-lists)
        precedences: precedences (as a list of (predecessor,successor) pairs)
    """
    split = task.split(',')[:-1]
    n = int(sqrt(len(split)))
    grid = [ split[i*n:(i+1)*n] for i in range(n) ]
    precedences = []

    for (i,j) in it.product(range(n),range(n)):
        cell = i*n+j
        element = split[cell]

        c = element.find( next( filter(str.isalpha,element) ) ) if any( filter(str.isalpha,element) ) else len(element) # index of the first alphabetic character, if any

        if element[:c] == '0':
            grid[i][j] = None
        else:
            grid[i][j] = int(element[:c])

        if c == -1:
            continue

        if 'D' in element[c:]:
            precedences.append( ( (cell+n,cell) ) )
        if 'U' in element[c:]:
            precedences.append( ( (cell-n,cell) ) )
        if 'L' in element[c:]:
            precedences.append( ( (cell-1,cell) ) )
        if 'R' in element[c:]:
            precedences.append( ( (cell+1,cell) ) )            

    return n, grid, precedences

def __encode_futoshiki_grid( grid:list[list]) -> str:
    """
    Encodes the given instance/solution for Futoshiki as a string.

    Args:
        - grid: the grid as a list of row-lists

    Returns:
        - the string that encodes the grid
    """

    return ','.join( ",".join( str(cell) if cell != None else '0' for cell in grid[i] ) for i in range(len(grid) ) ) + ','

def __print_futoshiki( n:int, grid:list[list[int]], precedences:list[tuple[int,int]] ) -> None:
    """
    Prints the given instance/solution for Futoshiki.
    
    Args:
        - n:           the size of the grid, i.e., number of rows (= number of columns)
        - grid:        the grid (as a list of row-lists)
        - precedences: precedences (as a list of (predecessor,successor) pairs)

    Limitations:
        - n <= 16 (as we use hexadecimals)
    """

    CHARS = '·<>^v' # empty|left|right|above|below

    print( f'┌{"─"*(4*n-1)}┐' ) # top rule

    for i in range(n):            
        cells = ''.join( hex(grid[i][j])[2:].upper() if grid[i][j] != None else CHARS[0] for j in range(n) )
        precs = ''.join( CHARS[1] if (i*n+j,i*n+j+1) in precedences else ( CHARS[2] if (i*n+j+1,i*n+j) in precedences else ' ' ) for j in range(n-1) )

        print( f'│ {" ".join( f"{cells[j]} {precs[j]}" if j < n-1 else f"{cells[j]}" for j in range(n) )} │' )

        if i < n-1:
            print( f'│ {"   ".join( CHARS[3] if (i*n+j,(i+1)*n+j) in precedences else ( CHARS[4] if ((i+1)*n+j,i*n+j) in precedences else " " ) for j in range(n) ) } │' )
    
    print( f'└{"─"*(4*n-1)}┘' ) # bottom rule

def __solve_futoshiki( n:int, grid:list[list[int]], precedences:list[tuple[int,int]] ) -> list[list[int]]:
    """
    Solves Futoshiki.

    Args:
        - n:           the size of the grid, i.e., number of rows (= number of columns)
        - grid:        the grid (as a list of row-lists)
        - precedences: precedences (as a list of (predecessor,successor) pairs)

    Returns:
        - the solution grid (as a list of row-lists)    
    """

    print( '!!! todo !!!' )

    return grid

def solve_futoshiki( task:str, print_task:bool= False, print_solution:bool= False ) -> str:
    """
    Solves Futoshiki.
    
    Args:
        - task:           instance for Futoshiki encoded as a string
        - print_task:     should we print the task?
        - print_solution: should we print the solution?

    Returns:
        - the solution encoded as a string
    """

    # process (and print) task
    n, grid, precedences = __decode_futoshiki_string( task )
    if print_task:
        __print_futoshiki( n, grid, precedences )

    # solve (and print) task
    solution = __solve_futoshiki( n, grid, precedences )
    if print_solution:
        __print_futoshiki( n, solution, precedences )

    return __encode_futoshiki_grid( solution )

if __name__ == '__main__':
    TASKS = [
        "0D,0D,0,0,0,0R,0,0,0,0,0,4,0D,0,0,0U,0,0R,0,0L,0U,0,0U,0,0U,",
        "0,0L,0D,0,0,0,0,0DL,1,0,0,0,0R,0,0,0U,0,0,0,0,0U,0,0,0,0L,",
        "0,0,0,0,0L,0U,1,0,0,0,0R,0R,0,0U,0,0,0,0D,0U,0U,0,0U,0,0,3,",
        "0,0,0D,0,0D,0,0,0D,0DL,0,0,0R,0R,0,0,0,0D,0,0,0R,0,0,3L,0R,0,0,0R,0,0,0,0,0,0,0,0D,6R,0,0U,0,0RL,0,0D,2R,0,0UR,0,0,0,0L,",
        "0,0,0,0,0,0,0,4,0D,0U,0,0,0L,1,0,0,3R,0,0,0,0,0U,0RL,0D,0,0R,0,0U,0,0U,0,0,6,0,0U,0,0,0,0,0,0U,0L,0,0U,0R,0,0,0,0,",
        "5,0,0,0R,0RD,0R,0,0,5UR,0R,0,0L,0L,0,0,0,0R,0,0U,0,0,0R,0U,0,0U,0,0,0,0UD,0D,0,0U,0,0R,0,0D,0D,0D,0,0L,0L,0D,0,0,0,0,0R,0U,0,",
        "0D,0,0DL,5L,0,0,0,0,0,0RD,0D,0D,0,0,0RL,0,0U,0,0,0D,0,0R,0D,0UD,0RL,0URD,0D,0,0,0,0,0,0,0U,0,0,4D,0,0DL,0L,0,0RL,0,0,0,0,0,0,0,0,6URD,0R,0,0U,0,0,0D,0R,0,0,0,0L,0,0,0,0,0,0,0,4,0,0L,3,0,0,0,5,7R,0R,0R,0,",
        "6,0L,0,0,0,0L,0,0D,0D,0U,0R,0,0UD,0L,0L,0D,4,0L,0,0L,0,0,0,0R,4,0L,0,0R,0R,0,0,0,0L,7DL,0U,0U,0,0U,0U,0,0L,0,0D,0R,4,0D,0,0,0,2,0,0,6,0L,0D,0R,0D,0,0,0,0U,0,0,0,4,0D,0L,0R,0R,0R,0,0,0,0U,0R,0R,0,0,0R,0,0L,",
        "0,0L,0L,5,0L,0,0D,0L,0D,4,0R,3,0,0,0D,0,0,0,0,3,0R,0,0,0L,0,0,0,0,0L,0,0D,0L,0,0U,0U,0UD,0R,0R,0,0,0,0,0,0,0D,0,0R,8,0,0L,0UD,0D,0U,0,8,0,5,0,0,0R,0,0,0,0,0L,0R,0URD,6,0L,0U,0,0U,0,0L,0,0L,0R,0,0L,0R,0U,",
        "0D,0L,0R,0,0D,0,0,0,0,0R,0,0D,0D,0RL,0U,0,0L,0R,0,0UR,0,0D,0,0,0U,0,0,5DL,0,4,0U,0,0,0,11,0,0,1,0,9,0D,0UL,0R,0,7,0R,0U,0,11,0,0D,0R,0,0L,0,0D,0,0U,0R,0,0L,0L,0,0R,0,0D,0RD,0,0,0,0U,0,0D,0,0,0U,0L,0D,0,0D,0,0D,0,0R,0R,0U,0U,0,0R,4,0R,0D,0,0U,0R,0UR,0R,0,0U,3,0,0L,7,0L,0L,0D,0,0,0,0,0R,0U,0L,9,0R,0R,0R,0,0R,0U,0,",
        "0,0D,0,0D,0D,0,12,0,0L,0,0,0,0D,0D,8,0,0,0L,0,0U,0,0,0U,0,0R,6,0D,0U,0,0R,0U,0U,0,0U,0U,7R,0U,0D,0U,0,0,0,0U,0R,8,0U,0D,0D,3,0,0R,0D,0,0D,9,0D,12,0,0U,0L,0,0D,0L,0,0D,10,0,0,0,0R,2U,0,0,0D,0R,7D,0D,0,0D,0D,0RL,0U,0R,0,0UR,0,0D,0,0,0R,0U,0D,0,0U,0L,0,11,8R,0R,0,0,0L,0,0L,0R,0U,0U,0UL,0L,0,0,0R,0R,0RD,0D,0D,0,0,0L,0,0RL,0D,0,0D,8L,0L,0R,0,0D,0U,1,0D,0D,0U,0D,0L,0R,0,0L,0L,0L,0,0D,0,0,0,0,0L,0,0D,0R,0R,5,0U,0,0L,2,0R,0R,0,0,0U,0L,0R,0,0,0,0L,1,",
        "7R,0D,0L,0,0R,0,14,0,0,0R,0,0,0R,0D,0,0,0,0D,0L,0,0UD,0L,0L,0L,0U,0R,0U,0,0,0,0U,2,6R,0,0U,0,0D,0U,0U,0,0RL,9RD,0U,0,0D,0U,14RDL,0D,10,0,0,0D,0U,9,0,0L,0L,3,0L,0L,0,0,8,0,0L,9URL,0R,0,0U,0L,0R,0D,0,0,0D,0U,0,3,7,0U,0D,0,0U,0D,12R,0U,0D,0,0U,0D,0R,0U,0L,0L,0,0,0L,8,0,0L,0,0DL,0,0D,0,0D,0U,0,0L,0R,0U,0D,0U,0,0,0D,0,0R,0,0D,0R,0U,0L,0L,0R,0D,0L,0L,0,0,0R,0,0U,0L,0L,0,0,0U,0D,0U,0,0R,0,10,0,0R,7,0,0,0L,0D,4U,0,0R,0R,2,0,15,0U,0,0D,0,0,0R,0U,0,0,0D,0,0,0,0,0DL,0L,0,0,0,0L,0D,0,0RD,0,0,0R,0U,0U,0,0,0U,0UL,0L,0,9UDL,0L,0,11,6,0L,0,0R,0,0,12,0,8,4D,0D,0D,0R,0U,0,0,0R,9,0U,0L,0R,5,12,0,0,0,0,0,0U,",
    ]

    task = TASKS[0]

    solution = solve_futoshiki( task, print_task= True, print_solution= True )

    print( f'task     = \'{task}\'')
    print( f'solution = \'{solution}\'' )
