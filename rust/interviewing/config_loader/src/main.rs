use serde::Deserialize;
use std::fs;
use std::path::{Path, PathBuf};
use thiserror::Error;

// =====================
// Domain Model
// =====================

#[derive(Debug, Deserialize, PartialEq)]
pub struct AppConfig {
    pub app_name: String,
    pub port: u16,
    pub debug: bool,
}

// =====================
// Error Modeling
// =====================

#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("I/O error while reading config: {0}")]
    Io(#[from] std::io::Error),

    #[error("JSON parse error: {0}")]
    Json(#[from] serde_json::Error),

    #[error("TOML parse error: {0}")]
    Toml(#[from] toml::de::Error),

    #[error("Unsupported config format")]
    UnsupportedFormat,
}

// =====================
// IO Layer
// =====================

pub fn load_file(path: &Path) -> Result<String, ConfigError> {
    Ok(fs::read_to_string(path)?)
}

// =====================
// Parsing Layer
// =====================

pub fn parse_config(contents: &str, extension: &str) -> Result<AppConfig, ConfigError> {
    match extension {
        "json" => Ok(serde_json::from_str(contents)?),
        "toml" => Ok(toml::from_str(contents)?),
        _ => Err(ConfigError::UnsupportedFormat),
    }
}

// =====================
// Orchestration Layer
// =====================

pub fn load_config(path: &Path) -> Result<AppConfig, ConfigError> {
    let extension = path
        .extension()
        .and_then(|ext| ext.to_str())
        .ok_or(ConfigError::UnsupportedFormat)?;

    let contents = load_file(path)?;
    parse_config(&contents, extension)
}

// =====================
// Main
// =====================

fn main() {
    let path = std::env::args()
        .nth(1)
        .unwrap_or_else(|| "config.toml".to_string());

    match load_config(Path::new(&path)) {
        Ok(config) => {
            println!("Config loaded successfully:");
            println!("{:#?}", config);
        }
        Err(e) => {
            eprintln!("Failed to load config: {}", e);
            std::process::exit(1);
        }
    }
}

// =====================
// Tests
// =====================

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::{SystemTime, UNIX_EPOCH};

    // -------- Parsing Tests --------

    #[test]
    fn parse_valid_json() {
        let json = r#"
        {
            "app_name": "test-app",
            "port": 8080,
            "debug": true
        }
        "#;

        let config = parse_config(json, "json").unwrap();

        assert_eq!(
            config,
            AppConfig {
                app_name: "test-app".into(),
                port: 8080,
                debug: true
            }
        );
    }

    #[test]
    fn parse_valid_toml() {
        let toml = r#"
            app_name = "test-app"
            port = 3000
            debug = false
        "#;

        let config = parse_config(toml, "toml").unwrap();

        assert_eq!(
            config,
            AppConfig {
                app_name: "test-app".into(),
                port: 3000,
                debug: false
            }
        );
    }

    #[test]
    fn parse_unsupported_format() {
        let result = parse_config("{}", "yaml");
        assert!(matches!(result, Err(ConfigError::UnsupportedFormat)));
    }

    // -------- Integration-Style Test --------

    #[test]
    fn load_config_from_file() {
        let content = r#"
            app_name = "file-app"
            port = 1234
            debug = true
        "#;

        let file_path = temp_file_path("config.toml");
        fs::write(&file_path, content).unwrap();

        let config = load_config(&file_path).unwrap();

        assert_eq!(
            config,
            AppConfig {
                app_name: "file-app".into(),
                port: 1234,
                debug: true
            }
        );

        fs::remove_file(file_path).unwrap();
    }

    // -------- Helpers --------

    fn temp_file_path(name: &str) -> PathBuf {
        let nanos = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();

        std::env::temp_dir().join(format!("{}_{}", nanos, name))
    }
}
