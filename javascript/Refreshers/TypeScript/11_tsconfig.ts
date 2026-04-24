/**
 * TYPESCRIPT CONFIGURATION (tsconfig.json)
 * ==========================================
 * Understanding and configuring TypeScript compiler options
 * Best practices for different project types
 * 
 * Note: This is a .ts file for demonstration purposes
 * Actual tsconfig.json is a JSON file
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT CONFIGURATION (tsconfig.json)");
console.log("=".repeat(80));

// ============================================================================
// 1. BASIC STRUCTURE
// ============================================================================

console.log("\n=== Basic tsconfig.json Structure ===");

/**
 * Minimal tsconfig.json:
 * 
 * {
 *   "compilerOptions": {
 *     "target": "ES2020",
 *     "module": "commonjs",
 *     "outDir": "./dist",
 *     "rootDir": "./src",
 *     "strict": true
 *   },
 *   "include": ["src/**/*"],
 *   "exclude": ["node_modules", "dist"]
 * }
 */

const basicConfig = {
    description: "Basic TypeScript configuration",
    options: {
        target: "ES2020",           // JavaScript version to compile to
        module: "commonjs",         // Module system (commonjs, esnext, etc.)
        outDir: "./dist",           // Output directory
        rootDir: "./src",           // Input directory
        strict: true                // Enable all strict type checking
    }
};

console.log(JSON.stringify(basicConfig, null, 2));


// ============================================================================
// 2. COMPILER OPTIONS - TYPE CHECKING
// ============================================================================

console.log("\n=== Type Checking Options ===");

/**
 * Type checking compiler options:
 */

const typeCheckingOptions = {
    // STRICT MODE (enable all strict checks)
    "strict": true,                          // Enable all strict options below
    
    // Individual strict options (when strict: true)
    "noImplicitAny": true,                   // Error on implicit 'any'
    "strictNullChecks": true,                // null and undefined are distinct types
    "strictFunctionTypes": true,             // Strict function type checking
    "strictBindCallApply": true,             // Strict bind/call/apply checking
    "strictPropertyInitialization": true,    // Class properties must be initialized
    "noImplicitThis": true,                  // Error on implicit 'this'
    "alwaysStrict": true,                    // Parse in strict mode, emit 'use strict'
    
    // Additional type checks
    "noUnusedLocals": true,                  // Error on unused local variables
    "noUnusedParameters": true,              // Error on unused parameters
    "noImplicitReturns": true,               // Error if not all code paths return
    "noFallthroughCasesInSwitch": true,     // Error on switch fallthrough
    "noUncheckedIndexedAccess": true,        // Add undefined to index signatures
    "noImplicitOverride": true,              // Require 'override' keyword
    "noPropertyAccessFromIndexSignature": true, // Require bracket notation for indexed access
    "allowUnusedLabels": false,              // Error on unused labels
    "allowUnreachableCode": false            // Error on unreachable code
};

console.log("Type checking options:", Object.keys(typeCheckingOptions).length, "options");


// ============================================================================
// 3. COMPILER OPTIONS - MODULES
// ============================================================================

console.log("\n=== Module Options ===");

/**
 * Module-related compiler options:
 */

const moduleOptions = {
    "module": "esnext",                      // Module system: commonjs, amd, esnext, etc.
    "moduleResolution": "node",              // How modules are resolved: node, classic
    "baseUrl": ".",                          // Base directory for non-relative imports
    "paths": {                                // Path mapping (relative to baseUrl)
        "@app/*": ["src/app/*"],
        "@components/*": ["src/components/*"],
        "@utils/*": ["src/utils/*"]
    },
    "rootDirs": ["src", "generated"],        // Multiple root directories
    "typeRoots": ["./node_modules/@types"],  // Folders to include type definitions from
    "types": ["node", "jest"],               // Type packages to include
    "allowSyntheticDefaultImports": true,    // Allow default imports from modules without default export
    "esModuleInterop": true,                 // Enable interop between CommonJS and ES modules
    "resolveJsonModule": true,               // Allow importing .json files
    "isolatedModules": true                  // Each file is a separate module (for Babel, etc.)
};

console.log("Module options:", Object.keys(moduleOptions).length, "options");


// ============================================================================
// 4. COMPILER OPTIONS - EMIT
// ============================================================================

console.log("\n=== Emit Options ===");

/**
 * Code generation / output options:
 */

