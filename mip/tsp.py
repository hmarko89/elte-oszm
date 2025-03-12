import networkx as nx
import random
import itertools as it
import math
import matplotlib.pyplot as plt
import mip

from time import perf_counter

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

def __draw_graph( graph:nx.DiGraph, edge_labels= None ) -> None:
    """
    Draws the given graph.
    
    Args:
        - graph:       directed graph
        - edge_labels: edge labels (optional)
    """
    nx.draw( graph, pos= nx.get_node_attributes( graph, 'pos' ), node_size= 50 )

    if edge_labels is not None:
        nx.draw_networkx_edge_labels( graph,  pos= nx.get_node_attributes( graph, 'pos' ), edge_labels= edge_labels, label_pos= 0.75 )

    plt.show( block= True ) # NOTE: blocks the execution!

def __nodesets( graph:nx.DiGraph ):
    """
    Returns an iterator for the non-trivial node subsets of the given graph.
    """
    return it.chain.from_iterable( it.combinations( graph.nodes, size ) for size in range(2,graph.number_of_nodes() ) )

def __log( model:str, status:str, nvars:int, nconss:int, ncuts:int, objval:float, time:float ) -> None:
    """
    Prints log.

    Args:
        - model:  name of the model
        - status: problem status name
        - nvars:  number of original variables
        - nconss: number of original constraints
        - ncuts:  number of cuts (generated constraints)
        - objval: objective value
        - time:   execution time
    """
    print( f'{model:10s} │ {status:10s} │ {nvars:5d} │ {nconss:5d} │ {ncuts:5d} │ {objval:6.1f} │ {time:7.4f}' )

def solve_tsp_dfj( graph:nx.DiGraph, draw_instance:bool= False, draw_solution:bool= False ) -> None:
    """
    Solves TSP as a MIP (DFJ formulation) with Python-MIP.
    All subtour-elimination constraints are added to the model in advance.

    Dantzig, G. B., Fulkerson, D. R., & Johnson, S. M. (1959). On a linear-programming, combinatorial approach to the traveling-salesman problem. Operations Research, 7(1), 58-66.
    
    Args:
        - graph:         networkx DiGraph, where each edge has the attribute 'cost'
        - draw_instance: should we draw the instance graph?
        - draw_solution: should we draw the optimal Hamiltonian tour?
    """
    if draw_instance:
        __draw_graph( graph )

    # BUILD MODEL
    model = mip.Model( 'tsp_dfj', sense= mip.MINIMIZE )
    model.verbose = 0

    # dictionary of arc-variables
    edge_costs = nx.get_edge_attributes( graph, 'cost' )
    x = { (u,v) : model.add_var( name= f'x_{u}_{v}', var_type= mip.BINARY, obj= edge_costs[(u,v)] ) for (u,v) in graph.edges }

    # constraints for nodes: in = out = 1
    for v in graph.nodes:
        model += mip.xsum( x[edge] for edge in graph.out_edges(v) ) == 1
        model += mip.xsum( x[edge] for edge in graph.in_edges(v) )  == 1

    # subtour-elimination constraints
    for subset in __nodesets(graph):
        vars = [ x[(u,v)] for (u,v) in graph.edges if u in subset and v in subset ]

        if 1 <= len(vars): # at least one variable is needed for a constraint
            model += mip.xsum(vars) <= len(subset)-1

    # SOLVE PROBLEM
    start = perf_counter()
    model.optimize()
    end = perf_counter()

    __log( 'DFJ', model.status.name, len(model.vars), len(model.constrs), 0, model.objective_value, end-start )

    if draw_solution and model.status in [ mip.OptimizationStatus.OPTIMAL, mip.OptimizationStatus.FEASIBLE ]:
        __draw_graph( graph.edge_subgraph( edge for edge in graph.edges if 0.9 < x[edge].x ) )

