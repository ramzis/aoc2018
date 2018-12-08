#!/usr/bin/env python3

import logging
import operator


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
        parentstack = ['@']
        nodes = []
        level = 0
        node_id = '@'
        unique_node_id = '@'

        i = 0
        while i < len(data):

            logging.info("===Reading new node===")

            c = data[i]
            m = data[i + 1]

            childstack.append(c)
            metastack.append(m)
            node_id = chr(ord(unique_node_id) + 1)
            unique_node_id = node_id
            parentstack.append(node_id)

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
                    nodes.append(
                        (level, metadata, parentstack[-1], parentstack[-2]))
                    i += meta_count
                    childstack[-1] -= 1

                    parentstack.pop()

                    logging.info("Reading metadata {}".format(metadata))
                    self.debug_info(level, childstack, metastack)

                    if childstack[-1] == 0:

                        logging.info("Node was last in level {}".format(level))

                        if level == 0:
                            break

                        level -= 1
                        i -= 2

                        logging.info("Ascending into level {}".format(level))

        nodes.sort(key=operator.itemgetter(3))

        tree_map = {n[3]: ([], []) for n in nodes}
        tree_map_2 = {n[2]: (n[1], []) for n in nodes}
        tree_map.update(tree_map_2)

        for n in nodes:
            tree_map[n[3]][1].append(n)

        metasum = self.score(tree_map, 'A')
        self.solution = metasum

    def score(self, tree, node):
        if node in tree.keys():
            metas, children = tree[node]
            child_sum = 0
            if children:
                for idx in metas:
                    if (idx - 1) < len(children):
                        child_sum += self.score(tree, children[idx - 1][2])
                return child_sum
            else:
                return sum(metas)
        else:
            return 0

    def debug_info(self, level, childstack, metastack):
        logging.info("Level    {}".format(level))
        logging.info("Children {}".format(childstack))
        logging.info("Metas    {}".format(metastack))

    def parse_line(self, line):
        return map(int, line.strip().split(' '))


if __name__ == '__main__':
    task = Task('8_2')
    task.solve()
    task.write_solution()