const emitOptions = {
    "target": "ES2020",                      // JavaScript version: ES3, ES5, ES2015, ES2020, ESNext
    "lib": ["ES2020", "DOM"],                // Library files to include
    "outDir": "./dist",                      // Output directory
    "rootDir": "./src",                      // Input root directory
    "outFile": "./bundle.js",                // Single output file (for AMD/System)
    "removeComments": true,                  // Remove comments from output
    "noEmit": false,                         // Don't emit output (type checking only)
    "importHelpers": true,                   // Import helpers from tslib
    "downlevelIteration": true,              // Emit more compliant but verbose iteration code
    "sourceMap": true,                       // Generate .map files
    "inlineSourceMap": false,                // Inline source map in JS file
    "declarationMap": true,                  // Generate .d.ts.map files
    "declaration": true,                     // Generate .d.ts files
    "emitDeclarationOnly": false,            // Only emit .d.ts files
    "preserveConstEnums": true,              // Don't inline const enum values
    "newLine": "lf"                          // Line ending: crlf or lf
};

console.log("Emit options:", Object.keys(emitOptions).length, "options");


// ============================================================================
// 5. COMPILER OPTIONS - INTEROP & SUPPORT
// ============================================================================

console.log("\n=== Interop & Support Options ===");

const interopOptions = {
    "allowJs": true,                         // Allow JavaScript files
    "checkJs": false,                        // Type check JavaScript files
    "jsx": "react",                          // JSX mode: preserve, react, react-native, react-jsx
    "jsxFactory": "React.createElement",     // JSX factory function
    "jsxFragmentFactory": "React.Fragment",  // JSX fragment factory
    "jsxImportSource": "react",              // Module for JSX factory (react-jsx)
    "experimentalDecorators": true,          // Enable decorators
    "emitDecoratorMetadata": true,           // Emit metadata for decorators
    "allowSyntheticDefaultImports": true,    // Allow default imports
    "esModuleInterop": true,                 // ES module interop
    "forceConsistentCasingInFileNames": true, // Ensure consistent casing
    "skipLibCheck": true                     // Skip type checking of .d.ts files
};

console.log("Interop options:", Object.keys(interopOptions).length, "options");


// ============================================================================
// 6. PROJECT REFERENCES
// ============================================================================

console.log("\n=== Project References ===");

/**
 * Project references for monorepos:
 * 
 * tsconfig.json:
 * {
 *   "references": [
 *     { "path": "./packages/core" },
 *     { "path": "./packages/utils" }
 *   ]
 * }
 * 
 * packages/core/tsconfig.json:
 * {
 *   "compilerOptions": {
 *     "composite": true,
 *     "declaration": true,
 *     "outDir": "./dist"
 *   }
 * }
 */

const projectReferences = {
    concept: "Split large project into smaller pieces",
    benefits: [
        "Faster builds (only rebuild changed projects)",
        "Better IDE performance",
        "Enforced logical separation"
    ],
    requirements: {
        "composite": true,
        "declaration": true
    }
};

console.log("Project references:", projectReferences.benefits.join(", "));


// ============================================================================
// 7. INCLUDE/EXCLUDE PATTERNS
// ============================================================================

console.log("\n=== Include/Exclude Patterns ===");

const includeExclude = {
    "include": [
        "src/**/*"               // All files in src directory
    ],
    "exclude": [
        "node_modules",          // Dependencies
        "**/*.spec.ts",          // Test files
        "dist",                  // Output directory
        "build"                  // Build artifacts
    ],
    "files": [
        "src/index.ts",          // Specific files to include
        "src/globals.d.ts"
    ]
};

console.log("Include/exclude patterns defined");


// ============================================================================
// 8. CONFIGURATION EXAMPLES
// ============================================================================

console.log("\n=== Configuration Examples ===");

// Node.js backend project
const nodeConfig = {
    name: "Node.js Backend",
    config: {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "lib": ["ES2020"],
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": true,
            "esModuleInterop": true,
            "skipLibCheck": true,
            "forceConsistentCasingInFileNames": true,
            "resolveJsonModule": true,
            "declaration": true,
            "sourceMap": true
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist"]
    }
};

