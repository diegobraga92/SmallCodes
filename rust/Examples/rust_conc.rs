use std::{
    env,
    error::Error,
    fs::File,
    io::Read,
    path::PathBuf,
    thread,
};

use tokio::fs;
use tokio::sync::oneshot;
use zip::ZipArchive;

type DynResult<T> = Result<T, Box<dyn Error + Send + Sync>>;

#[tokio::main]
async fn main() -> DynResult<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        return Err(format!(
            "Usage: {} <input.zip> <output.file>",
            args[0]
        ).into());
    }

    let input = PathBuf::from(&args[1]);
    let output = PathBuf::from(&args[2]);

    // Channel to receive data from the blocking thread
    let (tx, rx) = oneshot::channel();

    // Spawn a blocking OS thread for ZIP parsing
    thread::spawn(move || {
        let result = parse_zip(input);
        let _ = tx.send(result);
    });

    // Await the result asynchronously
    let extracted_bytes = rx
        .await
        .map_err(|_| "ZIP parsing thread was cancelled")??;

    // Async write to output file
    fs::write(&output, extracted_bytes)
        .await
        .map_err(|e| format!("Failed to write output file: {e}"))?;

    println!("Extraction complete -> {}", output.display());
    Ok(())
}

fn parse_zip(path: PathBuf) -> DynResult<Vec<u8>> {
    let file = File::open(&path)
        .map_err(|e| format!("Failed to open zip file {}: {e}", path.display()))?;

    let mut archive = ZipArchive::new(file)
        .map_err(|e| format!("Invalid ZIP archive: {e}"))?;

    if archive.len() == 0 {
        return Err("Zip archive is empty".into());
    }

    // Read the first file in the ZIP
    let mut zipped_file = archive
        .by_index(0)
        .map_err(|e| format!("Failed to read first file in ZIP: {e}"))?;

    let mut buffer = Vec::new();
    zipped_file
        .read_to_end(&mut buffer)
        .map_err(|e| format!("Failed to read zipped file contents: {e}"))?;

    Ok(buffer)
}
