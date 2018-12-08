#!/usr/bin/env python3

import re
import itertools

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
        data = []
        with open(self.input) as f:
            for line in f:
                data.append(self.parse_line(line))

        route = {step: [] for _, step in data}
        for prestep, step in data:
            route[step].append(prestep)

        available = []
        values = set(itertools.chain.from_iterable(route.values()))
        keys = set(route.keys())
        available = sorted(list(values - keys))

        while len(available) > 0:
            available = sorted(available)
            move = available.pop(0)
            self.solution += move
            for step, dependencies in route.items():
                # Remove dependencies on move
                if move in dependencies:
                    route[step].remove(move)
                # Make moves with no prerequisites available
                if route[step] == []:
                    available.append(step)
            # Remove available moves from route
            route = {k: v for k, v in route.items() if v}

    def parse_line(self, line):
        r = re.compile(r'\b[A-Z]\b')
        m, n = r.findall(line)
        return (m, n)


if __name__ == '__main__':
    task = Task('7_1')
    task.solve()
    task.write_solution()
