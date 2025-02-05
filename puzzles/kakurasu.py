def __decode_kakurasu_string( task:str ) -> tuple[list[int],list[int]]:
    """
    Decodes the given instance for Kakurasu.

    Args:
        task: an instance for Kakurasu encoded as a string

    Returns:
        list of the side numbers for columns (left to right)
        list of the side numbers for rows (up to bottom)
    """
    numbers = list( map( int, task.split('/') ) )
    n = len( numbers ) // 2

    return numbers[:n], numbers[n:]

def __encode_kakurasu_grid( grid:list[list[int]] ) -> str:
    """
    Encodes the given solution for Kakurasu as a string.

    Args:
        - grid: the grid as a list of row-lists

    Returns:
        - the string that encodes the grid
    """    
    return '/'.join( '/'.join( map( str, row ) ) for row in grid )

def __print_kakurasu( colnums:list[int], rownums:list[int], grid:list[list[int]]= None ) -> None:
    """
    Prints the given instance and solution for Kakurasu.
    
    Args:
        - colnums: side numbers for columns
        - rownums: side numbers for rows
        - grid:    the solution grid (as a list of lists)
    """
    n = len( rownums )

    CHARS = ' ×' # empty|filled

    headers = []
    if n < 10:
        headers.append( list( range(1,n+1) ) )
    else:
        headers.append( list( map( lambda num : str(num // 10) if 10 <= num else ' ', range(1,n+1) ) ) )
        headers.append( list( map( lambda num : str(num % 10), range(1,n+1) ) ) )

    footers = []
    if max( colnums ) < 10:
        footers.append( colnums )
    else:
        footers.append( list( map( lambda num : str(num // 10) if 10 <= num else ' ', colnums ) ) )
        footers.append( list( map( lambda num : str(num % 10), colnums ) ) )
    
    for header in headers:
        print( '    ', ' '.join( map( str, header ) ) )
        
    print( f'   ┌{"─"*(2*n+1)}┐' )

    for i in range(n):
        print( f'{i+1:2d} │ {" ".join( CHARS[1] if grid != None and grid[i][j] == 1 else CHARS[0] for j in range(n))} │ {rownums[i]}' )

    print( f'   └{"─"*(2*n+1)}┘' )

    for footer in footers:
        print( '    ', ' '.join( map( str, footer ) ) )

def __solve_kakurasu( colnums:list[int], rownums:list[int] ) -> list[list[int]]:
    """
    Solves Kakurasu.

    Args:
        - colnums: side numbers for columns
        - rownums: side numbers for rows

    Returns:
        - the solution grid filled with 0/1   
    """
    print( '!!! todo !!!')

    return [ [ 1 for j in range(len(colnums)) ] for i in range(len(rownums)) ]

def solve_kakurasu( task:str, print_task:bool= False, print_solution:bool= False ) -> str:
    """
    Solves Kakurasu.
    
    Args:
        - task:           encoded instance for Kakurasu
        - print_task:     should we print the task?
        - print_solution: should we print the solution?

    Returns:
        - solution encoded as a string
    """
    # process (and print) task
    colnums, rownums = __decode_kakurasu_string( task )
    if print_task:
        __print_kakurasu( colnums, rownums )

    # solve problem (and print solution)
    solution = __solve_kakurasu( colnums, rownums )
    if print_solution:
        __print_kakurasu( colnums, rownums, solution )

    return __encode_kakurasu_grid( solution )

if __name__ == '__main__':
    TASKS = [
        '5/3/4/7/5/4/2/8',
        '10/1/1/3/10/5/1/1',
        '4/5/3/7/8/4/6/10/5/5',
        '9/2/9/2/13/5/7/6/9/8',
        '4/11/1/11/5/10/10/6/11/2/7/10',
        '16/13/4/6/18/13/13/11/5/8/16/14',
        '9/7/10/3/8/7/11/7/8/21/2/5/14/3',
        '20/13/12/4/23/12/16/21/11/24/15/13/11/13',
        '3/9/3/15/2/18/7/20/4/28/4/6/21/12/16/4',
        '31/18/30/19/28/22/7/13/11/21/15/9/16/18/32/14',
        '18/22/13/4/3/12/4/11/1/16/1/13/10/18/10/8/1/2',
        '19/2/17/14/10/27/20/21/12/19/38/1/31/5/26/30/8/9',
    ]

    task = TASKS[0]
    
    solution = solve_kakurasu( task, print_task= True, print_solution= True )
    
    print( f'task     = \'{task}\'')
    print( f'solution = \'{solution}\'' )
    