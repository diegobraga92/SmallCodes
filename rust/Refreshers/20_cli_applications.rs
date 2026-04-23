//// RUST CLI APPLICATIONS - CLAP AND BEST PRACTICES
/// Comprehensive guide to building command-line applications in Rust
/// Covers argument parsing, subcommands, configuration, and user experience

// ============================================================================
// 1. CLAP - COMMAND LINE ARGUMENT PARSER
// ============================================================================

/// Clap is the most popular CLI framework for Rust
/// Two approaches:
/// 1. Derive API (recommended): Uses attributes on structs
/// 2. Builder API: Programmatic construction

/*
INSTALLATION:
cargo add clap --features derive
*/


// ============================================================================
// 2. BASIC CLI WITH DERIVE API
// ============================================================================

/*
use clap::Parser;

/// Simple program to greet a person
#[derive(Parser, Debug)]
#[command(name = "myapp")]
#[command(version = "1.0")]
#[command(about = "Does awesome things", long_about = None)]
struct Args {
    /// Name of the person to greet
    #[arg(short, long)]
    name: String,
    
    /// Number of times to greet
    #[arg(short, long, default_value_t = 1)]
    count: u8,
}

fn main() {
    let args = Args::parse();
    
    for _ in 0..args.count {
        println!("Hello, {}!", args.name);
    }
}

// Usage:
// myapp --name Alice
// myapp -n Bob --count 3
// myapp --help
// myapp --version
*/


// ============================================================================
// 3. ADVANCED ARGUMENT TYPES
// ============================================================================

/*
use clap::Parser;
use std::path::PathBuf;

#[derive(Parser, Debug)]
struct Args {
    /// Input file
    #[arg(short, long, value_name = "FILE")]
    input: PathBuf,
    
    /// Output file (optional)
    #[arg(short, long)]
    output: Option<PathBuf>,
    
    /// Verbosity level (can be used multiple times: -v, -vv, -vvv)
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,
    
    /// Enable debug mode
    #[arg(short, long)]
    debug: bool,
    
    /// Configuration format
    #[arg(value_enum)]
    format: Format,
    
    /// Additional files (can be repeated)
    #[arg(short = 'f', long)]
    files: Vec<PathBuf>,
}

#[derive(Debug, Clone, clap::ValueEnum)]
enum Format {
    Json,
    Yaml,
    Toml,
}

fn main() {
    let args = Args::parse();
    
    println!("Input: {:?}", args.input);
    println!("Verbose level: {}", args.verbose);
    println!("Format: {:?}", args.format);
}
*/


// ============================================================================
// 4. SUBCOMMANDS
// ============================================================================

/*
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "git-like")]
#[command(about = "A git-like CLI tool", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize a new repository
    Init {
        /// Repository path
        path: Option<PathBuf>,
    },
    
    /// Add files to staging
    Add {
        /// Files to add
        files: Vec<PathBuf>,
        
        /// Add all files
        #[arg(short, long)]
        all: bool,
    },
    
    /// Commit changes
    Commit {
        /// Commit message
        #[arg(short, long)]
        message: String,
        
        /// Amend previous commit
        #[arg(short, long)]
        amend: bool,
    },
    
    /// Show status
    Status,
}

fn main() {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Init { path } => {
            let repo_path = path.unwrap_or_else(|| PathBuf::from("."));
            println!("Initializing repository at {:?}", repo_path);
        }
        Commands::Add { files, all } => {
            if all {
                println!("Adding all files");
            } else {
                println!("Adding files: {:?}", files);
            }
        }
        Commands::Commit { message, amend } => {
            if amend {
                println!("Amending commit with message: {}", message);
            } else {
                println!("Creating commit: {}", message);
            }
        }
        Commands::Status => {
            println!("Showing status");
        }
    }
}

// Usage:
// myapp init
// myapp init /path/to/repo
// myapp add file1.txt file2.txt
// myapp add --all
// myapp commit -m "Initial commit"
// myapp status
*/


// ============================================================================
// 5. VALIDATION AND CUSTOM TYPES
// ============================================================================

