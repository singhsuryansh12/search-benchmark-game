
# What is this repo about?
This repository is forked from https://github.com/quickwit-oss/search-benchmark-game.

It aims to achieve a close comparison between Tantivy and Lucene using the same search workload from [luceneutil](https://github.com/mikemccand/luceneutil).

The latest results can be found [here](https://tony-x.github.io/search-benchmark-game/).


# The benchmark
## Workload
The corpus used in the benchmark is a snapshot of the English Wikipedia text.

```
# wget http://home.apache.org/~mikemccand/enwiki-20120502-lines-1k-fixed-utf8-with-random-label.txt.lzma
```

The search tasks are from [here](https://github.com/mikemccand/luceneutil/blob/master/tasks/wikimedium.1M.nostopwords.tasks). This repository has a copy, too.

As of now, this benchmark uses only basic text queries which includes:
```
TermQuery
BooleanQuery
PhraseQuery (with slop)
```

## Engine details
### Common
* Text analysis: Both engine use a simple whitespace tokenizer.

### Tantivy
version: 0.19

Features: All default

### Lucene
version: 9.5.0
* Disabled query cache.


## Methedology
The benchmark uses a client that simulates a closed-loop system, where a new query is sent only after the completion of the previous one. This is to measure the lowest latency from each engine.

The workload is run against both engines in multiple iterations, including a warmup run at the beginning.
