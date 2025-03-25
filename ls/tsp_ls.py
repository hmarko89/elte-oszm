import networkx as nx
import random
import itertools as it
import math
import matplotlib.pyplot as plt

import matplotlib.animation as animation

VERBOSITY_LEVEL = 1 # 0: off, 1: relevant, 2: detailed

def random_euclidean_graph( nnodes:int, seed:int= 0 ) -> nx.DiGraph:
    """
    Returns a random directed complete graph with the given number of nodes.
    Each node has the attribute 'pos' with the coordinates of the node.
    Each edge has the attribute 'cost' with the Euclidean distance of the corresponding nodes.

    Args:
        - nnodes: desired number of nodes
        - seed:   random seed

    Return:
        directed complete graph with node attributes 'pos', and edge attributes 'cost'.
    """
    # initialize
    random.seed( seed )

    NODES = range(nnodes)

    # CREATE GRAPH
    graph = nx.DiGraph()

    # generate random coordinates 
    coords = { u : (random.randint(0,100),random.randint(0,100)) for u in NODES }

    # add nodes to the graph with attribute 'pos'
    for u in NODES:
        graph.add_node( u, pos= coords[u] )

    # add edges to the graph with attribute 'cost'
    for (u,v) in it.permutations(graph.nodes,2):
        graph.add_edge( u, v, cost= math.dist( coords[u], coords[v] ) )

    return graph

def tetrahedron_instance( n:int, m:int ) -> nx.DiGraph:
    """
    Return the corresponding tetrahedron graph (with 3(n+m)-2 nodes).

    Hougardy, S., & Zhong, X. (2021). Hard to solve instances of the euclidean traveling salesman problem. Mathematical Programming Computation, 13, 51-74.

    Args:
        - n: n-parameter of the tetrahedron graph
        - m: m-parameter of the tetrahedron graph
        
    Return:
        directed complete graph with node attributes 'pos', and edge attributes 'cost'.
    """
    graph = nx.DiGraph()

    # nodes
    for i in range(n):
        graph.add_node( len(graph.nodes), pos= (n - i/2, i*math.sqrt(3)/2) )
        graph.add_node( len(graph.nodes), pos= (n/2 - i/2, (n-i)*math.sqrt(3)/2) )
        graph.add_node( len(graph.nodes), pos= (i, 0) )

    for j in range(1,m):
        graph.add_node( len(graph.nodes), pos= (j*n/(2*m), j*n/(2*math.sqrt(3)*m) ) )
        graph.add_node( len(graph.nodes), pos= (n - j*n/(2*m), j*n/(2*math.sqrt(3)*m) ) )
        graph.add_node( len(graph.nodes), pos= (n/2, n*math.sqrt(3)/2 - j*n/(math.sqrt(3)*m) ) )

    graph.add_node( len(graph.nodes), pos= (n/2, n/(2*math.sqrt(3)) ) )

    # edges
    pos = nx.get_node_attributes( graph, 'pos' )
    for (u,v) in it.permutations(graph.nodes,2):
        graph.add_edge( u, v, cost= math.dist( pos[u], pos[v] ) )

    return graph

def __edgelist( nodes:list[int] ) -> list[tuple[int,int]]:
    """
    Returns the edges of the tour given as a sequence of nodes.

    Args:
        - nodes: a Hamiltonian tour as a permutation of the nodes

    Return:
        a Hamiltonian tour as a sequence of edges
    """
    return [ (nodes[i-1],nodes[i]) for i in range(1,len(nodes)) ] + [ (nodes[-1],nodes[0]) ]

def __evaluate_solution( graph:nx.DiGraph, solution:list[int] ) -> float:
    """
    Returns the cost of the given solution.
    
    Args:
        - graph:    networkx digraph (with 'cost' edge attribute)
        - solution: a permutation of the nodes

    Return:
        - sum of the edge costs
    """
    return sum( graph.edges[edge]['cost'] for edge in __edgelist(solution) )

