import mip
import networkx as nx
import itertools as it

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# There is a product that requires a part to be processed in multiple stations.
# Now, we want to make a lot of this product.
#
# There is a robot that moves the parts between workstations, one at a time.
# We need to plan the movement of this robot.
# The travel times between stations are given.
# For each workstation, the minimum and maximum time the workpiece can spend there are also given.
# The solution (i.e., the movement of the robot) must be periodic.
# The goal is to minimize the takt time.
#
# ────────────────────────────────────────────────────────────────────────────────
#              <-- a robot transports the parts between positions -->
# ─┬───────────────┬──────────────────────┬──────────────────────┬──────────────┬─
#
#  IN >>> [ Work station 1 ] >>> [ Work station 2 ] >>> [ Work station 3 ] >>> OUT

def solve( product_route:list[dict], travel_time:int ) -> None:
    """
    Minimizes the takt time of the robot for the given product route.

    Args:
        - product_route: route (sequence of stations)
        - travel_time:   uniform travel time between two adjacent stations
    """
    # init
    stations = product_route[1:-1]
    nstations = len(stations)
    STATIONS = range(nstations)

    # BUILD GRAPH
    D = nx.DiGraph()

    # nodes
    D.add_node( 'START' )
    D.add_node( 'IN' )
    D.add_nodes_from( [f'begin_{i}' for i in STATIONS ] )
    D.add_nodes_from( [f'end_{i}' for i in STATIONS ] )
    D.add_node( 'OUT' )
    D.add_node( 'END' )

    # node positions
    position = dict()
    position['START']  = 0
    position['IN']  = 0
    position['OUT'] = nstations + 1
    position['END'] = 0
    for i in STATIONS:
        position[f'begin_{i}'] = i+1
        position[f'end_{i}'] = i+1

    # edges
    D.add_edge( 'START', 'IN' )
    D.add_edge( 'IN', f'begin_{0}' )
    D.add_edge( f'end_{nstations-1}', 'OUT' )
    D.add_edge( 'OUT', 'END' )

    for i in STATIONS:
        D.add_edge( 'OUT', f'end_{i}' )
        D.add_edge( f'end_{i}', 'END' )

        if 0 < i:
            D.add_edge( f'end_{i-1}', f'begin_{i}' )

    for (i,j) in it.product(STATIONS,STATIONS):
        D.add_edge( f'begin_{i}', f'end_{j}' )

    # BUILD MODEL
    M = sum( stations[i]['max_time'] for i in STATIONS ) + 2 * travel_time * (len(product_route)-1) # big-M

    model = mip.Model( sense= mip.MINIMIZE )

    # takt time variable
    taktvar = model.add_var( name= 'takt', var_type= mip.CONTINUOUS, obj= 1.0 )

    # node time variables
    t = { node : model.add_var( name= f't_{node}', var_type= mip.CONTINUOUS ) for node in D.nodes }

    model += t['START'] == 0
    model += t['END'] == taktvar

    # edge variables
    x = { (i,j): model.add_var( name= f'x_{i}_{j}', var_type= mip.BINARY ) for (i,j) in D.edges }        

    # flow conservation constraints
    for i in D.nodes:
        if i != 'END':
            model += mip.xsum( x[edge] for edge in D.out_edges(i) ) == 1

        if i != 'START':
            model += mip.xsum( x[edge] for edge in D.in_edges(i) ) == 1

    # travel time
    for (i,j) in D.edges:
        model += t[i] + travel_time * abs( position[i] - position[j] ) <= t[j] + (1 - x[(i,j)])*M

    # time warp variables and constraints
    y = { i: model.add_var( name= f'y_{i}', var_type= mip.BINARY ) for i in STATIONS }

    for i in STATIONS:
        # minimum time at station
        model += stations[i]['min_time'] <= t[f'end_{i}'] - t[f'begin_{i}'] + (1 - y[i])*M
        model += t[f'end_{i}'] - t[f'begin_{i}'] <= stations[i]['max_time'] + (1 - y[i])*M

        # maximum time at station
        model += stations[i]['min_time'] <= t[f'end_{i}'] - t[f'begin_{i}'] + taktvar + y[i]*M
        model += t[f'end_{i}'] - t[f'begin_{i}'] + taktvar <= stations[i]['max_time'] + y[i]*M

        # for the sake of correct drawing in the case of 'OPT <= min_time'
        model += 1 <= t[f'end_{i}'] - t[f'begin_{i}'] + (1- y[i])*M
        model += 1 <= t[f'begin_{i}'] - t[f'end_{i}'] + y[i]*M

    # SOLVE
    model.optimize()

    if model.status not in [ mip.OptimizationStatus.OPTIMAL, mip.OptimizationStatus.FEASIBLE ]:
        print( f'! model status: {model.status}' )
        model.write( 'takt_time.lp' )

    # DRAW SOLUTION
    _, ax = plt.subplots()

    for i in STATIONS:
        if 0.5 < y[i].x:
            ax.add_patch( Rectangle( (t[f'begin_{i}'].x, 10*position[f'begin_{i}'] +2), t[f'end_{i}'].x - t[f'begin_{i}'].x, 6, facecolor = 'lightgreen', fill=True ) )

        else:
            ax.add_patch( Rectangle( (0, 10*position[f'end_{i}'] +2), t[f'end_{i}'].x, 6, facecolor = 'wheat', fill=True) )
            ax.add_patch( Rectangle( (t[f'begin_{i}'].x, 10*position[f'begin_{i}'] +2), taktvar.x -t[f'begin_{i}'].x, 6, facecolor = 'wheat', fill=True) )

    for (i,j) in [ edge for edge in D.edges() if 0.5 < x[edge].x ]:
        plt.plot( (t[i].x, t[j].x), (10*position[i] +5, 10*position[j] +5), color='black', linewidth=2 )

    # labels
    xticks = sorted({round(t[node].x) for node in t})
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(x) for x in xticks])

    ax.set_yticks([10 * i + 5 for i in range(len(product_route))])
    ax.set_yticklabels([station['id'] for station in product_route])

    plt.show()

if __name__ == '__main__':
    product_route = [
        { 'id': 'IN',             'min_time': None, 'max_time': None },
        { 'id': 'work station 1', 'min_time': 160,  'max_time': 180  },
        { 'id': 'work station 2', 'min_time': 160,  'max_time': 180  },
        { 'id': 'work station 3', 'min_time': 160,  'max_time': 180  },
        { 'id': 'OUT',            'min_time': None, 'max_time': None },
    ]

    travel_time = 10

    solve( product_route, travel_time )
