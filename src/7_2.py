#!/usr/bin/env python3

import re
import itertools

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
        data = []
        with open(self.input) as f:
            for line in f:
                data.append(self.parse_line(line))

        route = {step: [] for _, step in data}
        for prestep, step in data:
            route[step].append(prestep)

        available = []
        values = set(itertools.chain.from_iterable(route.values()))
        keys = set(route.keys())
        available = sorted(list(values - keys))

        n_workers = 5
        workers = [0] * n_workers
        jobs = [None] * n_workers
        time_passed = 0

        while available or max(workers) > 0:

            # Assign new work
            free_workers = [idx for idx, _ in enumerate(workers) if jobs[idx] == None]
            jobs_to_assign = min(len(available), len(free_workers))

            print("==================")
            print("Workers", workers)
            print("Jobs   ", jobs)
            print("Queued ", available, '\n')

            for i in range(jobs_to_assign):
                job = available.pop(0)
                worker_id = free_workers[i]
                jobs[worker_id] = job
                workers[worker_id] = self.time_per_move(job)

                print("Assigned job {} @ {}".format(job, time_passed))
                print("To worker", worker_id)
                print(workers)

            # Finish shortest job(s)
            finished_jobs = []
            shortest_job_time = min([workers[idx] for idx, j in enumerate(jobs) if j != None] or 0)
            # If any work is in progress
            if shortest_job_time > 0:
                # Make everyone who has a task 
                # work until shortest job is done
                time_passed += shortest_job_time
                for idx, worker in enumerate(workers):
                    if jobs[idx] != None:
                        workers[idx] -= shortest_job_time
                        if workers[idx] == 0:
                            finished_jobs.append(jobs[idx])
                            jobs[idx] = None
                finished_jobs = sorted(finished_jobs)
            
            print()            
            print("Finished short jobs {} @ {}".format(finished_jobs, time_passed))       

            # See what it unlocks and queue it
            for move in finished_jobs:
                self.solution += move
                for step, dependencies in sorted(route.items(), key=lambda x: x[0]):
                    # Remove dependencies on move
                    if move in dependencies:
                        route[step].remove(move)
                    # Make moves with no prerequisites available
                    new_moves = []
                    if route[step] == []:
                        new_moves.append(step)
                    available += sorted(new_moves)
                    ms = sorted(new_moves)
                    if ms != []:
                        print("Added new available", ms)
                # Remove available moves from route
                route = {k: v for k, v in route.items() if v}

        self.solution = time_passed

    def time_per_move(self, move):
        return ord(move) - 4

    def parse_line(self, line):
        r = re.compile(r'\b[A-Z]\b')
        m, n = r.findall(line)
        return (m, n)


if __name__ == '__main__':
    task = Task('7_2')
    task.solve()
    task.write_solution()