// React frontend project
const reactConfig = {
    name: "React Frontend",
    config: {
        "compilerOptions": {
            "target": "ES2020",
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "module": "esnext",
            "moduleResolution": "node",
            "jsx": "react-jsx",
            "outDir": "./build",
            "rootDir": "./src",
            "strict": true,
            "esModuleInterop": true,
            "skipLibCheck": true,
            "forceConsistentCasingInFileNames": true,
            "resolveJsonModule": true,
            "isolatedModules": true,
            "allowSyntheticDefaultImports": true,
            "noEmit": true,  // Bundler handles emit
            "baseUrl": "src",
            "paths": {
                "@components/*": ["components/*"],
                "@utils/*": ["utils/*"]
            }
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules"]
    }
};

// Library project
const libraryConfig = {
    name: "TypeScript Library",
    config: {
        "compilerOptions": {
            "target": "ES2015",
            "module": "esnext",
            "lib": ["ES2020"],
            "declaration": true,
            "declarationMap": true,
            "outDir": "./dist",
            "rootDir": "./src",
            "strict": true,
            "esModuleInterop": true,
            "skipLibCheck": true,
            "forceConsistentCasingInFileNames": true
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist", "**/*.test.ts"]
    }
};

console.log("Config examples:", nodeConfig.name, reactConfig.name, libraryConfig.name);


// ============================================================================
// 9. EXTENDS & BASE CONFIGS
// ============================================================================

console.log("\n=== Extending Configurations ===");

/**
 * Share common config across projects:
 * 
 * tsconfig.base.json:
 * {
 *   "compilerOptions": {
 *     "strict": true,
 *     "esModuleInterop": true,
 *     "skipLibCheck": true,
 *     "forceConsistentCasingInFileNames": true
 *   }
 * }
 * 
 * tsconfig.json:
 * {
 *   "extends": "./tsconfig.base.json",
 *   "compilerOptions": {
 *     "target": "ES2020",
 *     "outDir": "./dist"
 *   }
 * }
 * 
 * Popular base configs:
 * - @tsconfig/node16
 * - @tsconfig/react-native
 * - @tsconfig/recommended
 * 
 * npm install --save-dev @tsconfig/node16
 * 
 * {
 *   "extends": "@tsconfig/node16/tsconfig.json"
 * }
 */

console.log("Extend base configs for consistency");


// ============================================================================
// 10. WATCH OPTIONS
// ============================================================================

console.log("\n=== Watch Options ===");

const watchOptions = {
    "watchOptions": {
        "watchFile": "useFsEvents",          // Use file system events
        "watchDirectory": "useFsEvents",     // Use file system events for directories
        "fallbackPolling": "dynamicPriority", // Fallback when events unavailable
        "synchronousWatchDirectory": true,   // Synchronous directory watching
        "excludeDirectories": ["**/node_modules", "_build"], // Directories to exclude
        "excludeFiles": ["build/fileWhichChangesOften.ts"]  // Files to exclude
    }
};

console.log("Watch options for tsc --watch");


// ============================================================================
// 11. BEST PRACTICES
// ============================================================================

/**
 * TSCONFIG BEST PRACTICES:
 * 
 * 1. ALWAYS USE STRICT MODE
 *    "strict": true
 * 
 * 2. ENABLE ADDITIONAL CHECKS
 *    noUnusedLocals, noUnusedParameters, noImplicitReturns
 * 
 * 3. USE PATH MAPPING
 *    Avoid ../../../ imports
 * 
 * 4. SKIP LIB CHECK IN PRODUCTION
 *    "skipLibCheck": true
 *    Faster compilation
 * 
 * 5. ENABLE SOURCE MAPS
 *    "sourceMap": true
 *    Better debugging
 * 
 * 6. SEPARATE DEV/PROD CONFIGS
 *    tsconfig.json
 *    tsconfig.prod.json
 * 
 * 7. USE PROJECT REFERENCES FOR MONOREPOS
 *    Faster builds, better organization
 * 
 * 8. CONSISTENT CASING
 *    "forceConsistentCasingInFileNames": true
 * 
 * 9. EXCLUDE UNNECESSARY FILES
 *    node_modules, dist, build
 * 
 * 10. USE EXTENDS FOR SHARED CONFIG
 *     DRY principle for multiple projects
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. tsconfig.json configures TypeScript compiler");
console.log("2. strict: true enables all strict type checks");
console.log("3. Module options: module, moduleResolution, paths");
console.log("4. Emit options: target, outDir, sourceMap");
console.log("5. include/exclude control which files to compile");
console.log("6. Project references for monorepos");
console.log("7. extends for shared configuration");
console.log("8. Different configs for different project types");
console.log("9. Watch options for development");
console.log("10. Always enable strict mode and source maps");
console.log("=".repeat(80));

export {};
