#!/usr/bin/env python3

import logging


class Task:

    input_dir = '../input'
    output_dir = '../output'

    logging.basicConfig(format='%(message)s', level=logging.WARNING)

    def __init__(self, day):
        self.day = day
        self.input = '{}/{}.txt'.format(self.input_dir, day)

    def write_solution(self):
        f = open('{}/{}.txt'.format(self.output_dir, self.day),
                 'wt', encoding='utf-8')
        f.write(str(self.solution) + '\n')

    def solve(self):
        self.solution = 0
        data = []
        with open(self.input) as f:
            for line in f:
                data += self.parse_line(line)

        childstack = [1]
        metastack = [0]
        nodes = []
        level = 0
        node_id = 0

        i = 0
        while i < len(data):

            logging.info("===Reading new node===")

            c = data[i]
            m = data[i + 1]

            childstack.append(c)
            metastack.append(m)

            self.debug_info(level, childstack, metastack)
            logging.info("Node has {} children and {} metadata".format(c, m))

            # Node in current level has more children nested
            if childstack[-1] > 0:

                logging.info("Node has more children nested")

                level += 1
                i += 2

                logging.info("Descending into level {}".format(level))

            # Node is a leaf
            else:
                while childstack[-1] == 0 and level >= 0:

                    i += 2

                    logging.info("Node is a leaf in level {}".format(level))

                    childstack.pop()
                    meta_count = metastack.pop()
                    metadata = [data[i + j] for j in range(meta_count)]
                    nodes.append((level, metadata, node_id))
                    node_id += 1
                    i += meta_count
                    childstack[-1] -= 1

                    logging.info("Reading metadata {}".format(metadata))
                    self.debug_info(level, childstack, metastack)

                    if childstack[-1] == 0:

                        logging.info("Node was last in level {}".format(level))

                        if level == 0:
                            break

                        level -= 1
                        i -= 2

                        logging.info("Ascending into level {}".format(level))

        metasum = 0
        for _, m, _ in nodes:
            metasum += sum(m)
        self.solution = metasum

    def debug_info(self, level, childstack, metastack):
        logging.info("Level    {}".format(level))
        logging.info("Children {}".format(childstack))
        logging.info("Metas    {}".format(metastack))

    def parse_line(self, line):
        return map(int, line.strip().split(' '))


if __name__ == '__main__':
    task = Task('8_1')
    task.solve()
    task.write_solution()
