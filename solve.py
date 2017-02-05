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

    def swap_indices(self, a, b, c, d):
        self.state[a][b], self.state[c][d] = self.state[c][d], self.state[a][b]

    def random_swap_indices(self, indices):
        a, b = random.choice(indices)
        c, d = random.choice(list(set(indices) - {(a, b)}))
        self.swap_indices(a, b, c, d)

    def swap_mini_square_indices(self, i, j):
        indices = [(m, n) for m, n in self.mini_square_indices(i, j) if self.hints[m][n] is None]
        if not indices:
            return
        self.random_swap_indices(indices)

    def move(self):
        random.seed(time.time())
        i, j = random.choice(self.mini_square_set())
        self.swap_mini_square_indices(i, j)

    def print(self):
        print('[\n[{}]\n]'.format('],\n['.join([','.join([str(el) for el in row]) for row in self.state])))

    def energy(self):
        e = 162.0
        for row in self.state:
            e -= len(set(row))
        for col in zip(*self.state):
            e -= len(set(col))
        return float(e)

    def anneal(self):
        """Minimizes the energy of a system by simulated annealing.

        Parameters
        state : an initial arrangement of the system

        Returns
        (state, energy): the best state and energy found.
        """
        step = 0
        self.start = time.time()

        # Precompute factor for exponential cooling from Tmax to Tmin
        if not isinstance(self.Tmin, float):
            raise Exception('Tmin has been set to something other than a float: {}'.format(self.Tmin))
        elif self.Tmin <= 0.0:
            raise Exception('Exponential cooling requires a minimum "\
                "temperature greater than zero.')
        Tfactor = -math.log(self.Tmax / self.Tmin)

        # Note initial state
        T = self.Tmax
        E = self.energy()
        prevState = self.copy_state(self.state)
        prevEnergy = E
        bestState = self.copy_state(self.state)
        bestEnergy = E
        trials, accepts, improves = 0, 0, 0
        if self.updates > 0:
            updateWavelength = self.steps / self.updates
            self.update(step, T, E, None, None)

        # Attempt moves to new states
        while step < self.steps:
            step += 1
            T = self.Tmax * math.exp(Tfactor * step / self.steps)
            self.move()
            E = self.energy()
            dE = E - prevEnergy
            trials += 1
            if dE > 0.0 and math.exp(-dE / T) < random.random():
                # Restore previous state
                self.state = self.copy_state(prevState)
                E = prevEnergy
            else:
                # Accept new state and compare to best state
                accepts += 1
                if dE < 0.0:
                    improves += 1
                prevState = self.copy_state(self.state)
                prevEnergy = E
                if E < bestEnergy:
                    bestState = self.copy_state(self.state)
                    bestEnergy = E
                    if bestEnergy == 0.0:
                        break
            if self.updates > 1:
                if step // updateWavelength > (step - 1) // updateWavelength:
                    self.update(
                        step, T, E, accepts / trials, improves / trials)
                    trials, accepts, improves = 0, 0, 0

        # Return best state and energy
        return bestState, bestEnergy
