#!/usr/bin/env python3

import os
import copy
import time
import cProfile
from operator import itemgetter


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
        self.goblin = 'G'
        self.elf = 'E'
        self.units = {}
        self.print_grid = None
        self.attack_val = 3
        self.start_health = 200
        self.read_data()
        self.print_grid_info()
        self.process_units()
        self.print_unit_info()
        self.combat()

    def read_data(self):
        self.grid = []
        with open(self.input) as f:
            for line in f:
                self.grid.append(self.parse_line(line))
        self.grid_y = len(self.grid)
        self.grid_x = len(self.grid[0] if self.grid_y > 0 else 0)

    def parse_line(self, line):
        return list(line.strip())

    def process_units(self):
        unit_id = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                item = self.grid[y][x]
                if item in [self.goblin, self.elf]:
                    unit_id += 1
                    unit = {'p': (x, y), 'hp': self.start_health, 't': item}
                    self.units[unit_id] = unit

    def find_path(self, p, t):
        # print('Finding path from {} to {}'.format(p, t))
        q = [[p]]
        v = set()

        while q:
            path = q.pop(0)
            last = path[-1]

            if last not in v:
                for n in self.get_adjacent_values(last, ['.']):
                    new_path = list(path)
                    new_path.append(n)
                    q.append(new_path)
                    if n == t:
                        # self.print_path(new_path)
                        yield new_path
                v.add(last)

    def get_adjacent_values(self, p, vals):
        points = []
        if p[1] - 1 >= 0 and self.grid[p[1] - 1][p[0]] in vals:
            points.append((p[0], p[1] - 1))
        if p[0] - 1 >= 0 and self.grid[p[1]][p[0] - 1] in vals:
            points.append((p[0] - 1, p[1]))
        if p[0] + 1 < self.grid_x and self.grid[p[1]][p[0] + 1] in vals:
            points.append((p[0] + 1, p[1]))
        if p[1] + 1 < self.grid_y and self.grid[p[1] + 1][p[0]] in vals:
            points.append((p[0], p[1] + 1))
        return points

    def get_start_order(self):
        order = [k for k, v in self.units.items() if v['hp'] > 0]
        return sorted(order, key=lambda x: (self.units[x]['p'][1], self.units[x]['p'][0]))

    def combat(self):

        is_combat = True
        round_ = 0
        while is_combat:

            print('Round ', round_)

            units = self.get_start_order()
            self.print_start_order()

            while units:

                u = units.pop(0)

                if self.units[u]['hp'] <= 0:
                    print('Dead units don\'t take turns...')
                    continue

                targets = [k for k, v in self.units.items() if
                           v['hp'] > 0 and v['t'] != self.units[u]['t']]

                # print('{} @ {} takes its turn'.format(type_, u))

                if targets:
                    if self.attack(u, targets):
                        continue
                    else:
                        self.move(u, targets)
                        if self.attack(u, targets):
                            print('Attacked after moving next to target')
                else:
                    sum_ = sum(
                        [v['hp']for v in self.units.values() if v['hp'] > 0])

                    healths = ['{}({})'.format(self.units[k]['t'], self.units[k]['hp'])
                               for k in self.get_start_order() if self.units[k]['hp'] > 0]

                    self.solution = sum_ * round_

                    print('No more enemies left. The {} win!'.format(
                        self.units[u]['t']))
                    print('Hp sum', sum_)
                    print('Round', round_)
                    print('Healths')
                    [print(x) for x in healths]
                    print(self.solution)
                    is_combat = False
                    break

            self.print_path([])
            round_ += 1

    def attack(self, u, targets):
        enemies = [self.goblin, self.elf]
        enemies.remove(self.units[u]['t'])
        in_range_enemies = self.get_adjacent_values(
            self.units[u]['p'], enemies)
        if len(in_range_enemies) < 1:
            return False

        # print('Unit surrounded by {} enemies'.format(
            # len(in_range_enemies)))

        in_range_enemies = {k: v for k, v in self.units.items() if
                            v['p'] in in_range_enemies and v['hp'] > 0}

        min_hp = min(in_range_enemies.values(), key=lambda v: v['hp'])['hp']

        lowest_hp_enemies = {k: v for k, v in in_range_enemies.items() if
                             v['hp'] == min_hp}

        attacked = sorted(lowest_hp_enemies.keys(),
                          key=lambda k:
                          (lowest_hp_enemies[k]['p'][1], lowest_hp_enemies[k]['p'][0]))[0]

        self.units[attacked]['hp'] -= self.attack_val

        print('{} attacks {}!'.format(u, attacked))

        if self.units[attacked]['hp'] <= 0:
            p = self.units[attacked]['p']
            self.grid[p[1]][p[0]] = '.'
            print('{} has died!'.format(attacked))

        return True

    def move(self, u, targets):
        nearest_path = []
        nearest_enemy = None
        nearest_path_length = 1000
        u_p = self.units[u]['p']

        for target in targets:
            t_p = self.units[target]['p']
            adjacent_tiles = self.get_adjacent_values(t_p, ['.'])
            for tile in adjacent_tiles:
                for path in self.find_path(u_p, tile):
                    if len(path) < nearest_path_length or \
                       (len(path) == nearest_path_length and
                            path[1] == sorted([path[1], nearest_path[1]], key=itemgetter(1, 0))[0]):
                        nearest_path = path
                        nearest_enemy = target
                        nearest_path_length = len(path)

        if nearest_path:
            # print('Nearest enemy:', nearest_enemy)
            # print('Nearest path:', nearest_path)
            # self.print_path(nearest_path)

            p = nearest_path[1]

            if p in [x['p'] for x in self.units.values() if x['hp'] > 0]:
                print("Trying to move onto taken spot!", p)
                taken = list(filter(lambda args: (
                    args[1]['p'] == p and args[1]['hp'] > 0), self.units.items()))
                print(taken)
                exit(1)
            self.grid[u_p[1]][u_p[0]] = '.'
            self.grid[p[1]][p[0]] = self.units[u]['t']
            self.units[u]['p'] = p

            print('{} moved to {}'.format(u, p))
        else:
            print('{} No enemy in reach'.format(u))

    ####################
    # Testing functions
    ####################

    def run_tests(self):
        self.test_4()

    def test_reset(self):
        self.solution = 0
        self.goblin = 'G'
        self.elf = 'E'
        self.units = {}
        self.print_grid = None
        self.attack_val = 3
        self.start_health = 200

    def test_read_data(self, test_data):
        self.grid = []
        for line in test_data:
            self.grid.append(self.parse_line(line))
        self.grid_y = len(self.grid)
        self.grid_x = len(self.grid[0] if self.grid_y > 0 else 0)

    def test_0(self):
        self.test_reset()
        data = [
            '#########',
            '#.......#',
            '#.......#',
            '#.......#',
            '#.......#',
            '#.......#',
            '#.......#',
            '#.......#',
            '#########'
        ]
        self.test_read_data(data)
        self.print_grid_info()
        self.process_units()
        self.print_unit_info()

    def test_1(self):
        self.test_reset()
        self.start_health = 10
        data = [
            '#########',
            '#...E...#',
            '#.......#',
            '#..G.G..#',
            '#.......#',
            '#.......#',
            '#.......#',
            '#.......#',
            '#########'
        ]
        self.test_read_data(data)
        self.print_grid_info()
        self.process_units()
        self.print_unit_info()
        self.combat()

    def test_2(self):
        self.test_reset()
        self.start_health = 3
        data = [
            '#########',
            '#...E...#',
            '####.####',
            '#..G.G..#',
            '#.......#',
            '#.......#',
            '#.......#',
            '#.......#',
            '#########'
        ]
        self.test_read_data(data)
        self.print_grid_info()
        self.process_units()
        self.print_unit_info()
        self.combat()

    def test_3(self):
        self.test_reset()
        self.start_health = 3
        data = [
            '#########',
            '#...E...#',
            '#...G...#',
            '#########'
        ]
        self.test_read_data(data)
        self.print_grid_info()
        self.process_units()
        self.print_unit_info()
        self.combat()

    def test_4(self):
        self.test_reset()
        self.start_health = 3
        data = [
            '#########',
            '#...G...#',
            '#..GEG..#',
            '#...G...#',
            '#########'
        ]
        self.test_read_data(data)
        self.print_grid_info()
        self.process_units()
        self.units[1]['hp'] = 1
        self.units[2]['hp'] = 1
        self.units[3]['hp'] = 100
        self.units[4]['hp'] = 1
        self.units[5]['hp'] = 1
        self.print_unit_info()
        self.combat()

    def test_4(self):
        self.test_reset()
        self.start_health = 3
        data = [
            '#######',
            '#.E...#',
            '#.....#',
            '#...G.#',
            '#######'
        ]
        self.test_read_data(data)
        self.process_units()
        paths = self.find_path((2, 1), (4, 2))
        for p in paths:
            print("Path found")

    ####################
    # Printing functions
    ####################

    def print_path(self, p):
        self.print_grid = copy.deepcopy(self.grid)
        for x in p:
            self.print_grid[x[1]][x[0]] = '@'

        # os.system('clear')
        [print(''.join(x)) for x in self.print_grid]
        print()

    def print_start_order(self):
        print('Starting order')
        print('==============')
        count = 1
        self.print_grid = copy.deepcopy(self.grid)
        for x in self.get_start_order():
            p = self.units[x]['p']
            self.print_grid[p[1]][p[0]] = str(count)
            count += 1
        [print(''.join(x)) for x in self.print_grid]
        print('==============')

    def print_adjacent_empty_points(self):
        print('Adjacent empty spots')
        print('===================')
        for unit in self.units.values():
            p = unit['p']
            adj = self.get_adjacent_values(p, ['.'])
            print('{} : {}'.format(unit, adj))
        print('===================')

    def print_unit_info(self):
        gs = [x for x in self.units.values() if x['t'] == self.goblin]
        es = [x for x in self.units.values() if x['t'] == self.elf]
        print('Available units')
        print('===========')
        print('{} Goblin: {}'.format(len(gs), gs))
        print('{} Elven : {}'.format(len(es), es))
        print('===========')
        print('The {} are outnumbered by {} {} units!'.format(
            'elves' if len(es) < len(gs) else 'goblins',
            abs(len(es) - len(gs)),
            'elven' if len(es) > len(gs) else 'goblin'
        ))
        print('===========')

    def print_grid_info(self):
        print('Grid info')
        print('==============')
        print('Size: {}x{}'.format(self.grid_y, self.grid_x))
        self.print_path([])

if __name__ == '__main__':
    task = Task('15_1')
    task.solve()
    task.write_solution()
    # task.run_tests()
