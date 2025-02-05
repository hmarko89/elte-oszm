# elte-oszm
Auxiliary material for the course 'Operációkutatás Számítógépes Módszerei' at ELTE.

```
├─ cp                         : exercises for constraint programming
│  ├─ send_more_money.py      : cryptarithmetic puzzle (SEND + MORE = MONEY)
│  └─ queens.py               : n-queens puzzle
│
├─ mip                        : exercises for mixed-integer linear programming
│
└─ puzzles                    : puzzle exercises for cp and/or mip
   ├─ binario.py              : binario (takuzu)
   ├─ futoshiki.py            : futoshiki (more or less)
   ├─ hitori.py               : hitori
   ├─ kakurasu.py             : kakurasu
   ├─ masyu.py                : masyu
   ├─ skyscrapers.py          : skyscrapers (skylines, towers)
   ├─ slitherlink.py          : slither link (fences)
   └─ sudoku.py               : sudoku
```

## Recommended Python packages

### <a href="https://developers.google.com/optimization" target="_blank">Google OR-Tools</a>

```
python -m pip install ortools
```

### <a href="https://www.python-mip.com/" target="_blank">Python-MIP</a>

```
python -m pip install mip
```

### <a href="https://github.com/networkx/networkx" target="_blank">NetworkX</a>

```
python -m pip install networkx
```
