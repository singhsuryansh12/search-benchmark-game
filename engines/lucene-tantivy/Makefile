export CORPUS

HEAP = 4g

NAME ?= "Lucene-Tantivy"
clean:
	@echo "--- Cleaning $(NAME) ---"
	@rm -fr idx
	@rm -fr build
	@rm -fr target

clean-index:
	@rm -fr idx

compile: build

serve:
	@java -Xmx$(HEAP) -Xms$(HEAP) -XX:+UseParallelGC -cp build/libs/search-index-benchmark-game-lucene-tantivy-1.0-SNAPSHOT-all.jar DoQuery idx

index: idx

build: src/main/java/*.java
	@echo "--- Building $(NAME) ---"
	@cargo build --release
	@gradle clean shadowJar

idx: build
	@echo "--- Indexing $(NAME) with %$(INDEX_DELETE_PCT) deletes ---"
	@mkdir -p idx
	java -server -cp build/libs/search-index-benchmark-game-lucene-tantivy-1.0-SNAPSHOT-all.jar BuildIndex idx $(INDEX_DELETE_PCT) < $(CORPUS)
