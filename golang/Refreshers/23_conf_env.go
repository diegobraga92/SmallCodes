/*
GOLANG CONFIGURATION & ENVIRONMENT MANAGEMENT
===============================================
Comprehensive examples covering concepts from junior to senior level.
Run with: go run main.go
*/

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/joho/godotenv" // For .env files
	"github.com/knadh/koanf/parsers/yaml"
	"github.com/knadh/koanf/providers/file"
	"github.com/knadh/koanf/v2" // Modern config management
	"github.com/spf13/viper"    // For config files
	"gopkg.in/yaml.v3"          // YAML parsing
)

// ============================================================================
// 1. ENVIRONMENT VARIABLES (Junior Level)
// ============================================================================
func demonstrateEnvVars() {
	fmt.Println("\n=== 1. ENVIRONMENT VARIABLES ===")

	// Basic environment variable access
	env := os.Getenv("APP_ENV")
	if env == "" {
		env = "development" // Default value
	}
	fmt.Printf("APP_ENV: %s\n", env)

	// Set environment variable (for this process and children)
	os.Setenv("CUSTOM_VAR", "my_value")

	// Get all environment variables
	fmt.Println("\nAll environment variables:")
	for _, env := range os.Environ() {
		if strings.HasPrefix(env, "APP_") {
			fmt.Println("  ", env)
		}
	}

	// Expanded environment variables with defaults
	port := getEnvAsInt("PORT", 8080)
	timeout := getEnvAsDuration("TIMEOUT", "30s")
	fmt.Printf("Port: %d, Timeout: %v\n", port, timeout)
}

// Helper function with default values
func getEnvAsInt(key string, defaultVal int) int {
	if val := os.Getenv(key); val != "" {
		if i, err := strconv.Atoi(val); err == nil {
			return i
		}
	}
	return defaultVal
}

func getEnvAsDuration(key, defaultVal string) time.Duration {
	if val := os.Getenv(key); val != "" {
		if d, err := time.ParseDuration(val); err == nil {
			return d
		}
	}
	if d, err := time.ParseDuration(defaultVal); err == nil {
		return d
	}
	return 30 * time.Second
}

// ============================================================================
// 2. CONFIG FILES (Mid-Level)
// ============================================================================
type AppConfig struct {
	Server   ServerConfig   `yaml:"server" json:"server"`
	Database DatabaseConfig `yaml:"database" json:"database"`
	Features FeatureFlags   `yaml:"features" json:"features"`
}

type ServerConfig struct {
	Port    int           `yaml:"port" json:"port"`
	Timeout time.Duration `yaml:"timeout" json:"timeout"`
	Host    string        `yaml:"host" json:"host"`
}

type DatabaseConfig struct {
	Host     string `yaml:"host" json:"host"`
	Port     int    `yaml:"port" json:"port"`
	Name     string `yaml:"name" json:"name"`
	Username string `yaml:"username" json:"username"`
	SSLMode  string `yaml:"ssl_mode" json:"ssl_mode"`
}

type FeatureFlags struct {
	EnableCache    bool `yaml:"enable_cache" json:"enable_cache"`
	EnableMetrics  bool `yaml:"enable_metrics" json:"enable_metrics"`
	BetaFeatures   bool `yaml:"beta_features" json:"beta_features"`
	MaxConnections int  `yaml:"max_connections" json:"max_connections"`
}

