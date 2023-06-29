import sys
import json

def main():
    '''
    NOTE: this can only compare two engines, one Tantivy one Lucene, for now
    '''
    
    if len(sys.argv) != 2:
        raise RuntimeError(f'\nUsage: {sys.executable} {sys.argv[0]} <results.json>')

    with open(sys.argv[1]) as f:
        results = json.load(f)

        lucene_engine = None
        tantivy_engine = None

        # collate/invert
        by_mode = {}
        for mode in results.keys():
            by_mode[mode] = {}
            for engine in results[mode].keys():
                if engine.startswith('lucene'):
                    if lucene_engine is None:
                        lucene_engine = engine
                    elif engine != lucene_engine:
                        raise RuntimeError(f'this tool only supports once Lucene engine (saw both {lucene_engine} and {engine}')
                elif engine.startswith('tantivy'):
                    if tantivy_engine is None:
                        tantivy_engine = engine
                    elif engine != tantivy_engine:
                        raise RuntimeError(f'this tool only supports one Tantivy engine (saw both {tantivy_engine} and {engine}')
                    
                for task in results[mode][engine]:
                    cat = task['tags'][0]
                    if cat not in by_mode[mode]:
                        by_mode[mode][cat] = {}
                    by_cat = by_mode[mode][cat]
                    query = task['query']
                    if query not in by_cat:
                        by_cat[query] = {}
                    by_query = by_cat[query]
                    if engine in by_query:
                        raise AssertionError()

                    # duration is usec (microseonds):
                    by_query[engine] = (task['count'], task['duration'][0])

        # 2nd pass: compute pct difference between the engines (only two engines supported for now!)
        for mode, by_cat in by_mode.items():

            for cat, by_query in by_cat.items():

                by_pct_diff = []

                max_query_len = 0
                
                for query, by_engine in by_query.items():

                    lucene_result = by_engine[lucene_engine]
                    tantivy_result = by_engine[tantivy_engine]

                    pct_diff = 100. * (lucene_result[1] / tantivy_result[1] - 1.0)

                    by_pct_diff.append((pct_diff, query, lucene_result, tantivy_result))

                    max_query_len = max(max_query_len, len(query))

                # sort by biggest slowdown of Lucene vs Tantivy
                by_pct_diff.sort(key=lambda x: -x[0])

                print(f'\n{mode} {cat}')
                for pct_diff, query, lucene_result, tantivy_result in by_pct_diff:
                    tantivy_count = tantivy_result[0]
                    lucene_count = lucene_result[0]
                    sys.stdout.write(f'  {pct_diff:5.1f}% {query:{max_query_len+1}s} {lucene_result[1]/1000.:5.1f} ms {tantivy_result[1]/1000:5.1f} ms count={lucene_count:<6d}')
                    if lucene_count != tantivy_count:
                        sys.stdout.write(f' (WARNING: tantivy_count={tantivy_count})')
                    sys.stdout.write('\n')
                        
                    

if __name__ == '__main__':
    main()
