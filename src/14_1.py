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
        self.solution = ''
        recipes = [3, 7]
        iterations = 0
        with open(self.input) as f:
            for line in f:
                iterations = self.parse_line(line)

        recipes_to_check = 10
        elves = [0, 1]

        count = 0
        while len(recipes) < recipes_to_check + iterations:
            count += 1
            new_recipe = recipes[elves[0]] + recipes[elves[1]]
            digits = list(int(d) for d in str(new_recipe))
            recipes += digits
            elves = [(e + recipes[e] + 1) % len(recipes) for e in elves]

        self.solution = ''.join(
            map(str, recipes[iterations:iterations + recipes_to_check]))

    def parse_line(self, line):
        return int(line)


if __name__ == '__main__':
    task = Task('14_1')
    task.solve()
    task.write_solution()
