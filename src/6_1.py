#!/usr/bin/env python3

from itertools import combinations
from math import ceil

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
        origins = {}
        grid = {}
        count = {}
        points_to_expand = []

        with open(self.input) as f:
            for idx, line in enumerate(f):
                point = self.parse_line(line)
                origins[idx] = point
                count[idx] = 1
                grid[point] = (idx, 0)
                points_to_expand.append((point, idx))

        max_distance = max([self.distance(a, b) for a, b in combinations(origins.values(), 2)])
        max_moves = ceil(max_distance / 2)

        counts = []
        for i in range(max_moves+2):
            new_points_to_expand = []
            for point, expanding_owner in points_to_expand:
                for new_point in self.neighbours(point):
                    # If someone has claimed a point
                    if new_point in grid.keys():
                        current_owner, d_old = grid[new_point]
                        if current_owner != expanding_owner:
                            d_new = self.distance(new_point, origins[expanding_owner])
                            if d_new < d_old:
                                grid[new_point] = (expanding_owner, d_new)
                                count[current_owner] -= 1
                                count[expanding_owner] += 1
                                new_points_to_expand.append((new_point, expanding_owner))
                            elif d_old == d_new:
                                grid[new_point] == ('.', d_old)
                                count[current_owner] -= 1
                    else:
                        d_new = self.distance(new_point, origins[expanding_owner])
                        grid[new_point] = (expanding_owner, d_new)
                        count[expanding_owner] += 1
                        new_points_to_expand.append((new_point, expanding_owner))
            points_to_expand = new_points_to_expand
            counts.append(list(count.values()))

        valid_count = [a for a, b in zip(counts[-2], counts[-1]) if a == b]
        self.solution = max(valid_count)

    def neighbours(self, a):
        return [(a[0]-1, a[1]), (a[0]+1, a[1]), (a[0], a[1]-1), (a[0], a[1]+1)]

    def distance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def parse_line(self, line):
        point = tuple(map(int, line.strip().split(",")))
        return point


if __name__ == '__main__':
    task = Task('6_1')
    task.solve()
    task.write_solution()
