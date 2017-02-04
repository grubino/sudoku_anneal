import itertools
import math
import random

import simanneal
import time

class SudokuSolve(simanneal.Annealer):

    def __init__(self, hints):
        if not isinstance(hints, list):
            raise Exception('expected a list')
        self.size = len(hints)
        self.hints = hints
        self.mini_square_size = int(math.sqrt(float(self.size)))
        self.state = [[None for _ in range(self.size)] for _ in range(self.size)]

        for i, j in self.mini_square_set():
            indices = [(k, m) for k, m in self.mini_square_indices(i, j)]
            choices = [n for n in range(1, self.size+1)
                       if n not in set([self.hints[k][m]
                                        for k, m in indices if self.hints[k][m] is not None])]
            for k, m in indices:
                if self.hints[k][m] is None:
                    self.state[k][m] = choices.pop()
                else:
                    self.state[k][m] = self.hints[k][m]

        super(SudokuSolve, self).__init__(self.state)

    def mini_square_set(self):
        return [(i, j) for i, j in itertools.product(range(0, self.size, self.mini_square_size),
                                                     range(0, self.size, self.mini_square_size))]

    def mini_square_indices(self, i, j):
        return [(i + a, j + b) for a, b in itertools.product(range(self.mini_square_size),
                                                             range(self.mini_square_size))]

    def move(self):
        random.seed(time.time())
        i, j = random.choice(self.mini_square_set())
        indices = [(m, n) for m, n in self.mini_square_indices(i, j) if self.hints[m][n] is None]
        if not indices:
            return
        random.shuffle(indices)
        a, b = random.choice(indices)
        c, d = random.choice(list(set(indices) - set([(a, b)])))
        self.state[a][b], self.state[c][d] = self.state[c][d], self.state[a][b]

    def print(self):
        print('[\n[{}]\n]'.format('],\n['.join([','.join([str(el) for el in row]) for row in self.state])))

    def energy(self):
        e = 162.0
        for row in self.state:
            e -= len(set(row))
        for col in zip(*self.state):
            e -= len(set(col))
        return float(e)
