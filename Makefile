CORPUS := $(shell pwd)/dev-corpus/20k-enwiki-20120502-lines-1k-fixed-utf8-with-random-label.txt
# CORPUS := "/local/home/tonyx/wss/luceneutil/data/enwiki-20120502-lines-1k-fixed-utf8-with-random-label.txt"
export

WIKI_SRC = "https://www.dropbox.com/s/wwnfnu441w1ec9p/wiki-articles.json.bz2"

# COMMANDS ?=  TOP_10 TOP_10_COUNT COUNT
COMMANDS ?= TOP_10 COUNT

# ENGINES ?= tantivy-0.13 lucene-8.4.0 pisa-0.8.2 rucene-0.1 bleve-0.8.0-scorch rucene-0.1 tantivy-0.11 tantivy-0.14 tantivy-0.15 tantivy-0.16 tantivy-0.17 tantivy-0.18 tantivy-0.19
# ENGINES ?= tantivy-0.16 lucene-8.10.1 pisa-0.8.2 bleve-0.8.0-scorch rucene-0.1
ENGINES ?=  tantivy-0.19 lucene-8.10.1
PORT ?= 12345
QUERY_FILE ?= queries/basic_queries.jsonl

help:
	@grep '^[^#[:space:]].*:' Makefile

all: index

corpus:
	@echo "--- Downloading $(WIKI_SRC) ---"
	@curl -# -L "$(WIKI_SRC)" | bunzip2 -c | python3 corpus_transform.py > $(CORPUS)

clean:
	@echo "--- Cleaning directories ---"
	@rm -fr results
	@for engine in $(ENGINES); do cd ${shell pwd}/engines/$$engine && make clean ; done

index:
	@echo "--- Indexing corpus ---"
	@for engine in $(ENGINES); do cd ${shell pwd}/engines/$$engine && make index ; done

bench:
	@echo "--- Benchmarking ---"
	@rm -fr results
	@mkdir results
	@python3 src/client.py $(QUERY_FILE) $(ENGINES)

compile:
	@echo "--- Compiling binaries ---"
	@for engine in $(ENGINES); do cd ${shell pwd}/engines/$$engine && make compile ; done

serve:
	@echo "--- Serving results ---"
	@cp results.json web/build/results.json
	@cd web/build && python3 -m http.server $(PORT)
