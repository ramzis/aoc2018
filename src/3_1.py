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
        with open(self.input) as f:
            for line in f:
                _, x, y, w, h = self.parse_line(line)
                for a in range(x, x+w):
                    for b in range(y, y+h):
                        Matrix[a][b] += 1
                        if Matrix[a][b] == 2:
                            self.solution += 1

    def parse_line(self, line):
        line = re.findall(r'-?\d+\.?\d*', line)
        line = list(map(int, line))
        return line

if __name__ == '__main__':
    task = Task('3_1')
    task.solve()
    task.write_solution()