def solve_tsp_dfj_constraint_generation( graph:nx.DiGraph, draw_instance:bool= False, draw_solution:bool= False ) -> None:
    """
    Solves TSP as a MIP (DFJ formulation) with Python-MIP iteratively, that is, subtour-elimination constraints are added to the model when needed.
    
    Args:
        - graph:         networkx DiGraph, where each edge has the attribute 'cost'
        - draw_instance: should we draw the instance graph?
        - draw_solution: should we draw optimal Hamiltonian tour?
    """
    if draw_instance:
        __draw_graph( graph )

    # BUILD MODEL
    model = mip.Model( 'tsp_dfj_gen', sense= mip.MINIMIZE )
    model.verbose = 0

    # variables: x[(u,v)] = 1 if and only if edge (u,v) is in the tour
    edge_costs = nx.get_edge_attributes( graph, 'cost' )
    x = { (u,v) : model.add_var( name= f'x_{u}_{v}', var_type= mip.BINARY, obj= edge_costs[(u,v)] ) for (u,v) in graph.edges }

    # constraints: incoming = outgoing = 1
    for v in graph.nodes:
        model += mip.xsum( x[edge] for edge in graph.out_edges(v) ) == 1
        model += mip.xsum( x[edge] for edge in graph.in_edges(v) )  == 1

    # constraints: subtour-elimination for edges
    for (u,v) in it.combinations(graph.nodes,2):
        if (u,v) in graph.edges and (v,u) in graph.edges:
            model += x[(u,v)] + x[(v,u)] <= 1

    # CONSTRAINT GENERATION
    noriginal_conss = len(model.constrs)

    start = perf_counter()

    while True:
        raise NotImplementedError( 'function solve_tsp_dfj_constraint_generation is not fully implemented' ) # TODO [Exercise 1]

    end = perf_counter()

    __log( 'CONS-GEN', model.status.name, len(model.vars), noriginal_conss, len(model.constrs) - noriginal_conss, model.objective_value, end-start )

class SubTourCutGenerator(mip.ConstrsGenerator):
    """Class to generate cutting planes for the TSP."""
    def __init__( self, graph:nx.DiGraph, x:dict ):
        self.graph:nx.DiGraph = graph
        self.x:dict           = x
        self.ncuts:int        = 0
        self.maxcuts:int      = 255 # max cuts per round

        # for each node we store its farthest partner
        self.nodepairs = []
        
        edge_costs = nx.get_edge_attributes( graph, 'cost' )
        for node in graph.nodes:
            longest_edge = None

            for (i,j) in graph.out_edges(node):
                if longest_edge is None or edge_costs[longest_edge] < edge_costs[(i,j)]:
                    longest_edge = (i,j)

            self.nodepairs.append( (node,j) )

    def generate_constrs( self, model:mip.Model, depth:int= 0, npass:int= 0 ):
        """Procedure to generate cutting planes for the TSP."""

        xtrans = model.translate( self.x )

        flowgraph = nx.DiGraph()

        for arc in self.graph.edges:
            flowgraph.add_edge( arc[0], arc[1], capacity= xtrans[arc].x )
        
        pool = mip.CutPool()

        for (s,t) in self.nodepairs:           
            value, (subset, complementer) = nx.minimum_cut( flowgraph, s, t )

            if value <= 0.9:
                vars = [ xtrans[arc] for arc in self.graph.edges if arc[0] in subset and arc[1] in subset ]

                if 1 <= len(vars): # at least one variable is needed for a constraint
                    pool.add( mip.xsum( vars ) <= len(subset) - 1  )

                    if self.maxcuts <= len(pool.cuts):
                        break

        for cut in pool.cuts:
            model += cut
            self.ncuts += 1

