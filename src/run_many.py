import subprocess
import time
import sys
import os

query_file = sys.argv[1]
iters = int(sys.argv[2])
engines = sys.argv[3:]

RESULTS_OUTPUT_DIR = 'results_many'

print(f'Running bench {iters} times, using queries from {query_file}, testing engines {" ".join(engines)}')

for i in range(10):
    t0 = time.time()
    print(f'\nIter {i}:')
    env = os.environ.copy()
    #env['COMMANDS'] = 'TOP_10_COUNT COUNT'
    #env['WARMUP_ITER'] = '1'
    #env['NUM_ITER'] = '10'
    try:
        result = subprocess.run([sys.executable, 'src/client.py', 'queries/basic_queries.jsonl', 'tantivy-0.19', 'lucene-9.5.0'], check=True, capture_output=True, env=env)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr.decode('utf-8'))
        raise
    os.rename('results.json', f'{RESULTS_OUTPUT_DIR}/results{i}.json')
    open(f'{RESULTS_OUTPUT_DIR}/stdout{i}.txt', 'wb').write(result.stdout)
    open(f'{RESULTS_OUTPUT_DIR}/stderr{i}.txt', 'wb').write(result.stderr)
    t1 = time.time()
    print(f'  done!  [{t1 - t0:.2f}] seconds')
