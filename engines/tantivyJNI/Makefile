NAME := "tantivyJNI"
export CORPUS

clean:
	@rm -fr idx
	@rm -fr target

clean-index:
	@rm -fr idx

compile: target/release/build_index

index: target/release/build_index
	@echo "--- Indexing $(NAME) with $(INDEX_DELETE_PCT)% deletes ---" >&2
	@mkdir -p idx
	@target/release/build_index idx $(INDEX_DELETE_PCT) < $(CORPUS) >&2

target/release/%: src/bin/%.rs src/lib.rs
	@echo "--- Building $(NAME) binary ---" >&2
	@cargo build --release --bin $(notdir $@)
