// ============================================
// GO PACKAGES & MODULES - COMPREHENSIVE GUIDE
// ============================================

// This example demonstrates Go packages and modules.
// To run: go mod init example && go mod tidy

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	// Standard library packages
	// Third-party packages (examples - would need actual modules)
	// "github.com/pkg/errors"
	// "golang.org/x/sync/errgroup"
	// Internal/local packages
)

// ============================================
// 1. GO MODULES (go.mod, go.sum)
// ============================================

/*
A Go module is a collection of Go packages with a go.mod file at its root.

go.mod file example (module descriptor):
-----------------------------------------
module github.com/username/repo

go 1.21

require (
    github.com/pkg/errors v0.9.1
    golang.org/x/sync v0.3.0
)

replace github.com/old/package => github.com/new/package v1.2.3

retract v1.0.0 // Published by mistake
-----------------------------------------

go.sum file (dependency integrity):
-----------------------------------------
Contains cryptographic checksums of dependencies
Auto-generated, should be committed to version control
Ensures reproducible builds
*/

func goModulesBasics() {
	fmt.Println("\n=== 1. Go Modules Basics ===")

	// Common go mod commands:
	// go mod init <module-path>    # Initialize new module
	// go mod tidy                  # Add missing, remove unused
	// go mod download              # Download dependencies
	// go mod vendor                # Create vendor directory
	// go mod verify                # Verify dependencies
	// go mod graph                 # Print dependency graph
	// go mod why <pkg>             # Explain why dependency exists

	fmt.Println("Module commands overview:")
	fmt.Println("  go mod init    - Create new module")
	fmt.Println("  go mod tidy    - Clean up dependencies")
	fmt.Println("  go mod vendor  - Vendor dependencies")
	fmt.Println("  go mod graph   - Show dependency graph")

	// Module-aware mode vs GOPATH mode
	// Since Go 1.16, module-aware mode is default
	// GO111MODULE environment variable controls behavior:
	//   auto (default) - enable if go.mod exists
	//   on             - always enable
	//   off            - disable (GOPATH mode)

	fmt.Printf("\nGO111MODULE (if set): %s\n", os.Getenv("GO111MODULE"))

	// Module paths should be globally unique
	// Convention: use repository location (github.com/user/repo)
	// or organization domain (company.com/team/project)

	// Module cache location
	cacheDir := os.Getenv("GOMODCACHE")
	if cacheDir == "" {
		cacheDir = filepath.Join(os.Getenv("GOPATH"), "pkg", "mod")
	}
	fmt.Printf("Module cache: %s\n", cacheDir)

	// Minimum version selection (MVS)
	// Go uses minimal version selection algorithm:
	// - Chooses minimum versions that satisfy all requirements
	// - Deterministic and reproducible
	// - Unlike other package managers that use "newest compatible"
}

// ============================================
// 2. SEMANTIC VERSIONING
// ============================================

/*
Semantic Versioning (SemVer): MAJOR.MINOR.PATCH
- MAJOR: Incompatible API changes
- MINOR: Backward-compatible functionality
- PATCH: Backward-compatible bug fixes

Examples:
- v1.0.0      # First stable release
- v1.2.3      # Major=1, Minor=2, Patch=3
- v2.0.0-beta # Pre-release version
- v0.1.0      # Development version (unstable)

Pseudo-versions:
- v0.0.0-20211030165408-4db5a4a819a8
  Format: v0.0.0-yyyymmddhhmmss-commitish
*/

func semanticVersioning() {
	fmt.Println("\n=== 2. Semantic Versioning ===")

	// Version prefixes in go.mod
	fmt.Println("Version patterns in require statements:")
	fmt.Println("  v1.2.3           - Exact version")
	fmt.Println("  v1.2             - Equivalent to v1.2.0")
	fmt.Println("  v1               - Equivalent to v1.0.0")
	fmt.Println("  v1.2.x           - Latest v1.2.x")
	fmt.Println("  v0.0.0-...       - Pseudo-version")
	fmt.Println("  commit-ish       - Branch/tag/commit")
	fmt.Println("  latest           - Latest tagged version")

	// Pre-release and build metadata
	fmt.Println("\nSpecial version suffixes:")
	fmt.Println("  -alpha, -beta, -rc  - Pre-release identifiers")
	fmt.Println("  +incompatible       - For v2+ modules without module path suffix")

	// Version comparison
	// Go uses SemVer 2.0.0 specification
	// Versions are compared component-wise: MAJOR > MINOR > PATCH

	// Go's approach to major versions:
	// For v2+ modules, module path must have /vN suffix
	// Example: module github.com/user/pkg/v2

	fmt.Println("\nMajor version upgrades in module paths:")
	fmt.Println("  v1: module github.com/user/pkg")
	fmt.Println("  v2: module github.com/user/pkg/v2")
	fmt.Println("  v3: module github.com/user/pkg/v3")

	// This allows multiple major versions to coexist
	// Example: import "github.com/user/pkg/v2"
}