def __log( operator:str, objval:float ) -> None:
    """
    Prints log.
    
    Args:
        - operator: name of the local search operator
        - objval:   current objective value
    """
    print( f'{operator[:20]:20s} │ {objval:8.2f}' )

def __log_table( config:str= 'm' ) -> None:
    """
    Prints log table.
    
    Args:
        - config: 't' for top rule, 'h' for header, 'm' for midrule, 'b' for bottomrule
    """
    if VERBOSITY_LEVEL == 0:
        return
    
    for c in config:
        if c == 't':
            print( '─────────────────────┬────────────' )
        elif c == 'h':
            print( 'operator             │ objval     ' )
        elif c == 'm': 
            print( '─────────────────────┼────────────' )
        elif c == 'b':        
            print( '─────────────────────┴────────────' )

def __animate_search( graph:nx.DiGraph, solutions:list[list[int]] ) -> None:
    """
    Creates an animation from the given solutions and shows it.
    
    Args:
        - graph:     networkx digraph (with 'pos' and 'cost' attributes)
        - solutions: list of Hamiltonian tours given as permutations of the nodes
    """
    fig, ax = plt.subplots()

    pos = nx.get_node_attributes( graph, 'pos' )

    def update(frame):
        ax.clear()    
        nx.draw_networkx_nodes( graph, pos, node_size= 50, ax= ax )
        nx.draw_networkx_edges( graph, pos, edgelist= __edgelist(solutions[frame]), ax= ax )
        plt.xlabel( f'Length: {__evaluate_solution( graph, solutions[frame] ):.2f}' )

    _ = animation.FuncAnimation( fig, update, frames= len(solutions), interval= 500, repeat= False )

    plt.show()

def __improve_by_node_relocations( graph:nx.digraph, solution:list ):
    """
    Tries to improve the given solution by node relocations.

    Args:
        - graph:    networx directed graph
        - solution: a Hamiltonian tour as a permutation of the nodes

    Return:
        - best_solution: best found solution (a permutation of the nodes)
        - best_cost:     cost of the best solution
        - improved:      improved?
    """
    assert len(graph) == len(solution), 'solution does not fit to graph!'

    init_cost     = __evaluate_solution( graph, solution )
    best_cost     = init_cost
    best_solution = solution[:] # copy !
    improved      = False

    # check all index permutations
    for (i,j) in it.permutations( range(1,len(solution)), 2 ): # NOTE : keep 0 in the first place!
        # relocate node from position i to position j
        working_solution = solution[:i] + solution[i+1:]                               # "remove" element from position i
        working_solution = working_solution[:j] + [solution[i]] + working_solution[j:] # "insert" element to position j

        # evaluate solution
        working_cost = __evaluate_solution( graph, working_solution )

        # update best solution, if possible
        if working_cost + 0.001 < best_cost:
            best_cost     = working_cost
            best_solution = working_solution[:] # copy !
            improved      = True
            
            if 2 <= VERBOSITY_LEVEL:
                __log( '', best_cost )

    if improved:
        __log( 'relocate node', best_cost )
    
    return best_solution, best_cost, improved

def __improve_by_node_swaps( graph:nx.digraph, solution:list ):
    """
    Tries to improve the given solution by node swaps.

    Args:
        - graph:    networx directed graph
        - solution: a Hamiltonian tour as a permutation of the nodes

    Return:
        - best_solution: best found solution (a permutation of the nodes)
        - best_cost:     cost of the best solution
        - improved:      improved? (bool)
    """
    assert len(graph) == len(solution), 'solution does not fit to graph!'

    init_cost     = __evaluate_solution( graph, solution )
    best_cost     = init_cost
    best_solution = solution[:] # copy !
    improved      = False

    for (i,j) in it.combinations( range(1,len(solution)), 2 ): # NOTE : keep 0 in the first place!
        working_solution = solution[:]
        working_solution[i] = solution[j]
        working_solution[j] = solution[i]

        working_cost = __evaluate_solution( graph, working_solution )

        if working_cost + 0.001 < best_cost:
            best_cost     = working_cost
            best_solution = working_solution[:] # copy !
            improved      = True

    if improved:
        __log( 'swap nodes', best_cost )
    
    return best_solution, best_cost, improved

