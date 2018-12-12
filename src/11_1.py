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
        serial_no = 0
        with open(self.input) as f:
            for line in f:
                serial_no += self.parse_line(line)

        m = 300
        Matrix = [[0 for j in range(m)] for i in range(m)]

        for y in range(1, m + 1):
            for x in range(1, m + 1):
                rack_id = x + 10
                power_lvl = (rack_id * y) + serial_no
                power_lvl *= rack_id
                power_lvl = (abs(power_lvl) // 100) % 10
                power_lvl -= 5
                Matrix[y - 1][x - 1] = power_lvl

        max_power = 0
        point = None

        for y in range(1, m - 1):
            for x in range(1, m - 1):

                up_l = Matrix[y - 1][x - 1]
                up = Matrix[y - 1][x]
                up_r = Matrix[y - 1][x + 1]
                l = Matrix[y][x - 1]
                mid = Matrix[y][x]
                r = Matrix[y][x + 1]
                bt_l = Matrix[y + 1][x - 1]
                bt = Matrix[y + 1][x]
                bt_r = Matrix[y + 1][x + 1]

                power = sum([up_l, up, up_r, l, mid, r, bt_l, bt, bt_r])

                if power > max_power:
                    max_power = power
                    point = (x, y)

        self.solution = point

    def print_matrix(self, m):
        for r in m:
            for c in r:
                print(c, end=' ')
            print()

    def parse_line(self, line):
        return int(line)


if __name__ == '__main__':
    task = Task('11_1')
    task.solve()
    task.write_solution()
