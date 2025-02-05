from math import sqrt

def __decode_binairo_string( task:str ) -> list[list[int]]:
    """
    Decodes the given instance for Binairo.

    Args:
        - task: an instance for Binairo encoded as a string

    Returns:
        - the grid filled with 0/1/None (as a list of row-lists)
    """
    cells = []

    for char in task:
        if char.isnumeric():
            cells.append( int(char) )
        elif char.isalpha():
            cells.extend( None for _ in range(96,ord(char)) )

    n = int(sqrt(len(cells)))

    assert len(cells) == n*n, f'could not parse task "{task}" succesfully'

    return [ cells[n*i:n*(i+1)] for i in range(n) ]

def __encode_binairo_grid( grid:list[list[int]] ) -> str:
    """
    Encodes the given solution for Binairo as a string.

    Args:
        - grid: the grid as a list of row-lists

    Returns:
        - the string that encodes the grid
    """    
    return ''.join( ''.join( map( str, row ) ) for row in grid )

def __print_binairo( grid:list[list[int]] ) -> None:
    """
    Prints the given instance or solution for Binairo.
    
    Args:
        - grid: task or solution grid (as a list of lists)
    """
    n = len( grid )

    CHARS = '01·' # white|black|empty
        
    print( f'┌{"─"*(2*n+1)}┐' )

    for i in range(n):
        print( f'│ {" ".join( CHARS[grid[i][j]] if grid != None and grid[i][j] != None else CHARS[2] for j in range(n))} │' )

    print( f'└{"─"*(2*n+1)}┘' )

def __solve_binairo( grid:list[list[int]] ) -> list[list[int]]:
    """
    Solves Binairo.

    Args:
        - grid: the grid as a list of row-lists

    Returns:
        - the solution grid filled with 0/1   
    """

    print( '!!! todo !!!' )

    return grid

def solve_binairo( task:str, print_task:bool= False, print_solution:bool= False ) -> str:
    """
    Solves Binairo.
    
    Args:
        - task:           encoded instance for Binairo
        - print_task:     should we print the task?
        - print_solution: should we print the solution?

    Returns:
        - solution encoded as a string
    """
    # process (and print) task
    grid = __decode_binairo_string( task )
    if print_task:
        __print_binairo( grid )

    # solve problem (and print solution)
    solution = __solve_binairo( grid )
    if print_solution:
        __print_binairo( solution )

    return __encode_binairo_grid( solution )

if __name__ == '__main__':
    TASKS = [
        'f1a1b1e1a0g1d11b',
        '00f1c1h1i1b01',
        'e00c11m0b0a00a00j1a1b11d1d1b',
        'a0d1d00b0b00j1a1c1e1b0a0i0a0a0b',
        'a0c00b1a0q01b1a1b1f0a11d0f0a1b01g1c1g0b0a1a1c1b',
        'c00e1a11a0a1g0c0f1c1a1g1a1a1l1e0c1c1f0e1e',
        'c0a0d1b000f1e1b0e0i00e0a0a0h1g0a1b0f0a0d0a001s10a0d10a1g0c0b0a11m11a1a1b1f1d0b0c1b0b1a',
        'a0d0b1b1b1e0d111b0b00i0l1e1a1b0b1g1j1n0e00g1a0b0a00c1d1f1a1o0a00b00b1f0e11c1a1b',
        'e1h0a10b1a1b1b11a1c1a0i0f0d01a1a0e01b1b1b1b0a1a0e0o00e1a1d0g1b1c1a01a0d1g1m1c0e00a1a1b0a10a0a1d10c1f1f1g1a0d11b1b11a1g0c1a1d0a0b11a1e1g0c1d01b1b01l1e0b1c0a0a0a0d1b1g01d0a0d11a1e11c1c0e0d0a11c0',
        'c1e00a1i0d0f1b0f0c1b1b1k1c1f1a11c11j0b11j11c0m11b1c0b00n0f00a0e11a1l0b0d0a1d1c1b1h0c1c0g1a10b1d1c0d0a0b0b0a0a0a1a1b1c1a0j00d0a1b0a0c0c1g00i0c1l0g1a111a1g1a1a1a1a1b0e00c0f',
        'c11c1b1a0b0g00a1g1',
        'e1f1a1b11h0c1a0a1',
        'b1a1a1a0m11a0e0a0b',
    ]

    task = TASKS[0]
    
    solution = solve_binairo( task, print_task= True, print_solution= True )
    
    print( f'task     = \'{task}\'')
    print( f'solution = \'{solution}\'' )
    