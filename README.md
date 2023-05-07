
# What is this repo about?
This repository forked from https://github.com/quickwit-oss/search-benchmark-game.

This repo aims to achieve a close comparison between Tantivy with Lucene, notably it tires to use the same search workload from [luceneutil](https://github.com/mikemccand/luceneutil).

The latest result can be found [here](https://tony-x.github.io/search-benchmark-game/).


# The benchmark
## Workload
The corpus used in the benchmark is a snapshot of the wiki text.

```
# wget http://home.apache.org/~mikemccand/enwiki-20120502-lines-1k-fixed-utf8-with-random-label.txt.lzma
```

The search tasks used are from [here](https://github.com/mikemccand/luceneutil/blob/master/tasks/wikimedium.1M.nostopwords.tasks). This repository has a copy, too.

As of now, this benchmark only uses basic text queries which includes
```
TermQuery
BooleanQuery
PhraseQuery (with slop)
```

## Engine details
### Common
* Text analysis: Both engine use a simple white-space tokenizer.

### Tantivy
version: 0.19

Features: All default

### Lucene
version: 9.5.0
* Disabled query cache.


## Methedology
The benchmark uses a client that simulates a closed-system, where a new query is only sent after the completion of the previous one. This is to meansure the best latency from each engine.

The workload is run against with every engine in multiple iterations, including a warmup run at the beginning.


# TODO list
- [ ] Support result level comparison, especially for TOP_10 mode.
- [ ] Understand why certain sloppy phrase queries return different results.