// ============================================
// 3. REPLACING MODULES
// ============================================

/*
Replace directives allow substituting one module with another.
Useful for:
- Local development
- Testing patches
- Forked dependencies
*/

func replaceModules() {
	fmt.Println("\n=== 3. Replacing Modules ===")

	// Types of replace directives
	fmt.Println("Replace directive examples in go.mod:")
	fmt.Println()
	fmt.Println("1. Replace with local directory:")
	fmt.Println("   replace github.com/user/pkg => ../local/pkg")
	fmt.Println()
	fmt.Println("2. Replace with different repository:")
	fmt.Println("   replace github.com/old/pkg => github.com/new/pkg v1.2.3")
	fmt.Println()
	fmt.Println("3. Replace with specific version:")
	fmt.Println("   replace github.com/user/pkg => github.com/user/pkg v1.2.4")
	fmt.Println()
	fmt.Println("4. Replace with fork:")
	fmt.Println("   replace github.com/original/pkg => github.com/myfork/pkg v0.0.0-fork")

	// When to use replace:
	fmt.Println("\nCommon use cases for replace:")
	fmt.Println("  - Local development of dependencies")
	fmt.Println("  - Testing patches/fixes")
	fmt.Println("  - Working with private forks")
	fmt.Println("  - Pinning to specific commits")
	fmt.Println("  - Bypassing broken releases")

	// Local development workflow
	fmt.Println("\nTypical local development workflow:")
	fmt.Println("  1. Clone dependency locally")
	fmt.Println("  2. Add replace directive in go.mod")
	fmt.Println("  3. Make changes and test")
	fmt.Println("  4. Remove replace when done")
	fmt.Println("  5. Update go.mod with new version")

	// Important: replace directives only affect current module
	// They are not transitive to dependents

	// Using vendor directory as alternative
	fmt.Println("\nVendor directory alternative:")
	fmt.Println("  go mod vendor   # Copy dependencies to vendor/")
	fmt.Println("  go build -mod=vendor")

	// Replace with environment variable
	fmt.Println("\nGOFLAGS for development:")
	fmt.Println("  export GOFLAGS='-mod=readonly'    # Prevent automatic go.mod updates")
	fmt.Println("  export GOFLAGS='-mod=vendor'      # Always use vendor directory")
}

// ============================================
// 4. PRIVATE MODULES
// ============================================

func privateModules() {
	fmt.Println("\n=== 4. Private Modules ===")

	// Configuring Go for private repositories
	fmt.Println("Configuration for private modules:")
	fmt.Println()
	fmt.Println("1. Set GOPRIVATE environment variable:")
	fmt.Println("   export GOPRIVATE=*.corp.example.com,github.com/myorg/*")
	fmt.Println()
	fmt.Println("2. For authentication (Git):")
	fmt.Println("   git config --global url.\"git@github.com:\".insteadOf \"https://github.com/\"")
	fmt.Println()
	fmt.Println("3. For private Go modules proxy:")
	fmt.Println("   export GOPROXY=direct")
	fmt.Println("   export GONOSUMDB=*.corp.example.com")

	// GOPROXY configuration
	fmt.Println("\nGOPROXY configuration examples:")
	fmt.Println("  GOPROXY=https://proxy.golang.org,direct")
	fmt.Println("  GOPROXY=https://goproxy.io,direct")
	fmt.Println("  GOPROXY=company.corp.example.com")
	fmt.Println("  GOPROXY=off")

	// Private module proxy setup (Athens, Artifactory, etc.)
	fmt.Println("\nPrivate proxy setup:")
	fmt.Println("  1. Set up proxy server (Athens/Artifactory/Nexus)")
	fmt.Println("  2. Configure GOPROXY to use it")
	fmt.Println("  3. Set up authentication if needed")
	fmt.Println("  4. Configure GONOPROXY/GONOSUMDB")

	// GONOSUMDB for private modules
	fmt.Println("\nGONOSUMDB environment variable:")
	fmt.Println("  Prevents checksum database lookup for private modules")
	fmt.Println("  Example: export GONOSUMDB=*.corp.example.com")

	// SSH vs HTTPS for private repos
	fmt.Println("\nAuthentication methods:")
	fmt.Println("  SSH: git@github.com:user/repo.git")
	fmt.Println("  HTTPS with credentials in .netrc")
	fmt.Println("  HTTPS with Git credential helper")
	fmt.Println("  Personal Access Tokens (PATs)")

	// Example .netrc file
	fmt.Println("\nExample ~/.netrc file:")
	fmt.Println("  machine github.com")
	fmt.Println("  login username")
	fmt.Println("  password token_or_password")

	// CI/CD considerations
	fmt.Println("\nCI/CD configuration:")
	fmt.Println("  - Set up secrets for authentication")
	fmt.Println("  - Configure GOPRIVATE/GONOSUMDB")
	fmt.Println("  - Use vendor directory or module cache")
	fmt.Println("  - Consider using a private proxy")
}

