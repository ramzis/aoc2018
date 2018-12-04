#!/usr/bin/env python3

import re
from dateutil import parser
from datetime import datetime

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
        data = []
        with open(self.input) as f:
            for line in f:
                d = self.parse_line(line)
                data.append(d)
        data.sort(key=lambda r: r[0])
        guard = None
        book = {}
        last_asleep = 0
        for time, action in data:
            if action == 'falls':
                last_asleep = time.minute
            elif action == 'wakes':
                for x in range(last_asleep, time.minute):
                    book[guard]['minutes'][x] += 1
                book[guard]["time"] += time.minute - last_asleep
            else:
                guard = action
                if guard not in book:
                    book[guard] = {"minutes": [0 for _ in range(60)], "time": 0}

        worst_guard = None
        max_times = 0
        max_minute = 0
        for guard in book.keys():
            m = book[guard]["minutes"]
            times = max(m)
            if times > max_times:
                max_times = times
                worst_guard = guard
                max_minute = m.index(times)

        self.solution = int(worst_guard) * max_minute

    def parse_line(self, line):
        p = re.compile(r"\[ (.*?) \] \s (?: .+? \#)* (\d+ | wakes | falls)", re.X | re.I)
        m = p.match(line)
        g = m.groups()
        g = (parser.parse(g[0]), g[1])
        return g


if __name__ == '__main__':
    task = Task('4_2')
    task.solve()
    task.write_solution()
