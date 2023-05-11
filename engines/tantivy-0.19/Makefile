export CORPUS

clean:
	@rm -fr idx
	@rm -fr target

clean-index:
	@rm -fr idx

index: binaries
	@echo "--- Indexing tantivy ----"
	@mkdir -p idx
	export RUST_LOG=info && target/release/build_index idx < $(CORPUS)

serve: target/release/do_query
	@target/release/do_query idx

target/release/%:
	@echo "--- Building tantivy's binary ---"
	@cargo build --release --bin $(notdir $@)

binaries: target/release/build_index target/release/do_query
