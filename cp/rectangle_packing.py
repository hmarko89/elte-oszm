from ortools.sat.python import cp_model

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from math import sqrt

def draw_rectangle_packing( container:tuple[int,int], rectangles:list[tuple[int,int]], positions:list[tuple[int,int]] ) -> None:
    """
    Draws rectangle packing.

    Args:
        - container:  size of the container as (width,height)
        - rectangles: list of rectangles as (width,height)
        - positions:  list of (x,y)-coordinates of the bottom-left corners
    """
    plt.figure()
    plt.xlim( 0, container[0] )
    plt.ylim( 0, container[1] )
    
    axis = plt.gca()
    axis.set_aspect( 'equal', adjustable= 'box' )

    for i in range(len(rectangles)):
        if positions[i] is not None:
            axis.add_patch( Rectangle( positions[i], rectangles[i][0], rectangles[i][1], facecolor='#78acff', ec='k', lw=2 ) )

    plt.show()

def solve_rectangle_packing_without_rotation( container:tuple[int,int], rectangles:list[tuple[int,int]] ) -> None:
    """
    Solves rectangle packing without rotation.

    Args:
        - container:  size of the container as (width,height)
        - rectangles: list of rectangles as (width,height)
    """
    n = len(rectangles)

    # CREATE MODEL
    model = cp_model.CpModel()

    # variables: x- and y-coordinates for the bottom-left corners
    x = [ model.new_int_var( 0, container[0] - rectangles[i][0], f'x_{i}' ) for i in range(n) ]
    y = [ model.new_int_var( 0, container[1] - rectangles[i][1], f'y_{i}' ) for i in range(n) ]

    # variables: intervals for projection on x- and y-axes
    xint = [ model.new_fixed_size_interval_var( x[i], rectangles[i][0], f'xint_{i}' ) for i in range(n) ]
    yint = [ model.new_fixed_size_interval_var( y[i], rectangles[i][1], f'yint_{i}' ) for i in range(n) ]

    # constraints: no overlap
    model.add_no_overlap_2d( xint, yint )

    # SOLVE PROBLEM
    solver = cp_model.CpSolver()
    #solver.parameters.log_search_progress = True
    status = solver.solve( model )

    print( f'status: {solver.status_name(status)} | total time: {solver.WallTime():.2f}' )

    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        draw_rectangle_packing( container, rectangles, [ ( solver.value(x[i]), solver.value(y[i]) ) for i in range(n) ] )

def solve_square_packing( container:tuple[int,int], squares_sizes:list[int] ) -> None:
    """
    Solves square packing.
    
    Args:
        - container:     size of the container as (width,height)
        - squares_sizes: list of the size of the squares
    """
    solve_rectangle_packing_without_rotation( container, [ (size,size) for size in squares_sizes ] )

def solve_perfect_squared_square( elements:list[int] ) -> None:
    """
    Solves perfect squared square problem.

    Args:
        - elements: list of the size of the squares

    References:
        - https://mathworld.wolfram.com/PerfectSquareDissection.html
        - Bouwkamp, C. J., & Duijvestijn, A. J. W. (1992). Catalogue of simple perfect squared squares of orders 21 through 25.
    """
    reduced_side = int(round(sqrt(sum( size**2 for size in elements ))))
    assert reduced_side**2 == sum( size**2 for size in elements ), 'total area check: squares cannot be arranged into a square'

    solve_square_packing( (reduced_side,reduced_side), elements )

def solve_rectangle_packing_with_rotation( container:tuple[int,int], rectangles:list[tuple[int,int]] ) -> None:
    """
    Solves rectangle packing with rotation.

    Args:
        - container:  size of the container as (width,height)
        - rectangles: list of rectangles as (width,height)
    """
    raise NotImplementedError( 'function is not implemented' )

# EXERCISES
# 1. Modify function solve_rectangle_packing_without_rotation to maximize the number of packed rectangles!
#    (See infeasible cases)
#    (Hint: model.new_optional_fixed_size_interval_var)
# 2. Implement function solve_rectangle_packing_with_rotation, where rectangles can be rotated by 90 degrees.
#    (Hint: model.new_int_var_from_domain with cp_model.Domain.from_values,
#           model.new_optional_interval_var,
#           model.add_allowed_assignments or only_enforce_if)

if __name__ == '__main__':
    # WITHOUT ROTATION

    # demo example
    
    solve_rectangle_packing_without_rotation( (6,7), [(2,3),(3,2),(1,4),(5,1),(3,5)] )

    # perferct rectangles

    #solve_rectangle_packing_without_rotation( (32,33), [ (i,i) for i in [1,4,7,8,9,10,14,15,18] ] ) # 9-square rectangle
    #solve_rectangle_packing_without_rotation( (65,47), [ (i,i) for i in [3,5,6,11,17,19,22,24,23,25] ] ) # 10-square rectangle

    # perfect squared squares

    #solve_perfect_squared_square( [2,4,6,7,8,9,11,15,16,17,18,19,24,25,27,29,33,35,37,42,50] ) # order: 21 | reduced size: 112
    #solve_perfect_squared_square( [2,3,4,6,7,8,12,13,14,15,16,17,18,21,22,23,24,26,27,28,50,60] )    # order: 22 | reduced size: 110
    #solve_perfect_squared_square( [1,2,3,4,6,8,9,12,14,16,17,18,19,21,22,23,24,26,27,28,50,60] )     # order: 22 | reduced size: 110
    #solve_perfect_squared_square( [4,8,9,10,12,14,17,19,26,28,31,35,36,37,41,47,49,57,59,62,71,86] ) # order: 22 | reduced size: 192
    #solve_perfect_squared_square( [1,2,3,4,5,7,8,10,12,13,14,15,16,19,21,28,29,31,32,37,38,41,44] )           # order: 23 | reduced size: 110
    #solve_perfect_squared_square( [1,2,7,8,12,13,14,15,16,18,19,20,21,22,24,26,27,28,32,33,38,59,80] )        # order: 23 | reduced size: 139
    #solve_perfect_squared_square( [1,15,17,24,26,30,31,38,47,48,49,50,53,56,58,68,83,89,91,112,120,123,129] ) # order: 23 | reduced size: 332
    #solve_perfect_squared_square( [3,4,5,6,8,9,10,12,13,14,15,16,17,19,20,23,25,32,33,34,40,41,46,47] ) # order: 24 | reduced size: 120
    #solve_perfect_squared_square( [1,2,3,4,5,8,9,14,16,18,20,29,30,31,33,35,38,39,43,51,55,56,64,81] )  # order: 24 | reduced size: 175
    #solve_perfect_squared_square( [3,4,5,6,8,9,10,12,13,14,15,16,17,19,20,23,25,27,32,33,34,40,41,73,74] ) # order: 25 | reduced size: 147

    # infeasible cases

    #solve_rectangle_packing_without_rotation( (4,4), [(3,3),(2,2)] ) # impossible to pack both rectangles
    #solve_rectangle_packing_without_rotation( (4,4), [(2,4),(4,2)] ) # rotation is needed

    # WITH ROTATION

    #solve_rectangle_packing_with_rotation( (4,4), [(2,4),(4,2)] )
    #solve_rectangle_packing_with_rotation( (15,23), [(2,3)]*57 )
    #solve_rectangle_packing_with_rotation( (19,29), [(2,3)]*91 )
    #solve_rectangle_packing_with_rotation( (86,52), [(5,9)]*99 ) # very hard
