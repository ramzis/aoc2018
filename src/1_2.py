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
        freq = 0
        freqs = {0}
        found = False
        while(not found):
            with open(self.input) as f:
                for line in f:
                    freq += self.parse_line(line)
                    if(freq in freqs):
                        found = True
                        self.solution = freq
                        break
                    else:
                        freqs.add(freq)


    def parse_line(self, line):
        return int(line)


if __name__ == '__main__':
    task = Task('1_2')
    task.solve()
    task.write_solution()
