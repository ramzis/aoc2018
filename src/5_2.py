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
        with open(self.input) as f:
            for line in f:
                data = line.strip()
        self.solution = len(data)
        for c in list(map(chr, range(97, 123))):
            p = re.compile(r'' + c, re.I)
            data_cleaned = p.sub('', data)
            n = self.parse_line(data_cleaned)
            if n < self.solution:
                self.solution = n

    def parse_line(self, line):
        stack = []
        for unit in line:
            if(stack):
                if(abs(ord(unit) - ord(stack[-1])) == 32):
                    stack.pop()
                else:
                    stack.append(unit)
            else:
                stack.append(unit)
        return len(stack)


if __name__ == '__main__':
    task = Task('5_2')
    task.solve()
    task.write_solution()
