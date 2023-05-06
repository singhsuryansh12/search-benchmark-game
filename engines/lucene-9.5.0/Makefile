NAME ?= "Lucene 9.5.0"
clean:
	@echo "--- Cleaning $(NAME) ---"
	@rm -fr idx
	@rm -fr build

compile: build

serve:
	@java -cp build/libs/search-index-benchmark-game-lucene-1.0-SNAPSHOT-all.jar DoQuery idx

index: idx

build:
	@echo "--- Building $(NAME) ---"
	@gradle clean shadowJar

idx: build
	@echo "--- Indexing $(NAME) ---"
	java -server -cp build/libs/search-index-benchmark-game-lucene-1.0-SNAPSHOT-all.jar BuildIndex idx  < $(CORPUS)
