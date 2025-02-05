from math import sqrt

def __decode_slitherlink_string( task:str ) -> list[list[int]]:
    """
    Decodes the given instance for Slither Link.
    
    Args:
        - task: an instance for Slither Link encoded as a string

    Returns:
        - the grid (as a list of row-lists)
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

def __draw_slitherlink( grid:list[list[int]], loop:list[tuple[int,int]]= None ) -> None:
    """
    Draws the given task (and solution) for Slither Link.

    Args:
        - grid:     the grid (as a list of row-lists)
        - solution: list of loop edges
    """
    print( '!!! todo !!!' )

def __solve_slitherlink( grid:list[list[int]] ) -> list[tuple[int,int]]:
    """
    Solves Slither Link.

    Args:
        - grid: the instance table (as a list of row-lists) for Slither Link

    Returns:
        - solution: list of the loop edges
    """
    print( '!!! todo !!!')

    return []

def solve_slitherlink( task:str, draw_task:bool= False, draw_solution:bool= False ) -> None:
    """
    Solves Slither Link.
    
    Args:
        - task:          instance for Slither Link encoded as a string
        - draw_task:     should we draw the the task?
        - draw_solution: should we draw the the solution?

    Returns:
        - the solution encoded as a string
    """
    # process (and draw) task
    grid = __decode_slitherlink_string( task )
    if draw_task:
        __draw_slitherlink( grid )

    # solve problem (and draw solution)
    solution = __solve_slitherlink( grid )
    if draw_solution:
        __draw_slitherlink( grid, solution )

if __name__ == '__main__':
    TASKS = [
        '2a12a31c3b1a2c2a202a',
        'b3a3a21222a22a122a33a2a3',
        '33a23a32c2b2b20b31a33332b0b22b2b231d3',
        'a3a2a2a1c31a2322222222a321b22a2d232a3b2a2a',
        'b223a3323a22b21a1b333a22a22b1b3c2b3b1c3303b33d3a11b22d32a3d2d202b1d333a',
        'a2a232a2e2b2b33123b1c3b10a1a13a2a2a3a31c2a3222223b2a1a21322a32b1a2a2e2c2a33d3',
        '23b2b332d02b3232d3b2a321a1a2a2a2a22a2d3a3313b2a2b232a2e3a2a22b23d22b3a32a12a3a123a22e2a13232b3a1d32a12c1e1c3c22b31d23c2g2a2a2a3a3322202022a3a2c32a2a2b22b222a2232c22a',
        '3g2e3b2a213b3e131a21b30a1b3c3a232a2a2a03232a1f23a3b133b322c22f0222d221b3a2b22b1a3e3a3121a222a203b2d2a3c2b1a1a22a2b2232a1c22c3e33a2b2a3a2a22221d2a23c2a2h',
        'b23223b23f23a32a2f13a3223a2a31a1c3121a12g3233d32323201a1a32a2a1c0a212b2d21323a1c32a2b12a3d1d2b21a2a3a1f2a223d2a31f03a3a2120b2c33c2f2b2222221332131b2a2c3a322e2103e2a12a2b31323b223d231a11b1a2323b12a2a33a2b11a1b13222a212a1c3a21b3a12b22b3232c2a1c1a222a2c221c22c222a13b1b3a21a223a2c2a1312b232e312b',
        'a3a333b1222b23f21b3b31c1b2122b2a12d2c21332d21d23a12a3d2f32d32a0a3a23c2a22a2d1f322222b0b22a22a1222e2a2b312a2123b3c2a1c2a32a313b2a233b22a3b12d3b1d13232c112a02a13202a12e2a2b2a222c1a13d3b1b2f2b011a2233a32a22b21e32a1a1b3c123a3a23b2322a2d3d3d2222c21c2c1a222a1c2f31322a32322a3a32b0d3a3',
    ]

    task = TASKS[0]
    
    print( f'task = \'{task}\'')

    solve_slitherlink( task, draw_task= True, draw_solution= True )