/*
use clap::Parser;
use std::num::ParseIntError;

#[derive(Parser)]
struct Args {
    /// Port number (1-65535)
    #[arg(short, long, value_parser = clap::value_parser!(u16).range(1..=65535))]
    port: u16,
    
    /// Email address
    #[arg(short, long, value_parser = validate_email)]
    email: String,
}

fn validate_email(s: &str) -> Result<String, String> {
    if s.contains('@') && s.contains('.') {
        Ok(s.to_string())
    } else {
        Err(String::from("Invalid email format"))
    }
}

// Custom type parsing
struct Percentage(u8);

impl std::str::FromStr for Percentage {
    type Err = String;
    
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let num: u8 = s.parse()
            .map_err(|e: ParseIntError| e.to_string())?;
        
        if num > 100 {
            Err("Percentage must be 0-100".to_string())
        } else {
            Ok(Percentage(num))
        }
    }
}
*/


// ============================================================================
// 6. ENVIRONMENT VARIABLES
// ============================================================================

/*
use clap::Parser;

#[derive(Parser)]
struct Args {
    /// API key (can also be set via API_KEY env var)
    #[arg(long, env = "API_KEY")]
    api_key: String,
    
    /// Log level
    #[arg(long, env = "LOG_LEVEL", default_value = "info")]
    log_level: String,
    
    /// Database URL
    #[arg(long, env)]
    database_url: String,
}

// Usage:
// myapp --api-key xyz
// API_KEY=xyz myapp
// API_KEY=xyz DATABASE_URL=postgres://... myapp
*/


// ============================================================================
// 7. INTERACTIVE CLI (PROMPTS)
// ============================================================================

/// For interactive prompts, use dialoguer crate

/*
use dialoguer::{Input, Confirm, Select, MultiSelect, Password};

fn interactive_setup() {
    // Text input
    let name: String = Input::new()
        .with_prompt("Your name")
        .default("Alice".into())
        .interact_text()
        .unwrap();
    
    // Password (hidden input)
    let password = Password::new()
        .with_prompt("Password")
        .with_confirmation("Confirm password", "Passwords don't match")
        .interact()
        .unwrap();
    
    // Yes/No confirmation
    let confirmed = Confirm::new()
        .with_prompt("Do you want to continue?")
        .interact()
        .unwrap();
    
    // Single selection
    let items = vec!["Option 1", "Option 2", "Option 3"];
    let selection = Select::new()
        .with_prompt("Choose one")
        .items(&items)
        .default(0)
        .interact()
        .unwrap();
    
    // Multiple selection
    let selections = MultiSelect::new()
        .with_prompt("Choose multiple")
        .items(&items)
        .interact()
        .unwrap();
    
    println!("Name: {}", name);
    println!("Confirmed: {}", confirmed);
    println!("Selected: {}", items[selection]);
}
*/


// ============================================================================
// 8. PROGRESS BARS
// ============================================================================

/// Use indicatif for progress indicators

/*
use indicatif::{ProgressBar, ProgressStyle};
use std::time::Duration;

fn download_files() {
    let pb = ProgressBar::new(100);
    
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner:.green} [{bar:40.cyan/blue}] {pos}/{len} {msg}")
            .unwrap()
            .progress_chars("#>-")
    );
    
    for i in 0..100 {
        pb.set_position(i);
        pb.set_message(format!("Processing item {}", i));
        std::thread::sleep(Duration::from_millis(50));
    }
    
    pb.finish_with_message("Done!");
}

// Spinner for indefinite operations
fn processing() {
    let spinner = ProgressBar::new_spinner();
    spinner.set_message("Processing...");
    
    for _ in 0..100 {
        spinner.tick();
        std::thread::sleep(Duration::from_millis(50));
    }
    
    spinner.finish_with_message("Complete!");
}
*/


// ============================================================================
// 9. COLORED OUTPUT
// ============================================================================

/// Use colored crate for terminal colors

/*
use colored::*;

fn print_messages() {
    println!("{}", "Success!".green());
    println!("{}", "Warning!".yellow());
    println!("{}", "Error!".red());
    println!("{}", "Info".blue());
    
    // With styles
    println!("{}", "Bold text".bold());
    println!("{}", "Italic text".italic());
    println!("{}", "Underlined".underline());
    
    // Combined
    println!("{}", "Success!".green().bold());
    println!("{}", "Critical error!".red().bold().underline());
}
*/


