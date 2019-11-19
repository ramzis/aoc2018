#!/usr/bin/env python3

import os
import copy
from itertools import chain
from collections import Counter


class Task:

    input_dir = '../input'
    output_dir = '../output'

    def __init__(self, day):
        self.day = day
        self.input = '{}/{}.txt'.format(self.input_dir, day)

    def write_solution(self):
        f = open('{}/{}.txt'.format(self.output_dir, self.day),
                 'wt', encoding='utf-8')
        f.write(str(self.solution) + '\n')

    def solve(self):
        self.solution = 0
        self.read_data()
        self.solution = self.step(self.grid, 1000000000)
        print(self.solution)

    def read_data(self):
        self.grid = []
        with open(self.input) as f:
            for line in f:
                self.grid.append(self.parse_line(line))
        self.grid_y = len(self.grid)
        self.grid_x = len(self.grid[0] if self.grid_y > 0 else 0)

    def parse_line(self, line):
        return list(line.strip())

    def visualize(self, g):
        [print(''.join(x)) for x in g]
        print()

    def step(self, g, n):
        gp = copy.deepcopy(g)
        past = []
        for i in range(n):
            grid = g if i % 2 == 0 else gp
            grid_p = gp if i % 2 == 0 else g

            for y in range(self.grid_y):
                for x in range(self.grid_x):
                    val = grid[y][x]
                    adj = self.get_adjacent(grid, x, y)
                    trees = adj.count('|')
                    mills = adj.count('#')
                    if val == '.':
                        grid_p[y][x] = '|' if trees > 2 else '.'
                    elif val == '|':
                        grid_p[y][x] = '#' if mills > 2 else '|'
                    elif val == '#':
                        grid_p[y][x] = '#' if mills > 0 and trees > 0 else '.'

            if i >= 500:
                value = self.value(grid_p)
                if value in past:
                    period = len(past)
                    diff = n - i
                    r = diff % period
                    return past[r - 1]
                else:
                    past.append(value)

    def get_adjacent(self, g, x, y):
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1),
                (-1, 1), (-1, -1), (1, 1), (1, -1)]
        vals = []
        for dir in dirs:
            if 0 <= x + dir[0] < self.grid_x and 0 <= y + dir[1] < self.grid_y:
                vals.append(g[y + dir[1]][x + dir[0]])
        return vals

    def value(self, g):
        vals = list(chain.from_iterable(g))
        counts = Counter(vals)
        return counts['#'] * counts['|']

if __name__ == '__main__':
    task = Task('18_2')
    task.solve()
    task.write_solution()
