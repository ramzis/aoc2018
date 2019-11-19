#!/usr/bin/env python3

import os
import copy
from itertools import chain


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
        self.grid = self.step(self.grid, 10)
        self.vals = list(chain.from_iterable(self.grid))
        self.solution = self.vals.count('#') * self.vals.count('|')
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
        for i in range(n):
            grid = g if i % 2 == 0 else gp
            grid_p = gp if i % 2 == 0 else g

            for y in range(self.grid_y):
                for x in range(self.grid_x):
                    val = grid[y][x]
                    adj = self.get_adjacent(grid, x, y)
                    if val == '.':
                        grid_p[y][x] = '|' if adj.count('|') > 2 else '.'
                    elif val == '|':
                        grid_p[y][x] = '#' if adj.count('#') > 2 else '|'
                    elif val == '#':
                        grid_p[y][x] = '#' if adj.count(
                            '#') > 0 and adj.count('|') > 0 else '.'
        return grid_p

    def get_adjacent(self, g, x, y):
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1),
                (-1, 1), (-1, -1), (1, 1), (1, -1)]
        vals = []
        for dir in dirs:
            if 0 <= x + dir[0] < self.grid_x and 0 <= y + dir[1] < self.grid_y:
                vals.append(g[y + dir[1]][x + dir[0]])
        return vals


if __name__ == '__main__':
    task = Task('18_1')
    task.solve()
    task.write_solution()
