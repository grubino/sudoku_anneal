import json

import sys

from solve import *

# solved = [
#     [1, 2, 3, 4, 5, 6, 7, 8, 9],
#     [4, 5, 6, 7, 8, 9, 1, 2, 3],
#     [7, 8, 9, 1, 2, 3, 4, 5, 6],
#     [2, 3, 1, 5, 6, 4, 8, 9, 7],
#     [5, 6, 4, 8, 9, 7, 2, 3, 1],
#     [8, 9, 7, 2, 3, 1, 5, 6, 4],
#     [3, 1, 2, 6, 4, 5, 9, 7, 8],
#     [6, 4, 5, 9, 7, 8, 3, 1, 2],
#     [9, 7, 8, 3, 1, 2, 6, 4, 5],
# ]

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        hints = json.load(f)
    solver = SudokuSolve(hints)
    print(solver.energy())
    solver.copy_strategy = "slice"
    params = solver.auto(100, 10000)
    solver.Tmin = params['tmin']
    solver.Tmax = params['tmax']
    solver.steps = params['steps']
    solver.updates = 10
    state, e = solver.anneal()

    print('[\n[{}]\n]'.format('],\n['.join([','.join([str(el) for el in row]) for row in state])))
