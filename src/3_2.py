#!/usr/bin/env python3

import re

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
        w_m, h_m = 2000, 2000
        Matrix = [[int(0) for x in range(w_m)] for y in range(h_m)]
        lines = []
        with open(self.input) as f:
            for line in f:
                i, x, y, w, h = self.parse_line(line)
                lines.append([i, x, y, w, h])
                for a in range(x, x+w):
                    for b in range(y, y+h):
                        Matrix[a][b] += 1

        for line in lines:
            i, x, y, w, h = line
            overlaps = False
            for a in range(x, x+w):
                if overlaps:
                    break
                for b in range(y, y+h):
                    if Matrix[a][b] > 1:
                        overlaps = True
                        break
            if not overlaps:
                self.solution = i

    def parse_line(self, line):
        line = re.findall(r'-?\d+\.?\d*', line)
        line = list(map(int, line))
        return line

if __name__ == '__main__':
    task = Task('3_2')
    task.solve()
    task.write_solution()
