#!/usr/bin/env python3

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
        self.solution = ''
        strings = []
        with open(self.input) as f:
            for line in f:
                strings.append(line.rstrip())

        for (a, b) in combinations(strings, 2):
            mismatches = 0
            diff = ''
            for n, x in enumerate(a):
                if x != b[n]:
                    mismatches += 1
                else:
                    diff += x
                if mismatches > 1: 
                    break
            if mismatches == 1:
                self.solution = diff
                break

if __name__ == '__main__':
    task = Task('2_2')
    task.solve()
    task.write_solution()