def solve_tsp_mtz( graph:nx.DiGraph, strengthened:bool= False, separation:bool= False, draw_instance:bool= False, draw_solution:bool= False ) -> None:
    """
    Solves TSP as a MIP (MTZ formulation) with Python-MIP.

    Miller, C. E., Tucker, A. W., & Zemlin, R. A. (1960). Integer programming formulation of traveling salesman problems. Journal of the ACM (JACM), 7(4), 326-329.

    Desrochers, M., & Laporte, G. (1991). Improvements and extensions to the Miller-Tucker-Zemlin subtour elimination constraints. Operations Research Letters, 10(1), 27-36.
    
    Args:
        - graph:         networkx DiGraph, where each edge has the attribute 'cost'
        - strengthened:  should we use strengthened big-M constraints?
        - separation:    should we separate subtour-elimination constraints?
        - draw_instance: should we draw the instance graph?
        - draw_solution: should we draw the optimal Hamiltonian tour?
    """
    if draw_instance:
        __draw_graph( graph )

    # initialize
    n = nx.number_of_nodes(graph)

    # BUILD MODEL
    model = mip.Model( 'tsp_mtz', sense= mip.MINIMIZE )

    # variables: x[(u,v)] = 1 if and only if edge (u,v) is in the tour
    edge_costs = nx.get_edge_attributes( graph, 'cost' )
    x = { (u,v) : model.add_var( name= f'x_{u}_{v}', var_type= mip.BINARY, obj= edge_costs[(u,v)] ) for (u,v) in graph.edges }

    # constraints: incoming = outgoing = 1
    for v in graph.nodes:
        model += mip.xsum( x[edge] for edge in graph.out_edges(v) ) == 1
        model += mip.xsum( x[edge] for edge in graph.in_edges(v) )  == 1

    # variables: y[u] is an index of node u
    raise NotImplementedError( 'function solve_tsp_mtz is not fully implemented' ) # TODO [Exercise 2.1]

    # constraints: x(u,v) = 1 => y(u) + 1 <= y(v)
    if not strengthened:
        raise NotImplementedError( 'function solve_tsp_mtz is not fully implemented' ) # TODO [Exercise 2.1]
    else:
        raise NotImplementedError( 'function solve_tsp_mtz is not fully implemented' ) # TODO [Exercise 2.2]

    # SOLVE PROBLEM
    model.verbose = 0

    if separation:
       raise NotImplementedError( 'function solve_tsp_mtz is not fully implemented' ) # TODO [Exercise 2.3]

    start = perf_counter()
    model.optimize()
    end = perf_counter()

    __log( f'MTZ{"-S" if strengthened else ""}{"-SEP" if separation else ""}', model.status.name, len(model.vars), len(model.constrs), model.cuts_generator.ncuts if model.cuts_generator is not None else 0, model.objective_value, end-start )
    
    if draw_solution and model.status in [ mip.OptimizationStatus.OPTIMAL, mip.OptimizationStatus.FEASIBLE ]:
        __draw_graph( graph.edge_subgraph( edge for edge in graph.edges if 0.5 < x[edge].x ) )
    
def solve_tsp_gg( graph:nx.DiGraph, draw_instance:bool= False, draw_solution:bool= False) -> None:
    """
    Solves TSP as a MIP (GG formulation) with Python-MIP.

    Gavish, B., & Graves, S. C. (1978). The travelling salesman problem and related problems.
    
    Args:
        - graph:         networkx DiGraph, where each edge has the attribute 'cost'
        - draw_instance: should we draw the instance graph?
        - draw_solution: should we draw the optimal Hamiltonian tour?
    """
    raise NotImplementedError( 'function solve_tsp_gg is not fully implemented' ) # TODO [Exercise 3]

# EXERCISES
# 1) DFJ formulation.
#   - Implement a constraint generation procedure to iteratively add necessary subtour-elimination constraints.
#     Hint: nx.is_strongly_connected, nx.strongly_connected_components
# 2) MTZ formulation.
#   2.1) Implement function solve_tsp_mtz to solve TSP as a MIP with MTZ-formulation.
#   2.2) Use the strengthened inequalities.
#   2.3) Modify function solve_tsp_mtz to separate subtour elimination constraints during branch-and-bound.
# 3) GG formulation.
#   - Implement function solve_tsp_gg to solve TSP as a MIP with GG-formulation.

if __name__ == '__main__':
    D = random_euclidean_graph( 12 )
    #D = tetrahedron_instance(4,4)

    print( '───────────┬────────────┬───────┬───────┬───────┬────────┬────────' )
    print( 'model      │ status     │  vars │ conss │  cuts │ objval │    time' )
    print( '───────────┼────────────┼───────┼───────┼───────┼────────┼────────' )

    solve_tsp_dfj( D )
    #solve_tsp_dfj_constraint_generation( D )
    #solve_tsp_mtz( D )
    #solve_tsp_mtz( D, strengthened= True )
    #solve_tsp_mtz( D, separation= True )
    #solve_tsp_mtz( D, strengthened= True, separation= True )
    #solve_tsp_gg( D )

    print( '───────────┴────────────┴───────┴───────┴───────┴────────┴────────' )
