from math import sqrt

def __decode_hitori_string( task:str ) -> list[list[int]]:
    """
    Decodes the given instance for Hitori.
    
    Args:
        - task: an instance for Hitori encoded as a string

    Returns:
        - the grid (as a list of row-lists)
    """
    cells = []

    for char in task:
        if char.isnumeric():
            cells.append( int(char) )
        elif char.isalpha():
            cells.extend( None for _ in range(96,ord(char)) )

    n = int(sqrt(len(cells)))

    assert len(cells) == n*n, f'could not parse task "{task}" succesfully'

    return [ cells[n*i:n*(i+1)] for i in range(n) ]

def __encode_hitori_grid( grid:list[list] ) -> str:
    """
    Encodes the given instance/solution for Hitori as a string.

    Args:
        - grid: the grid as a list of row-lists

    Returns:
        - the string that encodes the grid
    """
    return 'todo'

def __print_hitori( grid:list[list[int]] ) -> None:
    """
    Prints the given instance/solution for Hitori.
    
    Args:
        - grid: the grid of the instance/solution for Hitori
    """
    CHARS = '×' # shaded

    n = len(grid)

    print( f'┌{"─"*(2*n+1)}┐' )
    for row in grid:
        print( f'│ {" ".join( map( lambda cell : str(cell) if cell != None else CHARS[0], row ) )} │' )
    print( f'└{"─"*(2*n+1)}┘' )

def __solve_hitori( grid:list[list[int]] ) -> list[list[int]]:
    """
    Solves Hitori.

    Args:
        - grid: the instance table (as a list of row-lists) for Hitori

    Returns:
        - the solution table (as a list of row-lists)    
    """
    print( '!!! todo !!!' )

    return grid

def solve_hitori( task:str, print_task:bool= False, print_solution:bool= False ) -> str:
    """
    Solves Hitori.
    
    Args:
        - task:           instance for Hitori encoded as a string
        - print_task:     should we print the task?
        - print_solution: should we print the solution?

    Returns:
        - the solution encoded as a string
    """
    # process (and print) task
    grid = __decode_hitori_string( task )
    if print_task:
        __print_hitori( grid )

    # solve problem (and print solution)
    solution = __solve_hitori( grid )
    if print_solution:
        __print_hitori( solution )

    return __encode_hitori_grid( solution )

if __name__ == '__main__':
    TASKS = [
        '1544333125311531243124553',
        '4242114542242345132441212',
        '5243144315241434132512244',
        '4244543213315435212434353',
        'a4178565a4783613642113895a7384573997a858a1686719556a2495167995664842775472118243638571478316a772a198',
        'a369575491958a69193987719a43456a76369682393831462327a749757692139459a9513473a263164923786aa4a5a6aa7a',
        '42123972525698a52321832a5a6393393a363723537595168a74a4684549a843429767223282a92695517352a8a7872a5a3a',
        'adcd654799a624e2aadb38eb1ce5f11e61bcf92d3caf487bc86cba1799a1dbe7a96fc859b2f63d89ebfead284b69ee3b4224dff68a61b24c182a7d865f231c5ab39178bec798a5d168a6c71c836a92d9846b2988c22311c67e7e9ba45e7d6f415d948b4c11e9c76f3fe678d21aab429e7',
        '65cfd41c67de48c68287154a7fce89be1631f819b12d14ceac8c32bc9c5bd36dbaea759acaf5ab71b8c525f5e5e2d529a282762c21bffa227ec5e3e87da2dfc6cbc3d95e9ce6e4eda8e1e79ca49dae5aa1af9a67b563dcf4191e868c8789842af38bd49ce6838d5c7d273d922bde6d8d4',
        'ba6bebb894ddf9954184ec3642b4f717fd15afc6d2e316b7abf9ce2428d31c1b71da131614129a93695f989c9ebefcf72f183ab65d2e2b367356ca28131718b1d16e15185d321b6cfa57b948324dfc58bd1c132ca8dab27df62449b6ec2d7ef4281a9896949bd735dc3635d47139d83ad',
        'a75d9daej58h43j42bh69242ad5ebcdja1hej6hkfddk5339eje8hh58b7g76accgbfi3hd26539ef71732e4fedd6kkfj24ii5j3dbh2akijb637fci8ea4c85df5ik982aej3fjdab36fg594cbe84a8cfkab628hhdae5ce3i21g1a4cigh25jig8i4jd5b9268efhjick6hjebbg1643ia35j287dgi433c1i6j2541di5ee8bg3kchaf86bg1cfae39j872kk3edid5gh57eki9463hd9bjg77j3c68g9f36caa9i68b7he4g7e6e6ag54a82k14c5d8f3gcg67i17j28425idhc9842bc69eh7412i9hfdd6jch5a27497ij5bgk4g388j',
        'di3d8kh4151k937j1cge7d4h35da836i393caf3j3g39c37fij7853k81i6ib4i8kef89bc2bh45b78ab3g7gb1dk4hcfk298cjk5ada79ag12a3ajhak8af6dj2f1i6g196a56kc1h14ef4a14b4c4gh4674543a286h6g456e127i2fjc417kekck2a8fa6aj4hkdkji6i45852c37cb5fck91jkg5jigegfdj8g1679gbcahf326aki7ea8fa52b7kcdf67dhj6iabde8d4dgj91j5kck67jdkfgj3kekdjeafk31ffg47cc246c548k8d8j83b8682c8gaf87f73b8bcba5bj74e67kd81cfifba7ek4d65hf34218hb1j161k1fg19gih71',
        '49ei4j2ae8e531472g42f646i5d5ce95a6jh1egba4353gaedh1f1i2ac739gj5gck46ii3if21adk7g2ha76616ijadabakh3h5b7ja9632achai6gb4bf66keg1h114e7jef631cde3gfdhgjcgad84gie9bgk6216edi6f6k6gj4656b6da14k86b8f1gh1e5j983ej2hjba56h845dacai5fj3b1fcckj52ed2bha89ejcik54ej3gfbj8j26g5d48c5a85789b8k538ef65b63e5f9had3c85h12k577igi23id1ie6i9iji4aihibj7ehf14ab579b311g1gk68df656d97364ejec8beae1j9j758cedekj28i4dfgcb471234aj875jh',
    ]

    task = TASKS[0]

    solution = solve_hitori( task, print_task= True, print_solution= True )
    
    print( f'task     = \'{task}\'')
    print( f'solution = \'{solution}\'' )
