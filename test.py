from solve import *

if __name__ == '__main__':
    hints = [
        [None, None, 3, 4, 5, None, None, 8, 9],
        [4, 5, None, 7, None, None, None, 2, 3],
        [7, None, None, None, 2, 3, None, None, 6],
        [None, 3, None, 5, None, 4, None, None, 7],
        [None, None, None, 8, None, 7, 2, 3, 1],
        [8, None, None, 2, None, 1, 5, None, 4],
        [3, 1, None, 6, 4, 5, None, 7, 8],
        [None, None, 5, 9, None, 8, 3, None, 2],
        [None, None, None, 3, None, 2, 6, 4, None],
    ]
    solved = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 1, 5, 6, 4, 8, 9, 7],
        [5, 6, 4, 8, 9, 7, 2, 3, 1],
        [8, 9, 7, 2, 3, 1, 5, 6, 4],
        [3, 1, 2, 6, 4, 5, 9, 7, 8],
        [6, 4, 5, 9, 7, 8, 3, 1, 2],
        [9, 7, 8, 3, 1, 2, 6, 4, 5],
    ]
    solver = SudokuSolve(hints)
    solver.copy_strategy = "slice"
    solver.Tmax = 10.0
    solver.Tmin = 1.0
    solver.steps = 10000
    solver.updates = 1000000
    state, e = solver.anneal()

    print('\n'.join(['|'.join([str(el) for el in row]) for row in state]))
