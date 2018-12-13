#!/usr/bin/env python3

import re
import operator


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
        line_count = 0
        data = ''
        rules = []
        with open(self.input) as f:
            for line in f:
                if line_count == 0:
                    data = line.strip().split(' ')[2]
                if line_count > 1:
                    rules.append(self.parse_line(line))
                line_count += 1

        convert = lambda x: int(x == '#')
        data = list(map(convert, data))
        rules = [(list(map(convert, r)), convert(s)) for r, s in rules]

        # print(data)

        live_rules = filter(lambda x: x[1], rules)
        live_rules_10 = sorted([self.shifting(r) for r, _ in live_rules])
        # [print(r, end=' ') for r in live_rules_10]
        # print()

        rule_len = len(rules[0][0])

        iterations = 20

        check_rule = lambda x: 1 if self.shifting(x) in live_rules_10 else 0

        center = 0

        min_empty_sides = 3

        for i in range(iterations):

            new_data = [0, 0]

            side_l = data[0:3]
            side_r = data[-3:]

            while side_l != [0, 0, 0]:
                data.insert(0, 0)
                side_l = data[0:3]
                center += 1

            while side_r != [0, 0, 0]:
                data.append(0)
                side_r = data[-3:]

            moves = len(data) - rule_len + 1
            start = 0
            for move in range(moves):
                end = start + rule_len
                pots = data[start:end]
                new_data.append(int(self.shifting(pots) in live_rules_10))
                start += 1

            if data == new_data:
                break

            data = new_data

        self.solution = sum([idx - center for idx, x in enumerate(data) if x])

    def shifting(self, bitlist):
        out = 0
        for bit in bitlist:
            out = (out << 1) | bit
        return out

    def parse_line(self, line):
        r = re.compile(r'([#.]+)\s=>\s([#.])')
        ms = r.match(line).groups()
        return ms


if __name__ == '__main__':
    task = Task('12_1')
    task.solve()
    task.write_solution()
