#!/usr/bin/python3
"""Main manager: dependency tree and launching tasks"""
from typing import Set
import parsing
import argparse
import time

def get_runnable(done_tasks, task_graph) -> Set[str]:
    runnable = set()
    for task in task_graph:
        if task in done_tasks:
            continue
        if not all(dep in done_tasks for dep in task_graph[task]):
            continue
        runnable.add(task)
    return runnable

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('makefile', help='Makefile to parse')

    args = argparser.parse_args()
    tasks = parsing.parse_makefile(args.makefile)
    task_graph = parsing.generate_task_graph(tasks)

    done_tasks = set()
    executing_tasks = set()
    while len(done_tasks) < len(tasks):
        runnable = get_runnable(done_tasks, task_graph)
        to_run = runnable - executing_tasks

        if len(to_run) == 0:
            print("All running, waiting for news")
            time.sleep(10)

        for task in to_run:
            print("RUN", task)
            executing_tasks.add(task)


if __name__ == "__main__":
    main()
