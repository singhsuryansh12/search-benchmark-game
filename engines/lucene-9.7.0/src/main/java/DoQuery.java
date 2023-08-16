import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.nio.file.Paths;

public class DoQuery {
    public static void main(String[] args) throws IOException, ParseException {
        final Path indexDir = Paths.get(args[0]);
        try (IndexReader reader = DirectoryReader.open(FSDirectory.open(indexDir))) {
            final IndexSearcher searcher = new IndexSearcher(reader);
            searcher.setQueryCache(null);
            try (BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in))) {
                final QueryParser queryParser = new QueryParser("body", BuildIndex.getTextAnalyzer());
                String line;
                while ((line = bufferedReader.readLine()) != null) {
                    final String[] fields = line.trim().split("\t");

                    final String command = fields[0];
                    if (!command.equals("TOP_N_DOCS")) {
                        assert fields.length == 2;
                    }
                    final String query_str = fields[1];
                    Query query = queryParser
                              .parse(query_str);
                    String result;
                    long t0 = System.nanoTime();
                    switch (command) {
                        case "COUNT":
                        {
                            int count = searcher.count(query);
                            result = Integer.toString(count);
                        }
                            break;
                        case "TOP_10":
                        {
                            final TopDocs topDocs = searcher.search(query, 10);
                            int count = (int) topDocs.totalHits.value;
                            result = Integer.toString(count);
                        }
                            break;
                        case "TOP_10_COUNT":
                        {
                            // NOTE: this disables BMW (by passing 2nd argument Integer.MAX_VALUE
                            final TopScoreDocCollector topScoreDocCollector = TopScoreDocCollector.create(10, Integer.MAX_VALUE);
                            searcher.search(query, topScoreDocCollector);
                            int count = topScoreDocCollector.getTotalHits();
                            result = Integer.toString(count);
                        }
                            break;
                        case "TOP_N_DOCS":
                        {
                            assert fields.length == 3;
                            int n = Integer.parseInt(fields[2]);
                            // TODO: why not just the IS.search method?
                            final TopScoreDocCollector topScoreDocCollector = TopScoreDocCollector.create(n, n);
                            searcher.search(query, topScoreDocCollector);
                            StringBuilder sb = new StringBuilder();
                            var docs = topScoreDocCollector.topDocs().scoreDocs;
                            sb.append(docs.length);
                            for (var scoreDoc : docs) {
                                sb.append(" ").append(scoreDoc.doc);
                            }
                            result = sb.toString();
                        }
                            break;
                        default:
                            result = "UNSUPPORTED";
                            break;
                    }
                    // #14: paranoia
                    long t1 = System.nanoTime();
                    System.out.println((t1 - t0) + " " + result);
                    System.out.flush();
                }
            }
        }
    }
}
