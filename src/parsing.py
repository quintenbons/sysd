#!/usr/bin/python3
from celery import Celery
import argparse
import os
import subprocess
from collections import deque

# Configuration initiale de Celery
# app = Celery('parsing', broker='pyamqp://guest@localhost//')

# parsing du makefile
def parse_makefile(makefile: os.PathLike):
    tasks = {}
    with open(makefile, 'r') as f:
        for line in f.readlines():
            if line[0] not in ['\t', ' '] and len(line) != 0:
                split = line.split(':')
                if len(split) > 1: target, dependencies = split
                else: target, dependencies = split[0], ""
                tasks[target.strip()] = {'dependencies': dependencies.strip().split(), 'command': None}
            else:
                last_target = list(tasks.keys())[-1]
                tasks[last_target]['command'] = line.strip()
    return tasks

# tâches Celery
# @app.task
# def execute_command(command):
#     print(f"Executing: {command}")
#     subprocess.run(command, shell=True)

def generate_task_graph(tasks):
    graph = {target: set(info['dependencies']) for target, info in tasks.items()}
    return graph

# Tri topologique pour l'ordonnancement
def topological_sort(graph):
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    queue = deque([u for u in graph if in_degree[u] == 0])
    ordered_tasks = []

    while queue:
        u = queue.popleft()
        ordered_tasks.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(ordered_tasks) != len(graph):
        raise ValueError("Un graphe de tâches contient des cycles")

    return ordered_tasks

# Exécution séquentielle des commandes avec ordonnancement
def execute_sequentially(tasks, ordered_tasks):
    for target in ordered_tasks:
        if tasks[target]['command']:
            print(f"Executing: {tasks[target]['command']}")
            subprocess.run(tasks[target]['command'], shell=True)

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('makefile', help='Makefile to parse')

    args = argparser.parse_args()
    tasks = parse_makefile(args.makefile)
    task_graph = generate_task_graph(tasks)
    ordered_tasks = topological_sort(task_graph)
    execute_sequentially(tasks, ordered_tasks)

if __name__ == "__main__":
    main()
