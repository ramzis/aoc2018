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
        self.solution = ()
        layout = []
        with open(self.input) as f:
            for line in f:
                layout.append(self.parse_line(line))

        carts = []

        ys = len(layout)
        xs = len(layout[0])

        for y in range(ys):
            for x in range(xs):
                item = layout[y][x]
                if item in ['<', '>']:
                    layout[y][x] = '-'
                    carts.append(((x, y), item, 0))
                elif item in ['^', 'v']:
                    layout[y][x] = '|'
                    carts.append(((x, y), item, 0))

        tick = 0
        collision = False
        while not collision:
            tick += 1
            for c in range(len(carts)):
                curr_x, curr_y = carts[c][0]
                next_x = next_y = 0
                sign_curr = carts[c][1]
                if sign_curr == '^':
                    next_x, next_y = curr_x, curr_y - 1
                elif sign_curr == '<':
                    next_x, next_y = curr_x - 1, curr_y
                elif sign_curr == '>':
                    next_x, next_y = curr_x + 1, curr_y
                elif sign_curr == 'v':
                    next_x, next_y = curr_x, curr_y + 1

                if (next_x, next_y) in [cart[0] for cart in carts]:
                    collision = True
                    self.solution = "{},{}".format(next_x, next_y)
                    break

                sign_target = layout[next_y][next_x]

                if sign_target in ['-', '|']:
                    carts[c] = ((next_x, next_y), sign_curr, carts[c][2])
                elif sign_target == '/':
                    next_sign = \
                        '>' if sign_curr == '^' else \
                        'v' if sign_curr == '<' else \
                        '^' if sign_curr == '>' else \
                        '<' if sign_curr == 'v' else ''

                    carts[c] = \
                        ((next_x, next_y), next_sign, carts[c][2])
                elif sign_target == '\\':
                    next_sign = \
                        '<' if sign_curr == '^' else \
                        '^' if sign_curr == '<' else \
                        'v' if sign_curr == '>' else \
                        '>' if sign_curr == 'v' else ''

                    carts[c] = \
                        ((next_x, next_y), next_sign, carts[c][2])
                elif sign_target == '+':
                    next_sign = \
                        ['<', '^', '>'][carts[c][2]] if sign_curr == '^' else \
                        ['v', '<', '^'][carts[c][2]] if sign_curr == '<' else \
                        ['^', '>', 'v'][carts[c][2]] if sign_curr == '>' else \
                        ['>', 'v', '<'][carts[c][2]] if sign_curr == 'v' else ''

                    carts[c] = \
                        ((next_x, next_y), next_sign, (carts[c][2] + 1) % 3)

            carts.sort(key=lambda x: (x[0][1], x[0][0]))

    def parse_line(self, line):
        return list(line.rstrip('\n'))


if __name__ == '__main__':
    task = Task('13_1')
    task.solve()
    task.write_solution()
