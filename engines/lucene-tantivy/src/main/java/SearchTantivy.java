class SearchTantivy {
    // This declares that the static `hello` method will be provided
    // a native library.
    
    public static native void buildindex(String output_dir, int idx_del_pct);
    public static native void doquery(String input_dir);

    static {
        // This actually loads the shared object that we'll be creating.
        // The actual location of the .so or .dll may differ based on your
        // platform.
    // System.out.println(System.getProperty("java.library.path"));
    // System.setProperty("java.library.path", "./mylib/target/debug");
    System.load("/Volumes/workplace/TantivyHackathon/search-benchmark-game/engines/lucene-tantivy/target/release/libtantivy_jni.dylib");
    }

    // The rest is just regular ol' Java!
    public static void main(String[] args) {
        // System.out.println("In SearchTantivy main function");
    }
}