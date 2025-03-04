# elte-oszm
Auxiliary material for the course **Operációkutatás Számítógépes Módszerei** at ELTE.

```
├─ cp                         : exercises for constraint programming
│  ├─ send_more_money.py      :   cryptarithmetic puzzle (SEND + MORE = MONEY)
│  ├─ queens.py               :   n-queens puzzle
│  ├─ machine_scheduling.py   :   machine scheduling problems 
|  └─ rectangle_packing.py    :   rectangle packing problems
│
├─ mip                        : exercises for mixed-integer linear programming
│  ├─ knapsack.py             :   knapsack problem
│  ├─ queens.py               :   n-queens puzzle
|  └─ tsp.py                  :   travelling salesman problem
│
└─ puzzles                    : puzzle exercises for cp/mip
   ├─ binario.py              :   binario (takuzu)
   ├─ futoshiki.py            :   futoshiki (more or less)
   ├─ hitori.py               :   hitori
   ├─ kakurasu.py             :   kakurasu
   ├─ masyu.py                :   masyu
   ├─ skyscrapers.py          :   skyscrapers (skylines, towers)
   ├─ slitherlink.py          :   slither link (fences)
   └─ sudoku.py               :   sudoku
```

## Recommended Python packages

Python 3.9 (64-bit) or newer version is recommended.

### <a href="https://developers.google.com/optimization" target="_blank">Google OR-Tools</a>

```
python -m pip install ortools
```

### <a href="https://www.python-mip.com/" target="_blank">Python-MIP</a>

```
python -m pip install mip
```

### <a href="https://matplotlib.org/" target="_blank">Matplotlib: Visualization with Python</a>

```
python -m pip install matplotlib
```

### <a href="https://networkx.org/" target="_blank">NetworkX: Network Analysis in Python</a>

```
python -m pip install networkx
```