func demonstrateConfigFiles() {
	fmt.Println("\n=== 2. CONFIG FILES ===")

	// Example 1: Manual YAML parsing
	configYAML := `
server:
  port: 8080
  timeout: 60s
  host: localhost
database:
  host: db.example.com
  port: 5432
  name: myapp
  username: admin
  ssl_mode: require
features:
  enable_cache: true
  enable_metrics: false
  beta_features: true
  max_connections: 100
`

	var config AppConfig
	if err := yaml.Unmarshal([]byte(configYAML), &config); err != nil {
		log.Printf("Error parsing YAML: %v", err)
	} else {
		fmt.Printf("Parsed config: Server Port: %d, DB Host: %s\n",
			config.Server.Port, config.Database.Host)
	}

	// Example 2: Using godotenv for .env files
	if err := godotenv.Load(".env"); err != nil {
		fmt.Println("Note: No .env file found, using system environment")
	}

	// Example 3: Using Viper (popular config library)
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")
	viper.AddConfigPath("./config")
	viper.AddConfigPath("/etc/myapp/")

	// Set defaults
	viper.SetDefault("server.port", 8080)
	viper.SetDefault("server.timeout", "30s")
	viper.SetDefault("features.enable_cache", true)

	// Read config
	if err := viper.ReadInConfig(); err == nil {
		fmt.Printf("Config file used: %s\n", viper.ConfigFileUsed())
		port := viper.GetInt("server.port")
		timeout := viper.GetDuration("server.timeout")
		fmt.Printf("Viper config - Port: %d, Timeout: %v\n", port, timeout)
	}

	// Example 4: Using Koanf (modern config library)
	k := koanf.New(".")

	// Load YAML config
	if err := k.Load(file.Provider("config.yaml"), yaml.Parser()); err == nil {
		port := k.Int("server.port")
		host := k.String("server.host")
		fmt.Printf("Koanf config - Host: %s, Port: %d\n", host, port)

		// Get nested config
		var dbConfig DatabaseConfig
		if err := k.Unmarshal("database", &dbConfig); err == nil {
			fmt.Printf("Database config: %+v\n", dbConfig)
		}
	}
}

// ============================================================================
// 3. SECRETS MANAGEMENT (Senior Level)
// ============================================================================
// Interface for secrets manager (abstraction for different providers)
type SecretsManager interface {
	GetSecret(key string) (string, error)
	SetSecret(key, value string) error
	ListSecrets() ([]string, error)
}

// Environment-based secrets (for development)
type EnvSecretsManager struct{}

func (e *EnvSecretsManager) GetSecret(key string) (string, error) {
	// In production, this might come from AWS Secrets Manager, HashiCorp Vault, etc.
	val := os.Getenv(key)
	if val == "" {
		return "", fmt.Errorf("secret %s not found", key)
	}
	return val, nil
}

func (e *EnvSecretsManager) SetSecret(key, value string) error {
	return os.Setenv(key, value)
}

func (e *EnvSecretsManager) ListSecrets() ([]string, error) {
	// Return all environment variables with "SECRET_" prefix
	var secrets []string
	for _, env := range os.Environ() {
		if strings.HasPrefix(env, "SECRET_") || strings.HasPrefix(env, "DB_PASSWORD") {
			secrets = append(secrets, strings.Split(env, "=")[0])
		}
	}
	return secrets, nil
}

// Mock AWS Secrets Manager implementation
type AWSSecretsManager struct {
	region string
}

func (a *AWSSecretsManager) GetSecret(key string) (string, error) {
	// Mock implementation - in real code, use AWS SDK
	fmt.Printf("[AWS Secrets Manager] Fetching secret: %s from region: %s\n", key, a.region)
	return "mock-secret-value-from-aws", nil
}

func (a *AWSSecretsManager) SetSecret(key, value string) error {
	fmt.Printf("[AWS Secrets Manager] Setting secret: %s\n", key)
	return nil
}

func (a *AWSSecretsManager) ListSecrets() ([]string, error) {
	return []string{"api-key", "db-password", "jwt-secret"}, nil
}

func demonstrateSecretsManagement() {
	fmt.Println("\n=== 3. SECRETS MANAGEMENT ===")

	// Strategy pattern for secrets management
	var manager SecretsManager

	// Choose implementation based on environment
	if os.Getenv("APP_ENV") == "production" {
		manager = &AWSSecretsManager{region: "us-east-1"}
	} else {
		manager = &EnvSecretsManager{}
		// Set some test secrets
		os.Setenv("DB_PASSWORD", "dev-password-123")
		os.Setenv("API_KEY", "test-api-key")
	}

	// Use the secrets manager
	if secret, err := manager.GetSecret("DB_PASSWORD"); err == nil {
		fmt.Printf("Retrieved DB password: %s...\n", secret[:3]+"***")
	}

	if secrets, err := manager.ListSecrets(); err == nil {
		fmt.Printf("Available secrets: %v\n", secrets)
	}
}

