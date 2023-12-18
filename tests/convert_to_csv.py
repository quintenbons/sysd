#!/usr/bin/env python3
import json
import os
import pandas as pd
import sys

def convert_to_csv(data):
    # Creating a DataFrame for the CSV conversion
    if len(sys.argv) == 2:
        df = pd.DataFrame({
            "start_time": [data["start_time"]],
            "parsing_time": [data["parsing_time"]],
            "scheduling_time": [data["scheduling_time"]],
            "all_jobs_done_time": [data["all_jobs_done_time"]],
            "pulling_time": [data["pulling_time"]],
            "end_time": [data["end_time"]]
        })

        expanded_df = pd.DataFrame({
            "start_time": df['start_time'],
            "parsing_time": df['parsing_time'],
            "scheduling_time": df['scheduling_time'],
            "all_jobs_done_time": df['all_jobs_done_time'],
            "pulling_time": df['pulling_time'],
            "end_time": df['end_time']
        })
    else:
        df = pd.DataFrame({
            "start_time": data["start_time"],
            "parsing_time": data["parsing_time"],
            "scheduling_time": data["scheduling_time"],
            "jobs_running_time": data["jobs_running_time"],
            "jobs_done_time": data["jobs_done_time"],
            "all_jobs_done_time": data["all_jobs_done_time"],
            "pulling_time": data["pulling_time"],
            "end_time": data["end_time"]
        })

        # Expanding the DataFrame to have one row per 'jobs_done_time', duplicating other columns
        expanded_df = pd.DataFrame({
            "start_time": df['start_time'],
            "parsing_time": df['parsing_time'],
            "scheduling_time": df['scheduling_time'],
            "jobs_running_time": pd.Series(df['jobs_running_time'].explode()),
            "jobs_done_time": pd.Series(df['jobs_done_time'].explode()),
            "all_jobs_done_time": df['all_jobs_done_time'],
            "pulling_time": df['pulling_time'],
            "end_time": df['end_time']
        })

    # Resetting the index to ensure proper alignment of data
    expanded_df.reset_index(drop=True, inplace=True)

    return expanded_df

def file_to_csv(filepath: os.PathLike):
    """Convert an \n separated JSON file to a CSV file.
    Ignore lines that don't start with '{' or end with '}'.
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line.startswith('{') and line.endswith('}')]

    data = [json.loads(line) for line in lines]
    dfs = [convert_to_csv(d) for d in data]
    for i, df in enumerate(dfs):
        df['exec_id'] = i
    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.to_csv(filepath + '.csv', index=False)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: python convert_to_csv.py <filename> [true if extra data is needed]')
    file_to_csv(sys.argv[1])
