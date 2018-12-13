#!/usr/bin/env python3

import re
from collections import defaultdict


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

    def parse_line(self, line):
        r = re.compile(r'\d+')
        m = r.findall(line)
        return list(map(int, m))

    def read_data(self):
        self.data = []
        with open(self.input) as f:
            for line in f:
                self.data.append(self.parse_line(line))

    def solve(self):
        self.read_data()
        self.solution = 0
        self.register = [0, 0, 0, 0]
        self.opcodes = defaultdict(set)
        self.funcs = [self.addr,
                      self.addi,
                      self.mulr,
                      self.muli,
                      self.banr,
                      self.bani,
                      self.borr,
                      self.bori,
                      self.setr,
                      self.seti,
                      self.gtir,
                      self.gtri,
                      self.gtrr,
                      self.eqir,
                      self.eqri,
                      self.eqrr]

        i = 0
        while i + 1 < len(self.data):
            line = self.data[i]
            if line == []:
                if self.data[i + 1] == []:
                    i += 3
                    break
                else:
                    i += 1
            else:
                before = line
                cmd = self.data[i + 1]
                after = self.data[i + 2]
                self.decode(before, cmd, after)
                i += 3

        self.organize()

        while i < len(self.data):
            line = self.data[i]
            self.execute(line)
            i += 1

        self.solution = self.register[0]

    def execute(self, cmd):
        self.opcodes[cmd[0]](cmd[1], cmd[2], cmd[3])

    def decode(self, before, cmd, after):
        count = 0
        for f in self.funcs:
            self.register = list(before)
            f(cmd[1], cmd[2], cmd[3])
            if self.register == after:
                self.opcodes[cmd[0]].add(f)
                count += 1

        return count

    def organize(self):
        found = set()
        while sum([len(x) for x in self.opcodes.values()]) > len(self.funcs):
            for k in self.opcodes.keys():
                values = list(self.opcodes[k])
                if len(values) == 1 and values[0] not in found:
                    found.add(values[0])
                    for k_2 in self.opcodes.keys():
                        if k == k_2:
                            continue
                        old_values = list(self.opcodes[k_2])
                        new_values = [v for v in old_values if v != values[0]]
                        self.opcodes[k_2] = new_values

        self.opcodes = {k: list(v)[0] for k, v in self.opcodes.items()}

    def addr(self, a, b, c):
        self.register[c] = self.register[a] + self.register[b]

    def addi(self, a, b, c):
        self.register[c] = self.register[a] + b

    def mulr(self, a, b, c):
        self.register[c] = self.register[a] * self.register[b]

    def muli(self, a, b, c):
        self.register[c] = self.register[a] * b

    def banr(self, a, b, c):
        self.register[c] = self.register[a] & self.register[b]

    def bani(self, a, b, c):
        self.register[c] = self.register[a] & b

    def borr(self, a, b, c):
        self.register[c] = self.register[a] | self.register[b]

    def bori(self, a, b, c):
        self.register[c] = self.register[a] | b

    def setr(self, a, b, c):
        self.register[c] = self.register[a]

    def seti(self, a, b, c):
        self.register[c] = a

    def gtir(self, a, b, c):
        self.register[c] = 1 if a > self.register[b] else 0

    def gtri(self, a, b, c):
        self.register[c] = 1 if self.register[a] > b else 0

    def gtrr(self, a, b, c):
        self.register[c] = 1 if self.register[a] > self.register[b] else 0

    def eqir(self, a, b, c):
        self.register[c] = 1 if a == self.register[b] else 0

    def eqri(self, a, b, c):
        self.register[c] = 1 if self.register[a] == b else 0

    def eqrr(self, a, b, c):
        self.register[c] = 1 if self.register[a] == self.register[b] else 0


if __name__ == '__main__':
    task = Task('16_2')
    task.solve()
    task.write_solution()
