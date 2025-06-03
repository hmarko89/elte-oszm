import mip
from tqdm import tqdm

from knapsack import solve_knapsack

# def random_instance( n:int, capacity:int, seed:int= 0 ):
#     random.seed(seed)

#     for i in range(n)

def solve_bpp_with_ffd( capacity:int, items:list[int] ) -> list[list[int]]:
    """
    Solves the given instance for the Bin Packing Problem with the First-Fit Decreasing heuristic.
    
    Args:
        - capacity: uniform bin capacity
        - items:    list of items (item sizes)

    Returns:
        - list of bins, where each bin is a list of items
    """
    bins:list[list[int]] = []

    for item in sorted( items, reverse= True ):
        for bin in bins:
            if sum( bin ) + item <= capacity:
                bin.append( item )
                break
        else: # no bin found
            bins.append( [ item ] )

    return bins

def solve_bpp_with_mip( capacity:int, items:list[int] ) -> list[list[int]]:
    # init
    n = len(items)
    N = range(n)

    # initial columns
    columns = [ [ int(i==j) for j in N ] for i in N ]

    def get_packing( column:list[int] ):
        """Returns the packing corresponding to the given column."""
        return [ items[i] for i in N if column[i] ]

    # BUILD MODEL
    model = mip.Model( 'BPP', sense= mip.MINIMIZE )
    model.verbose = 0

    # initial variables
    # NOTE: use integers instead of binaries to avoid problems with handling upper bounds
    x = [ model.add_var( name= f'x_{j}', var_type= mip.INTEGER, obj= 1 ) for j in range(len(columns)) ]

    # initial constraints
    conss = [ model.add_constr( 1 <= mip.xsum( x[j] * column[i] for j, column in enumerate(columns) ), name= f'cover_{i}' ) for i in N ]

    # COLUMN GENERATION
    pbar = tqdm( bar_format='{desc}' )
    pbar.n = 1.0
    pbar.last_print_n = 1.0
    pbar.update(0)

    # solve LP iteratively
    iter = 0
    while True:
        iter += 1

        # solve the LP-relaxation of the problem
        model.optimize( relax= True )

        # get dual values
        master_objval = model.objective.x
        dual_values = [ conss[i].pi for i in N ]

        # solve subproblem (pricing problem)
        sub_objval, column = solve_knapsack( dual_values, items, capacity, binary= True )

        # add new pattern to the problem, if any
        if sub_objval <= 1 + model.opt_tol:
            break

        mip_column = mip.Column( conss, column ) # create column from pattern
        x.append( model.add_var( name= f'x_{len(columns)}', var_type= mip.INTEGER, obj= 1, column= mip_column ) ) # create variable based on column
        columns.append( column )

        # update progress bar
        pbar.n = round( master_objval, 4 )
        pbar.set_description( f'[Column Generation] Iteration: {iter} | Objective value: {master_objval:8.4f} | Reduced cost: {sub_objval:8.4f} | Time: {pbar.format_dict["elapsed"]:.2f}' )
        pbar.refresh()  # required to refresh display

    pbar.close()

    # solve MIP
    model.optimize()

    return [ get_packing(packing) for j, packing in enumerate(columns) if 0.5 < x[j].x ]

if __name__ == '__main__':
    capacity = 1000
    items = [ 495, 474, 473, 472, 466, 450, 445, 444, 439, 430, 419, 414, 410, 395, 372, 370, 366, 366, 366, 363, 361, 357, 355, 351, 350, 350, 347, 320, 315, 307, 303, 299, 298, 298, 292, 288, 287, 283, 275, 275, 274, 273, 273, 272, 272, 271, 269, 269, 268, 263, 262, 261, 259, 258, 255, 254, 252, 252, 252, 251 ]

    ffd_bins = solve_bpp_with_ffd( capacity, items )
    print( f'[First-Fit Decreased] Number of bins used: {len(ffd_bins)}' )

    mip_bins = solve_bpp_with_mip( capacity, items )
    print( f'[Column Generation] Number of bins used: {len(mip_bins)}' )
