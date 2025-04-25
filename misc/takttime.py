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
    # INIT
    stations = product_route[1:-1]
    nstations = len(stations)
    STATIONS = range(nstations)

    # big-M (calculated as the takt time of the straightforward solution)    
    M = sum( stations[i]['min_time'] for i in STATIONS ) + 2 * travel_time * (len(product_route)-1)

    # BUILD GRAPH
    D = nx.DiGraph()

    # nodes
    D.add_node( 'IN' )                                     # in event (source node)
    D.add_nodes_from( [f'start_{i}' for i in STATIONS ] )  # start events for the operations
    D.add_nodes_from( [f'finish_{i}' for i in STATIONS ] ) # finish events for the operations
    D.add_node( 'OUT' )                                    # out event
    D.add_node( 'END' )                                    # takt event (sink node)

    # node positions (for travel times)
    position = dict()
    position['IN'] = 0
    position['OUT'] = nstations + 1
    position['END'] = 0
    for i in STATIONS:
        position[f'start_{i}'] = i+1
        position[f'finish_{i}'] = i+1

    # mandatory edges (pick -> corresponding drop)
    D.add_edge( 'IN', f'start_{0}' )
    D.add_edges_from( (f'finish_{i-1}', f'start_{i}') for i in range(1,nstations) )
    D.add_edge( f'finish_{nstations-1}', 'OUT' )

    # selectable edges (some pick (or END) after some drop)
    D.add_edges_from( (f'start_{i}', f'finish_{j}') for (i,j) in it.product(STATIONS,STATIONS) )
    D.add_edges_from( ('OUT', f'finish_{i}') for i in STATIONS )

    D.add_edge( 'OUT', 'END' )
    D.add_edges_from( (f'start_{i}', 'END') for i in STATIONS )

    # BUILD MODEL
    model = mip.Model( sense= mip.MINIMIZE )

    # node time variables
    t = { node : model.add_var( name= f't_{node}', var_type= mip.CONTINUOUS ) for node in D.nodes }

    model += t['IN'] == 0
    model.objective = t['END']

    # edge variables
    x = { (i,j): model.add_var( name= f'x_{i}_{j}', var_type= mip.BINARY ) for (i,j) in D.edges }        

    # flow conservation constraints
    for i in D.nodes:
        if i != 'END':
            model += mip.xsum( x[edge] for edge in D.out_edges(i) ) == 1

        if i != 'IN':
            model += mip.xsum( x[edge] for edge in D.in_edges(i) ) == 1

    # travel time
    for (i,j) in D.edges:
        model += t[i] + travel_time * abs( position[i] - position[j] ) <= t[j] + (1 - x[(i,j)])*M

    # time wrap variables (y=1 <=> there is no time wrap)
    y = { i: model.add_var( name= f'y_{i}', var_type= mip.BINARY ) for i in STATIONS }

    # min-max time constraints
    for i in STATIONS:
        # min-max times within period (i.e., no time wrap)
        model += stations[i]['min_time'] <= t[f'finish_{i}'] - t[f'start_{i}'] + (1 - y[i])*M
        model += t[f'finish_{i}'] - t[f'start_{i}'] <= stations[i]['max_time'] + (1 - y[i])*M

        # min-max times through periods (i.e., time wrap)
        model += stations[i]['min_time'] <= t[f'finish_{i}'] - t[f'start_{i}'] + t['END'] + y[i]*M
        model += t[f'finish_{i}'] - t[f'start_{i}'] + t['END'] <= stations[i]['max_time'] + y[i]*M

        # for the sake of correct drawing in the case of 'OPT <= min_time'
        model += 1 <= t[f'finish_{i}'] - t[f'start_{i}'] + (1- y[i])*M
        model += 1 <= t[f'start_{i}'] - t[f'finish_{i}'] + y[i]*M

    # test (to forbid time wrap)
    # for var in y.values():
    #     model += var == 1

    # SOLVE
    model.optimize()

    if model.status not in [ mip.OptimizationStatus.OPTIMAL, mip.OptimizationStatus.FEASIBLE ]:
        print( f'model status: {model.status}' )
        model.write( 'takt_time.lp' )
        return

    # DRAW SOLUTION
    _, ax = plt.subplots()

    for i in STATIONS:
        if 0.5 < y[i].x:
            ax.add_patch( Rectangle( (t[f'start_{i}'].x, 10*position[f'start_{i}'] +2), t[f'finish_{i}'].x - t[f'start_{i}'].x, 6, facecolor = 'lightgreen', fill=True ) )

        else:
            ax.add_patch( Rectangle( (0, 10*position[f'finish_{i}'] +2), t[f'finish_{i}'].x, 6, facecolor = 'wheat', fill=True) )
            ax.add_patch( Rectangle( (t[f'start_{i}'].x, 10*position[f'start_{i}'] +2), t['END'].x -t[f'start_{i}'].x, 6, facecolor = 'wheat', fill=True) )

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
