use futures::executor::block_on;
use std::env;
use std::io::BufRead;
use std::path::Path;
use tantivy::schema::{Schema, TEXT};
use tantivy::{doc, IndexBuilder};
use tantivy_bench::get_tokenizer_manager;

fn main() {
    let args: Vec<String> = env::args().collect();
    main_inner(Path::new(&args[1])).unwrap();
}

fn main_inner(output_dir: &Path) -> tantivy::Result<()> {
    env_logger::init();

    let mut schema_builder = Schema::builder();

    let body = schema_builder.add_text_field(
        "body",
        TEXT.set_indexing_options(
            TEXT.get_indexing_options()
                .unwrap()
                .clone()
                .set_tokenizer("whitespace"),
        ),
    );
    let schema = schema_builder.build();

    let index = IndexBuilder::new()
        .schema(schema)
        .tokenizers(get_tokenizer_manager())
        .create_in_dir(output_dir)
        .expect("Failed to create index");

    let mut i = 0;
    let mut num_skipped = 0;
    {
        let mut index_writer = index
            .writer_with_num_threads(4, 2_000_000_000)
            .expect("failed to create index writer");
        let stdin = std::io::stdin();

        for line in stdin.lock().lines() {
            let line = line?;
            if line.trim().is_empty() {
                continue;
            }
            // (title, date, body, label)
            let parsed_line: Vec<&str> = line.split('\t').collect();
            i += 1;
            if parsed_line.len() != 4 {
                println!("Skippig malformed line: {}", line);
                num_skipped += 1;
                continue;
            }
            if i % 100_000 == 0 {
                println!("{}", i);
            }
            let doc = doc!(
                body => parsed_line[2]
            );
            index_writer.add_document(doc).unwrap();
        }

        index_writer.commit()?;
        index_writer.wait_merging_threads()?;
    }
    let segment_ids = index.searchable_segment_ids()?;
    let mut index_writer = index
        .writer(1_500_000_000)
        .expect("failed to create index writer");
    block_on(index_writer.merge(&segment_ids))?;
    block_on(index_writer.garbage_collect_files())?;
    println!("Done. Read {i} docs, skipped {num_skipped}");
    Ok(())
}
