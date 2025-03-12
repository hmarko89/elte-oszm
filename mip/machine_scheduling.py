import mip
import mip.model
import itertools as it

from time import perf_counter

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

def __log( model:mip.Model, ncuts:int, time:float ) -> None:
    """
    Prints log.

    Args:
        - model: mip model
        - ncuts: number of cuts (generated constraints)
        - time:  execution time
    """
    print( f'{model.name:10s} │ {model.status.name:10s} │ {model.num_cols:5d} │ {model.num_rows:5d} │ {ncuts:5d} | {model.objective_bound:8.1f} | {model.objective_value:8.1f} | {model.gap:4.2f} │ {time:6.2f}' )

def __separation_algorithm( p:list[int], C:list[int] ):
    """
    Separation algorithm.

    Queyranne, M. (1993). Structure of a simple scheduling polyhedron. Mathematical Programming, 58(1), 263-285.

    Args:
        - p: list of processing times
        - C: list of completion times (from LP-relaxation)

    Returns:
        - best_set: a subset that maximizes the submodular function, or None, if the maximum is 0
    """
    best_set   = None
    best_value = 0
    curr_set   = []
    curr_value = 0
    delta      = 0

    for j in sorted( range(len(p)), key= lambda i : C[i] ):
        curr_set.append(j)
        delta += p[j]
        curr_value += p[j]*(delta-C[j])

        if best_value < curr_value:
            best_value = curr_value
            best_set   = curr_set[:] # copy!
    
    return best_set

class SchedulingCutGenerator(mip.ConstrsGenerator):
    """Class to generate submodular inequalities."""
    
    def __init__( self, p:list, C:list ):
        """
        Class to generate submodular inequalities.

        Args:
            - p: list of processing times
            - C: list of completion time variables
        """
        assert len(p) == len(C), 'lists are of different lengths!'

        self.p = p
        self.C = C
        self.num_cuts = 0

    def generate_constrs( self, model:mip.Model, depth:int = 0, npass:int = 0 ):
        """Adds the most violated cut to the problem, if any."""

        # translate variables
        raise NotImplementedError( 'function generate_constrs is not fully implemented' ) # TODO [Exercise 1.2]

        # call separation procedure
        raise NotImplementedError( 'function generate_constrs is not fully implemented' ) # TODO [Exercise 1.2]
                
        # add cut, if any
        raise NotImplementedError( 'function generate_constrs is not fully implemented' ) # TODO [Exercise 1.2]

        self.num_cuts += 1

def schedule_jobs_on_a_single_machine( processing_times:list[int], weights:list[int], separation:bool= False, max_seconds= mip.INF ) -> None:
    """
    Solves scheduling problem "1 || sum w_jC_j" as a MIP with Python-MIP.

    NOTE: This problem can be solved in polynomial time (jobs should be scheduled in order of non-increasing ratios w/p).
          This is just a proof-of-concept for branch-and-cut.
    
    Args:
        - processing_times: list of processing times
        - weights:          list of weights
        - separation:       should we separate cuts?
    """
    # initialize
    n = len(processing_times)
    M = sum(processing_times)
    
    JOBS = range(n)
    
    # BUILD MODEL
    model = mip.Model( f'BIGM{"-SEP" if separation else ""}' )

    # completion time variables: p[j] <= C[j] <= M
    raise NotImplementedError( 'function schedule_jobs_on_a_single_machine is not fully implemented' ) # TODO [Exercise 1.1]

    # objective: weighted sum of completion times
    raise NotImplementedError( 'function schedule_jobs_on_a_single_machine is not fully implemented' ) # TODO [Exercise 1.1]

    # precedence variables: y[i][j] = 1 <=> job i precedes job j (NOTE: i<j)
    raise NotImplementedError( 'function schedule_jobs_on_a_single_machine is not fully implemented' ) # TODO [Exercise 1.1]

    # no-overlap constraints: y[i][j] = 1 => C[i] <= C[j] - p[j] and y[i][j] = 0 => C[j] <= C[i] - p[i]
    raise NotImplementedError( 'function schedule_jobs_on_a_single_machine is not fully implemented' ) # TODO [Exercise 1.1]

    # separation
    if separation:
        raise NotImplementedError( 'function schedule_jobs_on_a_single_machine is not fully implemented' ) # TODO [Exercise 1.2]
    
    # SOLVE PROBLEM
    model.verbose = 0
    start = perf_counter()
    model.optimize( max_seconds= max_seconds )
    end = perf_counter()

    num_cuts = model.cuts_generator.num_cuts if model.cuts_generator != None else 0

    __log( model, num_cuts, end-start )

# EXERCISES
# 1.1) Complete function schedule_jobs_on_a_single_machine to solve problem 1 || sum w_jC_j as a MIP.
# 1.2) Extend function schedule_jobs_on_a_single_machine to separate submodular inequalities during global search.

if __name__ == '__main__':
    p, w, d, r = random_instance( 12 )

    print( '───────────┬────────────┬───────┬───────┬───────┬──────────┬──────────┬──────┬───────' )
    print( 'model      │ status     │  vars │ conss │  cuts │   obj lb │   obj ub │  gap │   time' )
    print( '───────────┼────────────┼───────┼───────┼───────┼──────────┼──────────┼──────┼───────' )

    schedule_jobs_on_a_single_machine( p, w, separation= False, max_seconds= 10 )
    #schedule_jobs_on_a_single_machine( p, w, separation= True,  max_seconds= 10 )

    print( '───────────┴────────────┴───────┴───────┴───────┴──────────┴──────────┴──────┴───────' )
    