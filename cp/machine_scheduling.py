from ortools.sat.python  import cp_model

def random_instance( n:int, seed:int= 0 ) -> tuple[list[int],list[int],list[int],list[int]]:
    """
    Generates random instance for single machine scheduling problems, see Keha et al. (2009).
    
    Args:
        - n:    number of desired jobs
        - seed: random's seed

    Returns:
        - list of processing times
        - list of weights
        - list of due dates
        - list of release times
    """
    import random
    random.seed(seed)

    N = range(0,n)
    L = 0.5
    R = 0.8
    Q = 0.4

    # processing times
    p = [ random.randint(1,100) for _ in N ]
    P = sum( p )

    # weights
    w = [ random.randint(1,10) for _ in N ]

    # due dates
    d = [ random.randint( int(P*(L-R/2)), int(P*(L+R/2)) ) for _ in N ]

    # release dates
    r = [ random.randint( 0, int(P*Q) ) for _ in N ]

    return p, w, d, r

def __draw_schedule( processing_times:list[int], start_times:list[int] ) -> None:
    """
    Draws the given schedule.

    Args:
        - processing_times: list of processing times
        - start_times:      list of start times
    """
    raise NotImplementedError( 'drawing is not implemented' )

def __print_schedule( processing_times:list[int], weights:list[int], release_times:list[int], start_times:list[int] ) -> None:
    """
    Prints the given schedule.

    Args:
        - processing_times: list of processing times
        - weights:          list of weights
        - release_times:    list of release times
        - start_times:      list of start times
    """
    n = len(processing_times)

    print( '────┬─────┬─────┬─────┬───────────' )
    print( 'job │  w  │  p  │  r  │  interval ' )
    print( '────┼─────┼─────┼─────┼───────────' )
    for i in sorted( range(n), key= lambda i : start_times[i] ):
        print( f'{i:3d} │ {weights[i]:3d} │ {processing_times[i]:3d} │ {release_times[i]:3d} │ {start_times[i]:3d} -- {start_times[i]+processing_times[i]}')
    print( '────┴─────┴─────┴─────┴───────────' )

def schedule_jobs_on_a_single_machine( processing_times:list[int], weights:list[int], release_times:list[int] ) -> None:
    """
    Solves scheduling problem "1 | r_j | sum w_jC_j" as a CP with Google OR-Tools CP-SAT Solver.
    
    Args:
        - processing_times: list of processing times
        - weights:          list of weights
        - release_times:    list of release times
    """
    # initialize
    n = len(processing_times)
    H = sum(processing_times) + max(release_times) # upper bound on the makespan
    
    JOBS = range(n)
    
    # BUILD MODEL
    model = cp_model.CpModel()

    # variables: interval variables ~ start times
    jobs = [ model.new_fixed_size_interval_var(
        start= model.new_int_var( release_times[i], H, f'start_{i}' ),
        size=  processing_times[i],
        name=  f'job_{i}'
    ) for i in JOBS ]

    # constraint: jobs cannot overlap
    model.add_no_overlap( jobs )

    # objective: weighted sum of completion times
    model.minimize( sum( weights[i] * jobs[i].end_expr() for i in JOBS ) )
    
    # SOLVE PROBLEM
    solver = cp_model.CpSolver()
    #solver.parameters.log_search_progress = True
    status = solver.solve( model )

    print( f'status: {solver.status_name(status)} | objective: {int(solver.objective_value)} | total time: {solver.WallTime():.2f}' )

    if status in [ cp_model.FEASIBLE, cp_model.OPTIMAL ]:
        __print_schedule( processing_times, weights, release_times, [ solver.value(jobs[i].start_expr()) for i in JOBS ] )

def schedule_jobs_on_parallel_machines( processing_times:list[int], weights:list[int]= None, release_times:list[int]= None, nmachines:int= 2 ) -> None:
    """
    Solves scheduling problem "P || Cmax" as a CP with Google OR-Tools CP-SAT Solver.
    
    Args:
        - processing_times: list of processing times
        - weights:          (None) list of weights
        - release_times:    (None) list of release times
        - nmachines:        number of (parallel identical) machines
    """
    raise NotImplementedError( 'function is not implemented' )

# EXERCISES
# 1. Modify function schedule_jobs_on_a_single_machine to minimize the makespan of the schedule.
#    (Hint: model.add_max_equality)
# 2. Implement function schedule_jobs_on_parallel_machines to schedule jobs on parallel machines.
#    (Hint: model.new_optional_fixed_size_interval_var)
# -------------------------------------------------------------------------------------------------
# + Implement a function that solves a job-shop scheduling problem.
# + Implement function __draw_schedule for GANTT chart vizualization (see Plotly, for an example).

if __name__ == '__main__':
    # demo example
    p, w, d, r = [2,4,3,1], [1,1,1,1], None, [0,0,0,0]

    # random instances
    #p, w, d, r = random_instance( 16 )
    #p, w, d, r = random_instance( 17 ) # struggling (check log)

    # solve problem
    schedule_jobs_on_a_single_machine( p, w, r )

    #schedule_jobs_on_parallel_machines( p, w, r, 2 )
    