// ============================================================================
// 10. TABLE OUTPUT
// ============================================================================

/// Use comfy-table for formatted tables

/*
use comfy_table::{Table, Cell, Color};

fn display_data() {
    let mut table = Table::new();
    
    table
        .set_header(vec!["ID", "Name", "Status"])
        .add_row(vec!["1", "Alice", "Active"])
        .add_row(vec!["2", "Bob", "Inactive"])
        .add_row(vec!["3", "Charlie", "Active"]);
    
    println!("{table}");
}
*/


// ============================================================================
// 11. ERROR HANDLING IN CLI
// ============================================================================

/*
use anyhow::{Result, Context};
use std::fs;

fn main() -> Result<()> {
    let args = Args::parse();
    
    // Use anyhow for better error messages
    let content = fs::read_to_string(&args.input)
        .context("Failed to read input file")?;
    
    let processed = process_content(&content)
        .context("Failed to process content")?;
    
    if let Some(output) = args.output {
        fs::write(&output, processed)
            .context("Failed to write output file")?;
    } else {
        println!("{}", processed);
    }
    
    Ok(())
}

fn process_content(content: &str) -> Result<String> {
    // Processing logic
    Ok(content.to_uppercase())
}
*/


// ============================================================================
// 12. CONFIGURATION FILES
// ============================================================================

/*
use serde::{Serialize, Deserialize};
use std::path::PathBuf;
use anyhow::Result;

#[derive(Serialize, Deserialize, Debug)]
struct Config {
    api_url: String,
    timeout: u64,
    features: Vec<String>,
}

impl Config {
    fn load(path: &PathBuf) -> Result<Self> {
        let content = std::fs::read_to_string(path)?;
        
        // Support multiple formats
        if path.extension().map_or(false, |e| e == "json") {
            Ok(serde_json::from_str(&content)?)
        } else if path.extension().map_or(false, |e| e == "yaml" || e == "yml") {
            Ok(serde_yaml::from_str(&content)?)
        } else if path.extension().map_or(false, |e| e == "toml") {
            Ok(toml::from_str(&content)?)
        } else {
            Err(anyhow::anyhow!("Unsupported config format"))
        }
    }
    
    fn default_path() -> PathBuf {
        dirs::config_dir()
            .unwrap()
            .join("myapp")
            .join("config.toml")
    }
}
*/


// ============================================================================
// 13. LOGGING IN CLI
// ============================================================================

/*
use tracing::{info, warn, error};
use tracing_subscriber::{fmt, EnvFilter};

fn setup_logging(verbose: u8) {
    let level = match verbose {
        0 => "warn",
        1 => "info",
        2 => "debug",
        _ => "trace",
    };
    
    tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::new(level))
        .with_target(false)
        .with_timer(fmt::time::uptime())
        .init();
}

fn main() {
    let args = Args::parse();
    setup_logging(args.verbose);
    
    info!("Starting application");
    // ... rest of app
}
*/


// ============================================================================
// 14. BEST PRACTICES
// ============================================================================

/// CLI BEST PRACTICES:
/// 
/// USER EXPERIENCE:
/// ✓ Provide --help and --version
/// ✓ Good error messages with context
/// ✓ Progress indicators for long operations
/// ✓ Confirm destructive operations
/// ✓ Support both flags and env vars
/// ✓ Sensible defaults
/// ✓ Color output (respect NO_COLOR)
/// ✓ Support piping (stdin/stdout)
/// 
/// ERROR HANDLING:
/// ✓ Use anyhow for better errors
/// ✓ Provide actionable error messages
/// ✓ Non-zero exit codes on error
/// ✓ Log errors to stderr
/// ✓ Don't show stack traces to users
/// 
/// PERFORMANCE:
/// ✓ Fast startup (lazy initialization)
/// ✓ Async I/O for network operations
/// ✓ Stream large files (don't load all to memory)
/// ✓ Show progress for slow operations
/// 
/// COMPATIBILITY:
/// ✓ Follow Unix conventions
/// ✓ Support common flags (-v, -h, -V)
/// ✓ Use standard exit codes
/// ✓ Respect environment variables (NO_COLOR, PAGER)
/// 
/// DISTRIBUTION:
/// ✓ Static binary compilation
/// ✓ Cross-platform support
/// ✓ Package for major platforms (cargo install, brew, apt)
/// ✓ Auto-update capability


