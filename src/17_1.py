#!/usr/bin/env python3

import re
import os
from collections import defaultdict


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
        self.source = (500, 0)
        self.read_data()
        water = set()
        settled = True
        while settled:

            p = self.find_path(self.source)
            settled = self.settle_water(p)

            if not settled:
                self.visualize()
                self.solution = len([v for k, v in self.grid.items() if
                                     v in ['~', '|'] and k[1] >= self.min_y])

    def settle_water(self, p):
        settled = False
        settled_points = []
        for point in p:
            if self.is_still_water(point):
                settled_points.append(point)
                settled = True
        for point in settled_points:
            self.grid[point] = '~'
        return settled

    def is_still_water(self, p):
        q = [p]
        v = set()

        while q:
            n = q.pop(0)
            if n not in v:
                v.add(n)
                below = (n[0], n[1] + 1)
                above = (n[0], n[1] - 1)
                if self.grid[below] in ['|', '']:
                    return False
                else:
                    left = (n[0] - 1, n[1])
                    right = (n[0] + 1, n[1])
                    if self.grid[left] == '|':
                        q.append(left)
                    if self.grid[right] == '|':
                        q.append(right)

        return True

    def find_path(self, p):
        q = [p]
        v = set()

        while q:
            n = q.pop(0)
            if n not in v:
                v.add(n)
                for d in self.get_adjacent_empty_points(n):
                    q.append(d)
                    self.grid[d] = '|'
        v.remove(p)
        return list(v)

    def get_adjacent_empty_points(self, p):
        points = []
        below = (p[0], p[1] + 1)
        left = (p[0] - 1, p[1])
        right = (p[0] + 1, p[1])

        if self.grid[below] in ['~', '#']:
            if self.grid[left] in ['', '|']:
                points.append(left)
            if self.grid[right] in ['', '|']:
                points.append(right)
        elif self.grid[below] in ['', '|']:
            if below[1] <= self.max_y:
                points.append(below)

        return points

    def visualize(self):
        min_x = min(self.grid.keys(), key=lambda x: x[0])[0]
        min_y = min(self.grid.keys(), key=lambda x: x[1])[1]
        max_x = max(self.grid.keys(), key=lambda x: x[0])[0]
        max_y = max(self.grid.keys(), key=lambda x: x[1])[1]

        for y in range(max_y - min_y):
            line = ''
            for x in range(max_x - min_x):
                s = self.grid[(x + min_x, y + min_y)]
                if s == '':
                    line += '.'
                else:
                    line += s
            print(line.strip())

    def read_data(self):
        self.data = []
        self.grid = defaultdict(str)
        with open(self.input) as f:
            for line in f:
                c_1, v_1, _, r_1, r_2 = self.parse_line(line)
                if c_1 == 'x':
                    for y in range(int(r_1), int(r_2) + 1):
                        self.data.append((int(v_1), y))
                        self.grid[(int(v_1), y)] = '#'
                elif c_1 == 'y':
                    for x in range(int(r_1), int(r_2) + 1):
                        self.data.append((x, int(v_1)))
                        self.grid[(x, int(v_1))] = '#'

        self.data.sort()
        self.min_x = self.data[0][0]
        self.min_y = min(self.data, key=lambda x: x[1])[1]
        self.max_x = self.data[-1][0]
        self.max_y = max(self.data, key=lambda x: x[1])[1]
        print(self.min_x, self.min_y)
        print(self.max_x, self.max_y)

    def parse_line(self, line):
        r = re.compile(r'([xy])=(\d+),\s([^$1])=(\d+)..(\d+)')
        m = r.match(line.strip())
        return m.groups()


if __name__ == '__main__':
    task = Task('17_1')
    task.solve()
    task.write_solution()
