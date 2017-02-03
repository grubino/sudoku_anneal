import random

import itertools

import math
import simanneal
import time

random.seed(time.time())

class SudokuSolve(simanneal.Annealer):

    def __init__(self, hints):
        if not isinstance(hints, list):
            raise Exception('expected a list')
        self.size = len(hints)
        self.hints = hints
        self.mini_square_size = int(math.sqrt(float(self.size)))
        self.state = self.hints
        super(SudokuSolve, self).__init__(self.state)

    def __mini_square_set(self):
        return [(i, j) for i, j in itertools.product(range(0, self.size, self.mini_square_size),
                                                     range(0, self.size, self.mini_square_size))]

    def __mini_square_hints(self, i, j):
        return set([self.hints[k][l] for k, l in itertools.product(range(i, i+self.mini_square_size),
                                                                   range(j, j+self.mini_square_size))
                    if self.hints[k][l] is not None])

    def move(self):
        for i, j in self.__mini_square_set():
            hints = self.__mini_square_hints(i, j)
            choices = [v for v in range(1, self.size + 1) if v not in hints]
            random.shuffle(choices)
            for m, n in itertools.product(range(self.mini_square_size), range(self.mini_square_size)):
                if self.hints[i+m][j+n] is None:
                    self.state[i+m][j+n] = choices.pop()

    def energy(self):
        e = 0.0
        for row in self.state:
            e -= len(set(row))
        for col in zip(*self.state):
            e -= len(set(col))
        return float(e)