// ============================================
// 5. DEPENDENCY MANAGEMENT BEST PRACTICES
// ============================================

func dependencyBestPractices() {
	fmt.Println("\n=== 5. Dependency Management Best Practices ===")

	// 1. Version Pinning
	fmt.Println("1. Version Pinning:")
	fmt.Println("   - Pin to exact versions (v1.2.3)")
	fmt.Println("   - Avoid wildcards (v1.2.x)")
	fmt.Println("   - Avoid 'latest'")
	fmt.Println("   - Update dependencies regularly")

	// 2. Dependency Updates
	fmt.Println("\n2. Dependency Updates:")
	fmt.Println("   Use: go get -u             # Update all")
	fmt.Println("   Use: go get -u ./...       # Update all in module")
	fmt.Println("   Use: go get package@latest # Update specific")
	fmt.Println("   Use: go get package@v1.2.3 # Update to version")

	fmt.Println("\n   Update strategies:")
	fmt.Println("   - Regular updates (weekly/monthly)")
	fmt.Println("   - Test updates before committing")
	fmt.Println("   - Use go mod tidy after updates")
	fmt.Println("   - Review changelogs for breaking changes")

	// 3. Security Scanning
	fmt.Println("\n3. Security Scanning:")
	fmt.Println("   Tools: govulncheck, trivy, snyk")
	fmt.Println("   Command: go install golang.org/x/vuln/cmd/govulncheck@latest")
	fmt.Println("   Command: govulncheck ./...")
	fmt.Println("   Regularly scan for vulnerabilities")

	// 4. Minimal Dependencies
	fmt.Println("\n4. Minimal Dependencies:")
	fmt.Println("   - Only add necessary dependencies")
	fmt.Println("   - Review transitive dependencies")
	fmt.Println("   - Consider standard library alternatives")
	fmt.Println("   - Avoid large frameworks for small tasks")

	// 5. Vendor Directory
	fmt.Println("\n5. Vendor Directory:")
	fmt.Println("   Pros: Reproducible builds, offline development")
	fmt.Println("   Cons: Larger repo, manual updates")
	fmt.Println("   Command: go mod vendor")
	fmt.Println("   Build with: go build -mod=vendor")

	// 6. Module Design
	fmt.Println("\n6. Module Design:")
	fmt.Println("   - Keep modules focused and small")
	fmt.Println("   - Use internal/ for private code")
	fmt.Println("   - Separate API and implementation")
	fmt.Println("   - Consider multi-module workspaces")

	// 7. Workspaces (Go 1.18+)
	fmt.Println("\n7. Workspaces (Go 1.18+):")
	fmt.Println("   go work init")
	fmt.Println("   go work use ./module1 ./module2")
	fmt.Println("   Useful for multi-module development")

	// 8. Testing Dependencies
	fmt.Println("\n8. Testing Dependencies:")
	fmt.Println("   Use go test ./... to test everything")
	fmt.Println("   Separate test dependencies if needed")
	fmt.Println("   Use //go:build integration for integration tests")
}

// ============================================
// 6. ADVANCED MODULE CONCEPTS
// ============================================

