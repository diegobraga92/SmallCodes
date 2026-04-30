// =============================================================================
// build.rs — Code Generation for gRPC
// =============================================================================
//
// WHAT IS build.rs?
//   In Rust, a build.rs file is a "build script" that Cargo compiles and runs
//   BEFORE compiling the crate itself. It's used for:
//   - Code generation (like our .proto compilation)
//   - Native library linking (e.g., linking to C libraries)
//   - Platform detection
//   - Generating code from configuration
//
// WHAT DOES THIS BUILD SCRIPT DO?
//   1. Finds the protoc compiler (via protoc-bin-vendored)
//   2. Reads proto/task.proto
//   3. Generates Rust code:
//      - Message types (CreateTaskRequest, etc.) via prost
//      - Server/client stubs (TaskService trait, TaskServiceServer) via tonic
//      - File descriptor set (for gRPC reflection) via tonic
//   4. Writes the generated code to $OUT_DIR (a Cargo-managed temp directory)
//
// WHY protoc-bin-vendored?
//   Normally you need to install protoc manually. protoc-bin-vendored bundles
//   a pre-built binary so the build is reproducible and zero-install.
//   Tradeoff: larger download size (~5MB) vs convenience.
//
// WHAT IS A FILE DESCRIPTOR SET?
//   A binary representation of the .proto file that gRPC reflection uses.
//   With reflection enabled, tools like grpcurl can discover services at
//   runtime without needing the .proto file. This is the gRPC equivalent of
//   OpenAPI/Swagger for REST.
// =============================================================================

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Path to our .proto file (relative to the shared crate directory)
    let proto_path = std::path::Path::new("../proto/task.proto");
    // Directory containing .proto files (for import resolution)
    let proto_dir = std::path::Path::new("../proto");

    // Configure prost to use the vendored protoc binary
    let mut config = prost_build::Config::new();
    config.protoc_executable(&protoc_bin_vendored::protoc_bin_path()?);

    // Configure tonic-build to generate both server and client code,
    // plus the file descriptor set for gRPC reflection.
    tonic_build::configure()
        // Generate server-side code (the TaskService trait we implement)
        .build_server(true)
        // Generate client-side code (for potential future gRPC clients)
        .build_client(true)
        // Generate the file descriptor set binary for gRPC reflection
        .file_descriptor_set_path(
            std::path::PathBuf::from(std::env::var("OUT_DIR").unwrap()).join("task_descriptor.bin"),
        )
        // Compile the proto file with our prost config
        .compile_protos_with_config(config, &[proto_path], &[proto_dir])?;

    Ok(())
}
