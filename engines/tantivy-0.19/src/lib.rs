use tantivy::tokenizer::{RemoveLongFilter, TextAnalyzer, TokenizerManager, WhitespaceTokenizer};

pub fn get_tokenizer_manager() -> TokenizerManager {
    let tokenzier_manager = TokenizerManager::default();
    let tokenizer = TextAnalyzer::from(WhitespaceTokenizer).filter(RemoveLongFilter::limit(256));
    tokenzier_manager.register("whitespace", tokenizer);
    tokenzier_manager
}