// ============================================================================
// 15. COMPLETE EXAMPLE
// ============================================================================

/*
use clap::{Parser, Subcommand};
use anyhow::{Result, Context};
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "mytool")]
#[command(version, about, long_about = None)]
struct Cli {
    /// Verbosity level
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,
    
    /// Configuration file
    #[arg(short, long)]
    config: Option<PathBuf>,
    
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Process a file
    Process {
        /// Input file
        input: PathBuf,
        
        /// Output file
        #[arg(short, long)]
        output: Option<PathBuf>,
    },
    
    /// Show information
    Info,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    
    // Setup logging based on verbosity
    setup_logging(cli.verbose);
    
    // Load configuration
    let config = if let Some(path) = cli.config {
        Config::load(&path)?
    } else {
        Config::default()
    };
    
    // Execute command
    match cli.command {
        Commands::Process { input, output } => {
            process_command(input, output)?;
        }
        Commands::Info => {
            info_command(&config)?;
        }
    }
    
    Ok(())
}

fn process_command(input: PathBuf, output: Option<PathBuf>) -> Result<()> {
    use indicatif::{ProgressBar, ProgressStyle};
    
    let content = std::fs::read_to_string(&input)
        .context("Failed to read input file")?;
    
    let pb = ProgressBar::new(100);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner} [{bar:40}] {pos}/{len}")
            .unwrap()
    );
    
    // Simulate processing
    for i in 0..100 {
        pb.set_position(i);
        std::thread::sleep(std::time::Duration::from_millis(20));
    }
    pb.finish();
    
    let result = content.to_uppercase();
    
    if let Some(out) = output {
        std::fs::write(&out, result)
            .context("Failed to write output")?;
        println!("{}", "✓ Processed successfully".green());
    } else {
        println!("{}", result);
    }
    
    Ok(())
}
*/


fn main() {
    println!("=== RUST CLI APPLICATIONS ===\n");
    println!("This file demonstrates CLI patterns with clap.");
    println!("See comments for complete examples.\n");
    
    println!("CLAP FEATURES:");
    println!("  ✓ Derive API (attributes on structs)");
    println!("  ✓ Automatic help and version");
    println!("  ✓ Subcommands");
    println!("  ✓ Validation");
    println!("  ✓ Environment variables");
    
    println!("\nUSER EXPERIENCE:");
    println!("  • dialoguer - Interactive prompts");
    println!("  • indicatif - Progress bars");
    println!("  • colored - Terminal colors");
    println!("  • comfy-table - Formatted tables");
    
    println!("\nERROR HANDLING:");
    println!("  • anyhow - Better error messages");
    println!("  • Context for error chains");
    println!("  • Non-zero exit codes");
    
    println!("\nBEST PRACTICES:");
    println!("  ✓ Good help messages");
    println!("  ✓ Progress for long operations");
    println!("  ✓ Confirm destructive actions");
    println!("  ✓ Support env vars and flags");
    println!("  ✓ Fast startup time");
    
    println!("\n=== Complete ===");
}

/// DEPENDENCIES:
/// ```toml
/// [dependencies]
/// clap = { version = "4", features = ["derive", "env"] }
/// anyhow = "1"
/// dialoguer = "0.11"
/// indicatif = "0.17"
/// colored = "2"
/// comfy-table = "7"
/// serde = { version = "1", features = ["derive"] }
/// serde_json = "1"
/// serde_yaml = "0.9"
/// toml = "0.8"
/// dirs = "5"
/// tracing = "0.1"
/// tracing-subscriber = "0.3"
/// ```

/// KEY TAKEAWAYS:
/// 
/// 1. Use clap with derive API for argument parsing
/// 2. Implement subcommands for complex CLIs
/// 3. Provide excellent help messages
/// 4. Use anyhow for error handling
/// 5. Show progress for long operations (indicatif)
/// 6. Interactive prompts with dialoguer
/// 7. Color output with colored crate
/// 8. Support both CLI args and env vars
/// 9. Load configuration from files
/// 10. Fast startup and good performance
/// 11. Follow Unix conventions
/// 12. Test your CLI thoroughly
