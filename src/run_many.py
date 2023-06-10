import subprocess
import time
import sys
import os

print('Compile...')
subprocess.check_call(['make', 'compile'])

for i in range(10):
    t0 = time.time()
    print(f'\nIter {i}:')
    env = os.environ.copy()
    env['COMMANDS'] = 'TOP_10_COUNT COUNT'
    env['WARMUP_ITER'] = '1'
    env['NUM_ITER'] = '10'
    try:
        result = subprocess.run([sys.executable, 'src/client.py', 'queries/basic_queries.jsonl', 'tantivy-0.19', 'lucene-9.5.0'], check=True, capture_output=True, env=env)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(e.stderr.decode('utf-8'))
        raise
    os.rename('results.json', f'results/results{i}.json')
    open(f'results/stdout{i}.txt', 'wb').write(result.stdout)
    open(f'results/stderr{i}.txt', 'wb').write(result.stderr)
    t1 = time.time()
    print(f'  done!  [{t1 - t0:.2f}] seconds')
