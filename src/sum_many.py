import os
import sys
import glob
import json
import statistics

tasks = None

all_results = {}
run_count = 0

# load and collate all results
for results_file in glob.glob('results_many/results?.json'):
    results = json.load(open(results_file, 'r'))
    run_count += 1
    if tasks is None:
        tasks = list(results.keys())
        engines = list(results[tasks[0]].keys())
    for task in tasks:
        if task not in all_results:
            all_results[task] = {}
        for engine in engines:
            if engine not in all_results[task]:
                all_results[task][engine] = [list(x) for x in [()] * len(results[task][engine])]
            for i, query in enumerate(results[task][engine]):
                all_results[task][engine][i].append(query)
                # sanity checks
                if all_results[task][engine][i][0]['query'] != query['query']:
                    raise RuntimeError('WTF?')
                if all_results[task][engine][i][0]['count'] != query['count']:
                    raise RuntimeError('WTF?')

aggd = {}

# extract min_times by (task, engine, query)
for task in tasks:
    for engine in engines:
        all_results_mins = []
        for query_runs in all_results[task][engine]:
            all_mins = []
            for run in query_runs:
                all_mins.append(run['duration'][0])
            all_mins.sort()
            if all_mins[0] > 1000:
                stdev = statistics.stdev(all_mins)
                mean = statistics.mean(all_mins)
                #print(f'{task} {engine} {query_runs[0]["tags"][0]} {query_runs[0]["query"]}: {pct_diff} {all_mins}')
                all_results_mins.append((100.*stdev/mean, query_runs[0], all_mins))
        all_results_mins.sort(key=lambda x: -x[0])
        aggd[(task, engine)] = all_results_mins

# print highest pct diff by (task, engine)
for (task, engine), all_results_mins in aggd.items():
    print(f'\nlooksee: {task} {engine}:')
    for stdev_pct, query, mins in all_results_mins[:20]:
        print(f'  stdev {stdev_pct:.1f}%: {query["query"]} {mins}')
