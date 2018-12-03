#!/usr/bin/env python3

from collections import _count_elements as count
from functools import reduce

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
        repetitions = [2, 3]
        self.solution = {k:0 for k in repetitions}
        with open(self.input) as f:
            for line in f:
                count_dict = self.parse_line(line)
                values = list(count_dict.values())
                for r in repetitions:
                    if r in values:
                        self.solution[r] += 1

        self.solution = reduce(lambda x, y: x*y, list(self.solution.values()))

    def parse_line(self, line):
        d = {}
        c = count(d, line)
        return d 


if __name__ == '__main__':
    task = Task('2_1')
    task.solve()
    task.write_solution()