def __improve_by_2_opt( graph:nx.digraph, solution:list ):
    """
    Tries to improve the given solution by 2-opt.

    Args:
        - graph:    networx directed graph
        - solution: a Hamiltonian tour as a permutation of the nodes

    Return:
        - best_solution: best found solution (a permutation of the nodes)
        - best_cost:     cost of the best solution
        - improved:      improved? (bool)
    """
    assert len(graph) == len(solution), 'solution does not fit to graph!'

    init_cost     = __evaluate_solution( graph, solution )
    best_cost     = init_cost
    best_solution = solution[:] # copy !
    improved      = False

    for (i,j) in it.combinations( range(len(solution)), 2 ): # NOTE : keep 0 in the first place!
        working_solution = solution[:i] + solution[i:j][::-1] + solution[j:]

        working_cost = __evaluate_solution( graph, working_solution )

        if working_cost + 0.001 < best_cost:
            best_cost     = working_cost
            best_solution = working_solution[:] # copy !
            improved      = True

    if improved:
        __log( '2-opt', best_cost )
    
    return best_solution, best_cost, improved

def local_search( graph:nx.DiGraph, draw_progress:bool= True, draw_solutions:bool= False ) -> list[int]:
    """
    Solves TSP with a simple local-search procedure.

    NOTE: This is a proof-of-concept implementation.
          For efficiency, it would be better
          - to use, for example, doubly linked lists instead of python lists;
          - not to copy solutions;
          - to evaluate only the delta cost of the operation instead of the full tour; etc.

    Args:
        - graph:          networkx digraph (with 'pos' and 'cost' attributes)
        - draw_progress:  should we draw the cost evolution over iterations?
        - draw_solutions: should we draw solutions?

    Returns:
        - best found solution (a permutation of nodes)
    """
    # init
    solutions = []

    # create primitive initial solution
    solution = list( graph.nodes )
    random.shuffle( solution )
    solutions.append( solution[:] )
    
    __log( 'initial', __evaluate_solution( graph, solution ) )

    # improve solution
    while True:
        solution, cost, improved = __improve_by_node_relocations( graph, solution )
        #solution, cost, improved = __improve_by_node_swaps( graph, solution )
        #solution, cost, improved = __improve_by_2_opt( graph, solution )

        if not improved:
            break

        solutions.append( solution[:] )

    # visualize results
    if draw_progress:
        plt.xlabel( 'Iterations' )
        plt.ylabel( 'Cost' )
        plt.plot( [ __evaluate_solution( graph, solution ) for solution in solutions ] )
        plt.show()

    if draw_solutions:        
        __animate_search( graph, solutions )

    return solution

if __name__ == '__main__':
    graph = random_euclidean_graph( 30 )
    
    __log_table( 'thm' )

    local_search( graph, draw_solutions= True )
    
    __log_table( 'b' )

# FYI: optimal solution values for random_euclidean_graph(n):
#
#                11: 284.65     21: 354.40     31: 488.63     41: 511.48      60: 598.22
#                12: 296.56     22: 354.44     32: 491.26     42: 512.28      70: 627.60
#  3: 191.11     13: 297.13     23: 354.45     33: 491.67     43: 515.49      80: 687.79
#  4: 193.70     14: 297.81     24: 370.30     34: 491.71     44: 522.10      90: 722.55
#  5: 244.41     15: 300.48     25: 404.66     35: 492.12     45: 522.28     100: 758.56
#  6: 249.96     16: 305.05     26: 416.62     36: 501.79     46: 534.62     110: 791.41
#  7: 251.18     17: 306.31     27: 449.81     37: 502.62     47: 536.01     120: 838.39
#  8: 251.18     18: 324.09     28: 455.02     38: 510.96     48: 547.35     130: 876.79
#  9: 256.84     19: 332.72     29: 473.85     39: 511.20     49: 549.40     140: 921.44
# 10: 281.54     20: 346.15     30: 477.89     40: 511.21     50: 558.00     150: 941.17
