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
        self.opcodes = defaultdict(list)
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
                    break
                else:
                    i += 1
            else:
                before = line
                cmd = self.data[i + 1]
                after = self.data[i + 2]
                if self.decode(before, cmd, after) > 2:
                    self.solution += 1
                i += 3

    def decode(self, before, cmd, after):
        count = 0
        for f in self.funcs:
            self.register = list(before)
            f(cmd[1], cmd[2], cmd[3])
            if self.register == after:
                self.opcodes[cmd[0]].append(f)
                count += 1

        return count

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
    task = Task('16_1')
    task.solve()
    task.write_solution()
