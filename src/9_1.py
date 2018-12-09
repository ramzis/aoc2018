#!/usr/bin/env python3

import re


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
        with open(self.input) as f:
            for line in f:
                players, last_marble = self.parse_line(line)

        llist = DoubleLinkedList()
        head = Node(0)
        head.next = head
        head.prev = head
        llist.head = head
        curr_node = head

        scores = [0] * players
        marble = 1
        player = 1

        while marble <= last_marble:

            if marble % 23 == 0:
                removed_node = llist.remove_n_before(curr_node, 7)
                scores[player - 1] += removed_node.data + marble
                curr_node = removed_node.next
            else:
                curr_node = llist.insert_after_n(curr_node, Node(marble), 1)

            marble += 1
            player = player + 1 if player + 1 < players else 0

        self.solution = max(scores)

    def parse_line(self, line):
        r = re.compile(r'(\d+)')
        ms = r.findall(line)
        ms = list(map(int, ms))
        return ms


class Node:

    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return 'Node({})'.format(self.data)


class DoubleLinkedList:

    def __init__(self):
        self.head = None

    def listprint(self):
        start = self.head
        printval = self.head
        print(printval.data, end=' ')
        printval = printval.next
        while printval != start:
            print(printval.data, end=' ')
            printval = printval.next
        print()

    def insert_after_n(self, start_node, new_node, n):
        target_node = start_node
        for _ in range(n):
            target_node = target_node.next
        next_node = target_node.next

        target_node.next = new_node
        new_node.prev = target_node
        next_node.prev = new_node
        new_node.next = next_node
        return new_node

    def remove_n_before(self, start_node, n):
        target_node = start_node
        for _ in range(n):
            target_node = target_node.prev
        prev_node = target_node.prev
        next_node = target_node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        return target_node

if __name__ == '__main__':
    task = Task('9_1')
    task.solve()
    task.write_solution()
