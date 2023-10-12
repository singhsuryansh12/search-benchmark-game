use std::path::{Path, PathBuf};
use jni::JNIEnv;
use jni::objects::{JClass, JString, JObject, JObjectArray};
use jni::sys::{jint, jobjectArray};

use crate::util::{build_index, do_query};
use tantivy::tokenizer::{RemoveLongFilter, TextAnalyzer, TokenizerManager};
use whitespace_tokenizer_fork::WhitespaceTokenizer;

pub mod util;

#[no_mangle]
pub extern "system" fn Java_SearchTantivy_buildindex<'local>(
    mut env: JNIEnv<'local>,
    class: JClass<'local>,
    output_dir: JString<'local>,
    index_delete_pct: jint,
) {
    // First, we have to get the string out of Java. Check out the `strings`
    // module for more info on how this works.
    let output_dir: String = String::from(env
        .get_string(&output_dir)
        .expect("Couldn't get java string"));

    let _ = build_index::main_inner(&PathBuf::from(output_dir), index_delete_pct);

}

#[no_mangle]
pub extern "system" fn Java_SearchTantivy_doquery<'local>(
    mut env: JNIEnv<'local>,
    class: JClass<'local>,
    index_dir: JString<'local>,
    query_field: JString<'local>,
    command: JString<'local>,
) -> JString<'local> {
    let idx_dir: String = String::from(env
        .get_string(&index_dir)
        .expect("Couldn't get java string"));

        // let array_length = env.get_array_length(&query_fields).expect("Failed to get array length");

        // let mut rust_strings: Vec<String> = Vec::new();

        // for i in 0..array_length {
        //     let query_object: JObject = env.get_object_array_element(&query_fields, i).expect("Failed to get array element");
        //     let rust_string: String = env.get_string(&JString::from(query_object)).expect("Failed to convert to JString").into();
            
        //     // Convert the JString to a Rust string and push it into the vector.
        //     // let rust_string = env.get_string_utf_chars(jstring).expect("Failed to get UTF-8 string");
            
        //     rust_strings.push(rust_string);
            
        //     // Release the JString to avoid memory leaks.
        //     // env.release_string_utf_chars(jstring, rust_string);
        // }
        let query_fld: String = String::from(env
            .get_string(&query_field)
            .expect("Couldn't get java string"));
        let cmd: String = String::from(env
            .get_string(&command)
            .expect("Couldn't get java string"));

    let result = do_query::main_inner(&Path::new(&idx_dir), query_fld, cmd);
    env.new_string(result.unwrap()).expect("Failed to create JString from Rust string")
}


pub fn get_tokenizer_manager() -> TokenizerManager {
    let tokenzier_manager = TokenizerManager::default();
    let tokenizer = TextAnalyzer::builder(WhitespaceTokenizer).filter(RemoveLongFilter::limit(256)).build();
    tokenzier_manager.register("whitespace", tokenizer);
    tokenzier_manager
}

mod whitespace_tokenizer_fork {

    use tantivy::tokenizer::{Token, Tokenizer, TokenStream};
    use std::str::CharIndices;

    /// Tokenize the text by splitting on whitespaces.
    #[derive(Clone)]
    pub struct WhitespaceTokenizer;

    pub struct WhitespaceTokenStream<'a> {
        text: &'a str,
        chars: CharIndices<'a>,
        token: Token,
    }

    impl Tokenizer for WhitespaceTokenizer {
        type TokenStream<'a> = WhitespaceTokenStream<'a>;

        fn token_stream<'a>(&'a mut self, text: &'a str) -> WhitespaceTokenStream<'a> {
            WhitespaceTokenStream {
                text,
                chars: text.char_indices(),
                token: Token::default(),
            }
        }
    }

    impl<'a> WhitespaceTokenStream<'a> {
        // search for the end of the current token.
        fn search_token_end(&mut self) -> usize {
            (&mut self.chars)
                .filter(|&(_, ref c)| c.is_whitespace())
                .map(|(offset, _)| offset)
                .next()
                .unwrap_or(self.text.len())
        }
    }

    impl<'a> TokenStream for WhitespaceTokenStream<'a> {
        fn advance(&mut self) -> bool {
            self.token.text.clear();
            self.token.position = self.token.position.wrapping_add(1);
            while let Some((offset_from, c)) = self.chars.next() {
                if !c.is_whitespace() {
                    let offset_to = self.search_token_end();
                    self.token.offset_from = offset_from;
                    self.token.offset_to = offset_to;
                    self.token.text.push_str(&self.text[offset_from..offset_to]);
                    return true;
                }
            }
            false
        }

        fn token(&self) -> &Token {
            &self.token
        }

        fn token_mut(&mut self) -> &mut Token {
            &mut self.token
        }
    }

    #[cfg(test)]
    mod tests {
        use tantivy::tokenizer::{TextAnalyzer, Token};

        use super::WhitespaceTokenizer;

        #[test]
        fn test_whitespace_tokenizer_with_unicode_spaces() {
            let tokens = token_stream_helper("わ |　か　　花");
            assert_eq!(tokens.len(), 4);
        }

        fn token_stream_helper(text: &str) -> Vec<Token> {
            let mut a = TextAnalyzer::from(WhitespaceTokenizer);
            let mut token_stream = a.token_stream(text);
            let mut tokens: Vec<Token> = vec![];
            let mut add_token = |token: &Token| {
                tokens.push(token.clone());
            };
            token_stream.process(&mut add_token);
            tokens
        }
    }
}
