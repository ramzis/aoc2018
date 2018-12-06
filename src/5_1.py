#!/usr/bin/env python3


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
        with open(self.input) as f:
            for line in f:
                self.parse_line(line.strip())

    def parse_line(self, line):
        self.solution = len(line)
        stack = []
        for unit in line:
            if(stack):
                if(abs(ord(unit) - ord(stack[-1])) == 32):
                    stack.pop()
                else:
                    stack.append(unit)
            else:
                stack.append(unit)
        self.solution = len(stack)

if __name__ == '__main__':
    task = Task('5_1')
    task.solve()
    task.write_solution()
