#!/usr/bin/env python3

import re
import operator
import statistics


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
        points = []
        vectors = []
        with open(self.input) as f:
            for line in f:
                d = self.parse_line(line)
                points.append((d[0] + d[2] * 10000, d[1] + d[3] * 10000))
                vectors.append((d[2], d[3]))

        x_var, y_var = self.heuristic(points)
        i = 10000
        while True:
            self.iterate(points, vectors)
            new_x_var, new_y_var = self.heuristic(points)
            if new_x_var > x_var and new_y_var > y_var:
                self.iterate(points, list(
                    map(lambda x: (x[0] * -1, x[1] * -1), vectors)))
                break
            else:
                x_var, y_var = new_x_var, new_y_var

            i += 1

        # Find minimum points and normalize
        min_x = min(points, key=operator.itemgetter(0))
        min_y = min(points, key=operator.itemgetter(1))
        min_point = (min_x[0], min_y[1])

        points = [[point[0] - min_point[0], point[1] - min_point[1]]
                  for point in points]

        self.solution = ''
        for y in range(10):
            print('')
            for x in range(80):
                if [x, y] in points:
                    self.solution += '*'
                else:
                    self.solution += ' '
            self.solution += '\n'

    def iterate(self, points, vectors, reverse=False):
        for i, p in enumerate(points):
            points[i] = (p[0] + vectors[i][0], p[1] + vectors[i][1])

    def heuristic(self, data):
        x_var = int(statistics.variance([abs(p[0]) for p in data]))
        y_var = int(statistics.variance([abs(p[1]) for p in data]))

        return x_var, y_var

    def parse_line(self, line):
        r = re.compile(r"[-]*\d+")
        ms = r.findall(line)
        return list(map(int, ms))


if __name__ == '__main__':
    task = Task('10_1')
    task.solve()
    task.write_solution()