func advancedModuleConcepts() {
	fmt.Println("\n=== 6. Advanced Module Concepts ===")

	// 1. Module Graph
	fmt.Println("1. Module Graph:")
	fmt.Println("   Command: go mod graph")
	fmt.Println("   Shows dependency relationships")
	fmt.Println("   Useful for debugging dependency issues")

	// 2. Minimal Version Selection (MVS)
	fmt.Println("\n2. Minimal Version Selection:")
	fmt.Println("   Go chooses minimum satisfying versions")
	fmt.Println("   Different from npm/yarn's 'newest compatible'")
	fmt.Println("   Ensures reproducible builds")

	// 3. Retract Directive
	fmt.Println("\n3. Retract Directive:")
	fmt.Println("   Marks versions as broken/deprecated")
	fmt.Println("   Example: retract v1.0.0 // Buggy release")
	fmt.Println("   Warns users when using retracted versions")

	// 4. Exclude Directive
	fmt.Println("\n4. Exclude Directive:")
	fmt.Println("   Prevents specific versions from being used")
	fmt.Println("   Example: exclude github.com/user/pkg v1.2.3")
	fmt.Println("   Useful for blocking broken versions")

	// 5. Checksum Database (sum.golang.org)
	fmt.Println("\n5. Checksum Database:")
	fmt.Println("   Verifies module authenticity")
	fmt.Println("   Prevents supply-chain attacks")
	fmt.Println("   Can be disabled with GOSUMDB=off")

	// 6. Build Constraints and Tags
	fmt.Println("\n6. Build Constraints:")
	fmt.Println("   //go:build linux")
	fmt.Println("   // +build linux,amd64")
	fmt.Println("   Use for platform-specific dependencies")

	// 7. Module Proxies
	fmt.Println("\n7. Module Proxies:")
	fmt.Println("   Speed up downloads")
	fmt.Println("   Provide private module hosting")
	fmt.Println("   Cache modules for CI/CD")

	// 8. Go 1.16+ Defaults
	fmt.Println("\n8. Go 1.16+ Defaults:")
	fmt.Println("   - GO111MODULE=on by default")
	fmt.Println("   - go install with version suffix")
	fmt.Println("   - Vendor directory out of sync check")
}

// ============================================
// 7. PRACTICAL EXAMPLES
// ============================================

// Example module structure
/*
mymodule/
├── go.mod
├── go.sum
├── cmd/
│   ├── app/
│   │   └── main.go
│   └── cli/
│       └── main.go
├── internal/
│   ├── utils/
│   │   ├── math.go
│   │   └── strings.go
│   └── database/
│       └── client.go
├── pkg/
│   ├── api/
│   │   ├── client.go
│   │   └── types.go
│   └── config/
│       └── loader.go
├── vendor/          # Optional
├── tests/
│   └── integration/
└── examples/
    └── basic/
*/

// Example go.mod file
const exampleGoMod = `module example.com/mymodule

go 1.21

require (
    github.com/go-chi/chi/v5 v5.0.8
    github.com/joho/godotenv v1.5.1
    github.com/lib/pq v1.10.9
    github.com/stretchr/testify v1.8.4
)

require (
    github.com/davecgh/go-spew v1.1.1 // indirect
    github.com/pmezard/go-difflib v1.0.0 // indirect
    gopkg.in/yaml.v3 v3.0.1 // indirect
)

// For local development
// replace github.com/lib/pq => ../local-pq-fork

retract v1.0.0 // Published with critical bug

exclude github.com/lib/pq v1.10.0 // Broken version
`

func practicalExamples() {
	fmt.Println("\n=== 7. Practical Examples ===")

	// Creating a new module
	fmt.Println("Creating a new module:")
	fmt.Println("  1. mkdir myproject && cd myproject")
	fmt.Println("  2. go mod init github.com/username/myproject")
	fmt.Println("  3. Write your code")
	fmt.Println("  4. go mod tidy")
	fmt.Println("  5. go build")

	// Adding dependencies
	fmt.Println("\nAdding dependencies:")
	fmt.Println("  go get github.com/pkg/errors")
	fmt.Println("  go get golang.org/x/sync@latest")
	fmt.Println("  go get github.com/user/pkg@v1.2.3")

	// Updating dependencies
	fmt.Println("\nUpdating dependencies:")
	fmt.Println("  go get -u              # Update all")
	fmt.Println("  go get -u=patch        # Update patch versions only")
	fmt.Println("  go get github.com/user/pkg@v1.3.0")

	// Removing unused dependencies
	fmt.Println("\nCleaning up:")
	fmt.Println("  go mod tidy    # Remove unused, add missing")
	fmt.Println("  go mod verify  # Verify dependencies")
	fmt.Println("  go mod why -m all  # Show why each module is needed")

	// Working with vendor directory
	fmt.Println("\nVendor workflow:")
	fmt.Println("  go mod vendor          # Create vendor directory")
	fmt.Println("  go build -mod=vendor   # Build using vendor")
	fmt.Println("  rm -rf vendor && go mod vendor  # Update vendor")

	// Multi-module workspace
	fmt.Println("\nWorkspace workflow (Go 1.18+):")
	fmt.Println("  mkdir workspace && cd workspace")
	fmt.Println("  go work init")
	fmt.Println("  go work use ../module1 ../module2")
	fmt.Println("  go run ./module1/cmd/app")

	// Show example go.mod
	fmt.Println("\nExample go.mod file:")
	fmt.Println(exampleGoMod)
}

