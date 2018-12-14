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
        recipes = [3, 7]
        goal = ''
        with open(self.input) as f:
            for line in f:
                goal = self.parse_line(line)

        elves = [0, 1]
        recipes_to_check = len(goal)

        while True:
            new_recipe = recipes[elves[0]] + recipes[elves[1]]
            digits = list(int(d) for d in str(new_recipe))
            recipes += digits
            n_to_check = min(len(recipes), recipes_to_check + 1)

            check_string = ''.join(map(str, recipes[-n_to_check:]))

            idx = check_string.find(goal)
            if idx >= 0:
                self.solution = len(recipes) - (n_to_check - idx)
                break

            elves = [(e + recipes[e] + 1) % len(recipes) for e in elves]

        print(self.solution)

    def parse_line(self, line):
        return str(line)


if __name__ == '__main__':
    task = Task('14_2')
    task.solve()
    task.write_solution()
