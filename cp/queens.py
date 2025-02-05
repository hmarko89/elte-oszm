from ortools.sat.python import cp_model

class QueensSolutionCallback( cp_model.CpSolverSolutionCallback ):
    """
    Solution printer for n-queens.

    Attributes:
        x:     variables (x[i] = j if and only if the queen of row i is in column j)
        n:     number of variables
        nsols: number of found solutions
    """
    def __init__( self, x ):
        super().__init__()

        self.x = x
        self.n = len(self.x)
        self.nsols = 0

    def on_solution_callback(self):
        """
        Draws solution.
        """
        CHARS = '·×' # empty | queen

        self.nsols += 1
        
        print( f'solution #{self.nsols}:' )
        for i in range(self.n):
            print( ' '.join( [ CHARS[1] if self.Value(self.x[i]) == j else CHARS[0] for j in range(self.n) ] ) ) 
        print( '' )

def solve_queens( n:int ) -> None:
    """
    Solves the n-queens puzzle as a CP with Google OR-Tools CP-SAT Solver.

    Args:
        n: size of the board (and the number of queens)
    """
    # create model
    model = cp_model.CpModel()

    # variables: x[i] = j if and only if the queen of row i is in column j
    # NOTE: by definition, there is only one queen in each row
    x = [ model.new_int_var( 0, n-1, f'x_{i}' ) for i in range(n) ]
 
    # constraints: queens cannot share columns
    model.add_all_different( x )

    # constraints: queens cannot share / diagonals
    model.add_all_different( x[i] + i for i in range(n) )
    
    # constraints: queens cannot share \ diagonals
    model.add_all_different( x[i] - i for i in range(n) )

    # solve
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve( model, solution_callback= QueensSolutionCallback(x) )

    print( f'status: {solver.status_name(status)} | total time: {solver.WallTime():.2f}' )

if __name__ == '__main__':
    solve_queens( 5 )
