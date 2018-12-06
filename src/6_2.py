#!/usr/bin/env python3

from math import ceil
from itertools import combinations

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
        origins = []
        visited = set()
        unvisited = []
        count = 0
        region_limit = 10000

        with open(self.input) as f:
            for idx, line in enumerate(f):
                point = self.parse_line(line)
                origins.append(point)

        # Find center point
        min_center_sum = 1e+10
        for point in origins:
            center_sum = self.distance_sum(point, origins)
            if center_sum < min_center_sum:
                min_center_sum = center_sum
                center = point

        # Apply BFS from center
        unvisited.append(center)

        max_distance_sum = 0
        while len(unvisited) > 0:
           
            point = unvisited.pop(0)
            visited.add(point)

            distance_sum = self.distance_sum(point, origins)

            if distance_sum > max_distance_sum:
                max_distance_sum = distance_sum

            if distance_sum < region_limit:
                count += 1

                for neighbour in self.neighbours(point):
                    
                    if neighbour not in visited and neighbour not in unvisited:
                        unvisited.append(neighbour)

        self.solution = count

    def neighbours(self, a):
        return [(a[0]-1, a[1]), (a[0]+1, a[1]), (a[0], a[1]-1), (a[0], a[1]+1)]

    def distance_sum(self, a, bs):
        _sum = 0
        for b in bs:
            _sum += self.distance(a, b)
        return _sum
        
    def distance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def parse_line(self, line):
        point = tuple(map(int, line.strip().split(',')))
        return point


if __name__ == '__main__':
    task = Task('6_2')
    task.solve()
    task.write_solution()
