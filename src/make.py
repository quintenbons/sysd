#!/usr/bin/python3
"""Main manager: dependency tree and launching tasks"""
from typing import Set
import parsing
import argparse
import time
import runner

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
    running = set()
    while len(done_tasks) < len(tasks):
        runnable = get_runnable(done_tasks, task_graph)
        to_run = runnable - executing_tasks

        for job_handle in list(running):
            task, job = job_handle
            if job.ready():
                print("JOB DONE", job, "FOR TASK", task)
                running.remove(job_handle)
                done_tasks.add(task)
                executing_tasks.remove(task)

        if len(to_run) == 0:
            print("All running, waiting for news")
            time.sleep(1)

        for task in to_run:
            print(f"RUN {task} with command {tasks[task]['command']}")
            executing_tasks.add(task)
            cmd = tasks[task]['command']
            dependencies = task_graph[task]
            celery_instance = runner.run.delay(task, cmd, dependencies)
            running.add((task, celery_instance))

if __name__ == "__main__":
    main()