// ============================================================================
// 4. FEATURE FLAGS (Mid to Senior Level)
// ============================================================================
type FeatureFlagManager struct {
	flags      map[string]bool
	percentage map[string]int // For percentage-based rollouts
	configFile string
	lastReload time.Time
}

func NewFeatureFlagManager(configFile string) *FeatureFlagManager {
	ffm := &FeatureFlagManager{
		flags:      make(map[string]bool),
		percentage: make(map[string]int),
		configFile: configFile,
	}
	ffm.loadConfig()

	// Auto-reload config every 30 seconds
	go ffm.autoReload(30 * time.Second)

	return ffm
}

func (f *FeatureFlagManager) loadConfig() {
	// Load from file, database, or feature flag service (LaunchDarkly, etc.)
	// For simplicity, using a JSON file
	data, err := os.ReadFile(f.configFile)
	if err != nil {
		// Default flags
		f.flags = map[string]bool{
			"new_checkout":     false,
			"dark_mode":        true,
			"experimental_api": false,
		}
		f.percentage = map[string]int{
			"beta_features": 10, // 10% of users
		}
		return
	}

	var config struct {
		Flags      map[string]bool `json:"flags"`
		Percentage map[string]int  `json:"percentage"`
	}

	if err := json.Unmarshal(data, &config); err == nil {
		f.flags = config.Flags
		f.percentage = config.Percentage
	}
	f.lastReload = time.Now()
}

func (f *FeatureFlagManager) autoReload(interval time.Duration) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for range ticker.C {
		f.loadConfig()
		fmt.Println("[Feature Flags] Config reloaded")
	}
}

func (f *FeatureFlagManager) IsEnabled(flag string) bool {
	return f.flags[flag]
}

func (f *FeatureFlagManager) IsEnabledForUser(flag, userId string) bool {
	if !f.flags[flag] {
		return false
	}

	// Percentage-based rollout
	if percent, ok := f.percentage[flag]; ok {
		// Simple hash-based percentage calculation
		hash := simpleHash(userId)
		return hash%100 < percent
	}

	return true
}

func simpleHash(s string) int {
	h := 0
	for _, c := range s {
		h = 31*h + int(c)
	}
	return h % 100
}

func (f *FeatureFlagManager) SetFlag(flag string, enabled bool) {
	f.flags[flag] = enabled
}

func demonstrateFeatureFlags() {
	fmt.Println("\n=== 4. FEATURE FLAGS ===")

	ffm := NewFeatureFlagManager("feature-flags.json")

	// Check feature flags
	fmt.Printf("New checkout enabled: %v\n", ffm.IsEnabled("new_checkout"))
	fmt.Printf("Dark mode enabled: %v\n", ffm.IsEnabled("dark_mode"))

	// Percentage-based rollout
	userId := "user-12345"
	enabled := ffm.IsEnabledForUser("beta_features", userId)
	fmt.Printf("Beta features enabled for user %s: %v\n", userId, enabled)

	// Dynamically toggle flags
	ffm.SetFlag("new_checkout", true)
	fmt.Printf("New checkout after toggle: %v\n", ffm.IsEnabled("new_checkout"))
}

// ============================================================================
// 5. 12-FACTOR APP PRINCIPLES IMPLEMENTATION
// ============================================================================
type TwelveFactorApp struct {
	config   *AppConfig
	secrets  SecretsManager
	features *FeatureFlagManager
}

func NewTwelveFactorApp() *TwelveFactorApp {
	// I. Codebase - One codebase tracked in revision control
	// II. Dependencies - Explicitly declared (go.mod)
	// III. Config - Store config in environment
	env := os.Getenv("APP_ENV")
	if env == "" {
		env = "development"
	}

	// IV. Backing services - Treat as attached resources
	dbUrl := os.Getenv("DATABASE_URL")
	if dbUrl == "" {
		dbUrl = "postgres://localhost:5432/mydb"
	}

	// V. Build, release, run - Strict separation
	// VI. Processes - Execute as stateless processes

	app := &TwelveFactorApp{
		secrets:  &EnvSecretsManager{},
		features: NewFeatureFlagManager("features.json"),
	}

	// VII. Port binding - Export via port
	port := getEnvAsInt("PORT", 8080)

	// VIII. Concurrency - Scale out via process model
	// IX. Disposability - Fast startup and graceful shutdown
	// X. Dev/prod parity - Keep environments similar
	// XI. Logs - Treat as event streams
	// XII. Admin processes - Run as one-off processes

	app.config = &AppConfig{
		Server: ServerConfig{
			Port:    port,
			Host:    os.Getenv("HOST"),
			Timeout: getEnvAsDuration("TIMEOUT", "30s"),
		},
		Database: DatabaseConfig{
			Host:    parseDBHost(dbUrl),
			SSLMode: getEnvAsString("DB_SSL_MODE", "require"),
		},
	}

	return app
}

