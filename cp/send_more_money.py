from ortools.sat.python import cp_model

if __name__ == '__main__':
    """
    Solve the cryptarithmetic puzzle
           SEND
        +  MORE
        = MONEY
    as a CP with Google OR-Tools CP-SAT Solver.
    """
    # create model
    model = cp_model.CpModel()

    # variables
    S = model.new_int_var( 1, 9, 'S' ) # leading digit
    E = model.new_int_var( 0, 9, 'E' )
    N = model.new_int_var( 0, 9, 'N' )
    D = model.new_int_var( 0, 9, 'D' )
    M = model.new_int_var( 1, 9, 'M' ) # leading digit
    O = model.new_int_var( 0, 9, 'O' )
    R = model.new_int_var( 0, 9, 'R' )
    Y = model.new_int_var( 0, 9, 'Y' )

    # constraint: all letters are different digits
    model.add_all_different( [S,E,N,D,M,O,R,Y] )

    # constraint: SEND + MORE = MONEY
    model.add( 1000*S + 100*E + 10*N + D + 1000*M + 100*O + 10*R + E == 10000*M + 1000*O + 100*N + 10*E + Y )

    # solve
    solver = cp_model.CpSolver()
    status = solver.Solve( model )

    print( f'status: {solver.status_name(status)} | total time: {solver.WallTime():.2f}' )

    # print solution, if any
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print( f'   {solver.value(S)}{solver.value(E)}{solver.value(N)}{solver.value(D)}' )
        print( f'+  {solver.value(M)}{solver.value(O)}{solver.value(R)}{solver.value(E)}' )
        print( f'= {solver.value(M)}{solver.value(O)}{solver.value(N)}{solver.value(E)}{solver.value(Y)}' )
