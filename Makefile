# CORPUS := $(shell pwd)/dev-corpus/20k-enwiki-20120502-lines-1k-fixed-utf8-with-random-label.txt
CORPUS := "$(shell pwd)/dev-corpus/enwiki-20120502-lines-1k-fixed-utf8-with-random-label.txt"
export

WIKI_SRC = "http://home.apache.org/~mikemccand/enwiki-20120502-lines-1k-fixed-utf8-with-random-label.txt.lzma"

# COMMANDS ?=  TOP_10 TOP_10_COUNT COUNT
COMMANDS ?= TOP_10 COUNT

ENGINES ?=  tantivy-0.19 lucene-9.5.0
PORT ?= 12345
QUERY_FILE ?= queries/basic_queries.jsonl

help:
	@grep '^[^#[:space:]].*:' Makefile

all: index

corpus:
	@echo "--- Downloading $(WIKI_SRC) ---"
	@curl -s $(WIKI_SRC) | lzma -d - > $(CORPUS)

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
	@cd web/build && python3 -m http.server $(PORT) --bind localhost
