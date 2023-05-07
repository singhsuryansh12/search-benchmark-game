import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.FSDirectory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.nio.file.Paths;

public class BuildIndex {
    public static void main(String[] args) throws IOException {
        final Path outputPath = Paths.get(args[0]);

        final IndexWriterConfig config = new IndexWriterConfig(getTextAnalyzer());
        config.setRAMBufferSizeMB(1000);
        int i = 0, num_skipped = 0;
        try (IndexWriter writer = new IndexWriter(FSDirectory.open(outputPath), config)) {
            try (BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in))) {
                final Document document = new Document();

                TextField bodyField = new TextField("body", "", Field.Store.NO);

                document.add(bodyField);

                String line;
                while ((line = bufferedReader.readLine()) != null) {
                    if (line.trim().isEmpty()) {
                        continue;
                    }
                    i += 1;
                    var parsed_line = line.split("\t");
                    // title date body label
                    if (parsed_line.length != 4) {
                        System.out.println("invalid record, skipping line: " + line);
                        num_skipped += 1;
                        continue;
                    }
                    bodyField.setStringValue(parsed_line[2]);
                    writer.addDocument(document);
                }
            }

            writer.commit();
            System.out.println("Merging");
            writer.forceMerge(1, true);
            System.out.println("Done. Read " + i + " docs." + "Skipped " + num_skipped + " lines");
        }
    }

    public static Analyzer getTextAnalyzer() {
        return  new WhitespaceAnalyzer();
    }

}
