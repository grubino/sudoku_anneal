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

        def __fill(row):
            missing = [i for i in range(self.size+1) if i not in set(row)]
            def __replace(e):
                return e if e is not None else missing.pop()
            return [__replace(i) for i in row]

        self.state = [__fill(row) for row in hints]

        super(SudokuSolve, self).__init__(self.state)

    def move(self):
        self.state = self.hints
        for i, j in itertools.product(range(self.size), range(self.size)):
            if self.hints[i][j]:
                self.state[i][j] = random.choice(range(1,self.size+1))

    def energy(self):
        e = 0
        for col in zip(*self.state):
            e += (self.size - len(set(col)))

        size_root = int(math.floor(math.sqrt(self.size)))
        for i in range(0, self.size, size_root):
            for j in range(0, self.size, size_root):
                e += (self.size - len(set([self.state[k][l]
                                           for k, l in itertools.product(range(i, i + size_root),
                                                                         range(j, j + size_root))])))
        return float(e)