func parseDBHost(url string) string {
	// Simplified URL parsing
	if strings.Contains(url, "://") {
		parts := strings.Split(url, "://")
		if len(parts) > 1 {
			return strings.Split(parts[1], "/")[0]
		}
	}
	return url
}

func getEnvAsString(key, defaultVal string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return defaultVal
}

func (app *TwelveFactorApp) Start() {
	fmt.Println("\n=== 5. 12-FACTOR APP DEMONSTRATION ===")
	fmt.Printf("Starting app on port: %d\n", app.config.Server.Port)
	fmt.Printf("Environment: %s\n", os.Getenv("APP_ENV"))
	fmt.Printf("Database host: %s\n", app.config.Database.Host)

	// Get secret
	if secret, err := app.secrets.GetSecret("API_KEY"); err == nil {
		fmt.Printf("API Key loaded: %s...\n", secret[:3]+"***")
	}

	// Check feature flags
	if app.features.IsEnabled("new_checkout") {
		fmt.Println("New checkout flow is ACTIVE")
	}

	// Log to stdout (principle XI)
	log.Println("Application started successfully")

	// Demonstrate graceful shutdown handling
	setupGracefulShutdown()
}

func setupGracefulShutdown() {
	// This would typically handle SIGTERM/SIGINT signals
	fmt.Println("App is ready for graceful shutdown handling")
}

func demonstrateTwelveFactor() {
	// Set up environment for demonstration
	os.Setenv("APP_ENV", "staging")
	os.Setenv("PORT", "9090")
	os.Setenv("DATABASE_URL", "postgres://user:pass@prod-db.example.com:5432/mydb")
	os.Setenv("API_KEY", "prod-api-key-abcdef123456")

	app := NewTwelveFactorApp()
	app.Start()
}

// ============================================================================
// MAIN FUNCTION - RUN ALL DEMONSTRATIONS
// ============================================================================
func main() {
	fmt.Println("GOLANG CONFIGURATION & ENVIRONMENT MANAGEMENT DEMO")
	fmt.Println("=====================================================")

	// Run all demonstrations
	demonstrateEnvVars()
	demonstrateConfigFiles()
	demonstrateSecretsManagement()
	demonstrateFeatureFlags()
	demonstrateTwelveFactor()

	fmt.Println("\n=== SUMMARY ===")
	fmt.Println("1. Environment Variables: Direct OS access with defaults")
	fmt.Println("2. Config Files: Structured config with YAML/JSON support")
	fmt.Println("3. Secrets: Abstracted secret management with multiple backends")
	fmt.Println("4. Feature Flags: Dynamic feature control with rollouts")
	fmt.Println("5. 12-Factor App: Cloud-native application principles")

	// Clean up
	os.Unsetenv("CUSTOM_VAR")
}

/*
INSTRUCTIONS TO RUN:
====================
1. Install dependencies:
   go get github.com/joho/godotenv
   go get github.com/spf13/viper
   go get github.com/knadh/koanf/v2
   go get gopkg.in/yaml.v3

2. Create a config.yaml file:
   server:
     port: 8080
     host: localhost
   database:
     host: localhost
     port: 5432

3. Create a .env file (optional):
   APP_ENV=development
   DB_PASSWORD=secret123

4. Run:
   go run main.go

KEY TAKEAWAYS:
==============
- Always use environment variables for config in production
- Use structs for type-safe configuration
- Abstract secrets management for different environments
- Implement feature flags for controlled rollouts
- Follow 12-factor principles for cloud-native apps
- Use established libraries (Viper, Koanf) for complex config needs
*/
