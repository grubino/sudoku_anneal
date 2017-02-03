import json

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
    with open('puzzle.json', 'r') as f:
        hints = json.load(f)
    solver = SudokuSolve(hints)
    solver.copy_strategy = "slice"
    solver.steps = 10000
    solver.Tmax = 0.5
    solver.Tmin = 0.1
    solver.updates = 100
    state, e = solver.anneal()

    print('[\n[{}]\n]'.format('],\n['.join([','.join([str(el) for el in row]) for row in state])))
