from math import sqrt

def __decode_masyu_string( task:str ) -> list[list[int]]:
    """
    Decodes the given instance for Masyu.
    
    Args:
        - task: an instance for Masyu encoded as a string

    Returns:
        - the grid (as a list of row-lists)
    """
    cells = []

    for char in task:
        if not char.isalpha():
            raise f'unexpected character ({char}) in task'
        
        if char.isupper():
            cells.append( char )
        else:
            cells.extend( None for _ in range(96,ord(char)) )

    n = int(sqrt(len(cells)))

    assert len(cells) == n*n, f'could not parse task "{task}" succesfully'

    return [ cells[n*i:n*(i+1)] for i in range(n) ]

def __draw_masyu( grid:list[list[int]], loop:list[tuple[int,int]]= None ) -> None:
    """
    Draws the given task (and solution) for Masyu.

    Args:
        - grid:     the grid (as a list of row-lists)
        - solution: list of loop edges
    """
    print( '!!! todo !!!' )

def __solve_masyu( grid:list[list[int]] ) -> list[tuple[int,int]]:
    """
    Solves Masyu.

    Args:
        - grid: the instance table (as a list of row-lists) for Masyu.

    Returns:
        - solution: list of the loop edges
    """
    print( '!!! todo !!!' )

    return []

def solve_masyu( task:str, draw_task:bool= False, draw_solution:bool= False ):
    """
    Solves Masyu.
    
    Args:
        - task:          instance for Masyu encoded as a string
        - draw_task:     should we draw the task?
        - draw_solution: should we draw the solution?
    """
    # decode task
    grid = __decode_masyu_string( task )
    if draw_task:
        __draw_masyu( grid )

    # solve problem (and draw solution)
    solution = __solve_masyu( grid )
    if draw_solution:
        __draw_masyu( grid, solution )

if __name__ == '__main__':
    TASKS = [
        'dWBWaWbWcBcWaWWaWWgBb',
        'fWaWWaWfWWbWWcWaBeWbWaBcBbWaWWaWaWWaWbBc',
        'bWjWcWdWWbWcBaBaWkBcWgWaBc',
        'jBiBaBcBdBcWbWaWaWWfWiWaBa',
        'eBaWWbWeWBaBbWWeWcWaWbWaWWbWaBeWiBWaWWaWaWBcWaWaWaWaWaBeWeWa',
        'BeWbBbWaWkWbBbWbBaWcWjWWaWaBhBaWaWaWgWaWaWbBhBaWa',
        'jWWfBcWBWtWBaBaWbWcWcWbBbBbWdWbWcWdWeBf',
        'BWgWbWWaWBWbWBBfWcWBbWbWBWWWWWbWaWbWaWfWBWcWbWaBdWWaBbWaWbBbBbWaBdWgBdWcBWBbWWaBWWfWaBWWbWeWcWaBeBWaBbWdBWBaWcWaBWcWaWaWjWaBWWaWBcWbBeWB',
        'aWeWbWWkWaBbWaBaWaWbBWgBbWgWgBcWoWWWWbWWWdWbWiWaWaWbWeBWdWaWdWbBBaBbWbWaBhWqBgBcWaWjBhBBcBdWb',
        'gBbWeBcWdBgBaWaWeBfWfBkBdWaBnBdBaBWdBeBBgBkBcWWaBcBiBbWdBbWeWbBfWcWbWfWbWgWWfWWhWaB',
        'aWfWWbWhWWcWaWBcWaWWaWWBaWbWWbWaWaBbBaBWaBaWBbWWBcWaBBbBiWWdWaBWBWaWbBWWdWWeWdWWBcWWWBcBcWBWbWWbBdWbWBeWpBcWWaWbWWBBWcBaWeBaBbBaWbBdWiWWbWaBBaWbWWbWaWcBaWdWaWaWaWWaBWdBdWWBaBeWWdWeWaBcWaWaBWeBgBaWdBaBbWbBfWbWaWfWbWbWWbWeWBWbWgWbWcB',
        'bWcWeWbWkBcWeWWbWhWcWaBdWaBbBWbBfBaWbBbBcWWbWaWaWcWfWdBjBbBcWcBbBaWbWeBcBaBeWaBbBeWaBcBgBbWaWfBbWWWaWtWaWWeBbWaWbBcWbBbBBdWaWbWdWaBiWeWWfBdWbBWWBWWcWeWgWcBaWbWaWdWaWaWaWeWbWbWbWcWcWaWbBbWeWeWh',
        'BdBbWeBhWeWWfWWaWbBbWeWbWcBcWaWWaBcBaWcBbWmWdWbBeBaWaBiWWfWjBBbWaWcBdBWfWbBWcWBbBfWeBgWbWaWdBdWbWdWaBaWiWcWWdWcBeWaWcWdWaWbWWcWWiWlBaBaWWcBaBbWcBdBcWBdWWbWfWdBeBbWaBbWcWbBeWhWgBeB',
        'bWbBfWcBcWbWcBWBWcWWaBWaWWBaWBjBaWeWbWcBWbBaBdWcWWbWcWaWeBbWWBWdWbBbWWfWWbWcWWaWWdBWaBWbWhBeBeWdWWBaBfBdWaWWaWaWfBdBaBbWaWbWcWaWdWlWkBBhBbBbWaWaWBWbWWaBWaBaBWaWBbWWaWWhWaWWcWBWWcWbWWBWBWaWWaWBcBWaBeWbBaWbWhWbWdWcBWaBcWaWdWWaWjWcWWBaWcWcBWWBaWBWaWgBbWaWBWbBcBcBaWbWWBeWBWbWcBWWaBWcBWaBaWiBcWbWeWBbWBfWWcWbWaBWaBWeBWaBWcWWcBaWbWBcBWcWWbWWdWeWbWaBjWWbWaWdWb',
        'dBaWbWbWbWeWeBhWaWbWcWiBcWdWaBcBbWcBcWWcWBcWBaBaWdWaWaWcWcBbWfBbWdBaWaWaWdWWaBgBdWcWdWeBaBhWbBaBbBWWeBaBbBaBaWjBaWeWgWaWWBcWaBfWbWaBaBcWdWWcWeWeWbBWWhWBaWdWkBhBdWbBaBbWWcWcWdWWhWgBWdWWWbWWiBeBeWWbWaWWbWeBdWgWeWbWgWWaWaBcWWdWaWbBaWfWWaWWaBbWWbWaWfWfWmBdWaWBdWaBcWWcBbWdWeBeWbBjBaWbWaWdWbBcWBaBjBaWe',
        'eBhWaBdWcBmWiWbWfWWWgBaBWaWaWbBbBfWcWhWeBWeWBWWaWdBkBaWfBaBgBWcWaBbWbBcWbWaWWBcBbWbBoBWWcBaBdBBdBhWeWbBWcBbBaBaWbWbBdWeWiWeBcWbWaWWbWbWbWWfWfWeBfBaBcWWeWbWaWbWaWaBaWgBhBWaWfBaWcWbWbWaWWeWaWWbBaWbBhWbBWeWbWWcBWWeWbWaWaWaBbWgWBaWaWWWfWcWbWbWkWhWaBcBbBWWfWWbWkWWbBaBbBWWcWaWdBgWWeWcWbBBfWfBdWe',
    ]

    task = TASKS[0]
    
    print( f'task = \'{task}\'')

    solve_masyu( task, draw_task= True, draw_solution= True )