// ============================================
// MAIN DEMONSTRATION
// ============================================

func main() {
	fmt.Println("=== GO PACKAGES & MODULES COMPREHENSIVE GUIDE ===\n")

	// Run all demonstrations
	goModulesBasics()
	semanticVersioning()
	replaceModules()
	privateModules()
	dependencyBestPractices()
	advancedModuleConcepts()
	practicalExamples()

	fmt.Println("\n=== END OF DEMONSTRATION ===")

	// Additional practical tips
	fmt.Println("\nQuick Reference:")
	fmt.Println("  • Always commit go.mod and go.sum")
	fmt.Println("  • Use semantic versioning")
	fmt.Println("  • Run go mod tidy before commits")
	fmt.Println("  • Regularly update dependencies")
	fmt.Println("  • Use internal/ for private packages")
	fmt.Println("  • Consider vendor for reproducible builds")
	fmt.Println("  • Set up CI with dependency scanning")

	// Environment check
	fmt.Println("\nCurrent environment:")
	fmt.Printf("  Go version: %s\n", runtime.Version())

	if goPath := os.Getenv("GOPATH"); goPath != "" {
		fmt.Printf("  GOPATH: %s\n", goPath)
	}

	if goProxy := os.Getenv("GOPROXY"); goProxy != "" {
		fmt.Printf("  GOPROXY: %s\n", goProxy)
	}
}

// ============================================
// KEY TAKEAWAYS FOR DEVELOPERS
// ============================================

// JUNIOR DEVELOPERS:
// 1. Always initialize projects with `go mod init`
// 2. Commit both go.mod and go.sum to version control
// 3. Use `go mod tidy` regularly to keep dependencies clean
// 4. Add dependencies with `go get package@version`
// 5. Understand basic semantic versioning (MAJOR.MINOR.PATCH)

// MID-LEVEL DEVELOPERS:
// 1. Structure code properly (cmd/, pkg/, internal/)
// 2. Use replace directive for local development
// 3. Understand and configure GOPRIVATE for private repos
// 4. Regularly update dependencies with security scanning
// 5. Use vendor directory for reproducible builds when needed
// 6. Understand minimal version selection (MVS)

// SENIOR DEVELOPERS:
// 1. Design modular, reusable packages
// 2. Set up private module proxies for organizations
// 3. Implement dependency vulnerability scanning in CI/CD
// 4. Use workspaces for multi-module projects
// 5. Establish team-wide dependency management policies
// 6. Monitor and control transitive dependencies
// 7. Plan for major version upgrades (v2+ modules)

// TEAM LEADERS/ARCHITECTS:
// 1. Establish coding standards for module usage
// 2. Set up automated dependency update workflows
// 3. Implement security scanning in CI/CD pipeline
// 4. Create private module registry for proprietary code
// 5. Document dependency management processes
// 6. Plan for long-term dependency maintenance
// 7. Consider monorepo vs polyrepo module strategy

// SECURITY BEST PRACTICES:
// 1. Regularly run `govulncheck` on dependencies
// 2. Pin exact versions, not ranges
// 3. Review third-party code before adding
// 4. Use private proxies to cache and audit downloads
// 5. Keep Go version up to date for security fixes
// 6. Implement SBOM (Software Bill of Materials) generation

// PERFORMANCE OPTIMIZATIONS:
// 1. Use GOPROXY for faster downloads
// 2. Cache modules in CI/CD pipelines
// 3. Consider vendor directory for consistent builds
// 4. Minimize dependencies to reduce build times
// 5. Use build tags to exclude unused code

// TROUBLESHOOTING COMMON ISSUES:
// 1. Version conflicts: `go mod why -m package`
// 2. Authentication issues: Check .netrc, SSH keys
// 3. Proxy issues: Try `GOPROXY=direct`
// 4. Checksum mismatches: Delete go.sum and run `go mod tidy`
// 5. Old dependencies: `go get -u ./...`
