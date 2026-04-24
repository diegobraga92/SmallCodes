/**
 * TYPESCRIPT DECLARATION FILES (.d.ts)
 * ======================================
 * Type definitions for JavaScript libraries
 * Writing and using declaration files
 * DefinitelyTyped and @types packages
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT DECLARATION FILES");
console.log("=".repeat(80));

// ============================================================================
// 1. WHAT ARE DECLARATION FILES?
// ============================================================================

console.log("\n=== Declaration Files Overview ===");

/**
 * Declaration files (.d.ts):
 * - Provide type information for JavaScript code
 * - No runtime code, only type definitions
 * - Used for:
 *   1. Third-party JavaScript libraries
 *   2. Generated from TypeScript code
 *   3. Augmenting global scope
 * 
 * Example structure:
 * 
 * // math.d.ts
 * export function add(a: number, b: number): number;
 * export function multiply(a: number, b: number): number;
 * export const PI: number;
 */

console.log("Declaration files provide types without implementation");


// ============================================================================
// 2. BASIC DECLARATION FILE SYNTAX
// ============================================================================

console.log("\n=== Basic Declaration Syntax ===");

/**
 * Declaration file example (would be in .d.ts file):
 */

// Declare functions
declare function greet(name: string): string;
declare function calculate(a: number, b: number): number;

// Declare variables
declare const API_URL: string;
declare let debug: boolean;

// Declare classes
declare class Logger {
    constructor(name: string);
    log(message: string): void;
    error(message: string): void;
}

// Declare interfaces
interface Config {
    apiUrl: string;
    timeout: number;
}

// Declare types
type UserId = string | number;

// Declare enums
declare enum Status {
    Active,
    Inactive,
    Pending
}

console.log("Basic declaration syntax defined");


// ============================================================================
// 3. MODULE DECLARATIONS
// ============================================================================

console.log("\n=== Module Declarations ===");

/**
 * Declare types for external module:
 * 
 * // lodash.d.ts
 * declare module 'lodash' {
 *     export function chunk<T>(array: T[], size: number): T[][];
 *     export function debounce<T extends Function>(
 *         func: T,
 *         wait: number
 *     ): T;
 *     export function isEmpty(value: any): boolean;
 * }
 * 
 * Now you can use:
 * import { chunk, debounce } from 'lodash';
 */

// Wildcard module declarations
declare module "*.json" {
    const value: any;
    export default value;
}

declare module "*.css" {
    const styles: { [key: string]: string };
    export default styles;
}

declare module "*.svg" {
    const content: string;
    export default content;
}

declare module "*.png" {
    const path: string;
    export default path;
}

console.log("Module declarations for various file types");


// ============================================================================
// 4. GLOBAL DECLARATIONS
// ============================================================================

console.log("\n=== Global Declarations ===");

/**
 * Declare global variables/functions:
 * 
 * // globals.d.ts
 * declare global {
 *     var APP_VERSION: string;
 *     var DEBUG: boolean;
 *     
 *     interface Window {
 *         myCustomProperty: string;
 *         myCustomMethod(): void;
 *     }
 *     
 *     namespace NodeJS {
 *         interface ProcessEnv {
 *             NODE_ENV: 'development' | 'production' | 'test';
 *             API_KEY: string;
 *             DATABASE_URL: string;
 *         }
 *     }
 * }
 * 
 * export {};  // Make it a module
 */

// Augmenting global interfaces
declare global {
    interface String {
        capitalize(): string;
    }
    
    interface Array<T> {
        shuffle(): T[];
    }
}

// Must export to make it a module
export {};

// Now you can use globally:
// const str = "hello";
// str.capitalize();  // TypeScript knows this exists


// ============================================================================
// 5. NAMESPACE DECLARATIONS
// ============================================================================

console.log("\n=== Namespace Declarations ===");

/**
 * Declare types for global libraries:
 * 
 * // jquery.d.ts
 * declare namespace $ {
 *     function ajax(url: string, settings?: any): any;
 *     
 *     namespace fn {
 *         function extend(obj: any): any;
 *     }
 * }
 * 
 * declare function $(selector: string): any;
 * 
 * Now you can use:
 * $(".button").click();
 * $.ajax("/api/data");
 */

declare namespace MathLib {
    function add(a: number, b: number): number;
    function multiply(a: number, b: number): number;
    
    namespace Constants {
        const PI: number;
        const E: number;
    }
}

console.log("Namespace declarations for global libraries");


// ============================================================================
// 6. TRIPLE-SLASH DIRECTIVES
// ============================================================================

console.log("\n=== Triple-Slash Directives ===");

/**
 * Reference other declaration files:
 * 
 * /// <reference path="./types.d.ts" />
 * /// <reference types="node" />
 * /// <reference lib="es2015" />
 * 
 * Used at top of .d.ts files to include other definitions
 */

/// <reference lib="es2020" />
/// <reference lib="dom" />

console.log("Triple-slash directives for references");


// ============================================================================
// 7. DEFINITLYTYPED & @types
// ============================================================================

console.log("\n=== DefinitelyTyped (@types) ===");

/**
 * DefinitelyTyped = repository of type definitions
 * npm packages: @types/[library-name]
 * 
 * Installation:
 * npm install --save-dev @types/node
 * npm install --save-dev @types/express
 * npm install --save-dev @types/react
 * npm install --save-dev @types/lodash
 * 
 * TypeScript automatically includes types from node_modules/@types
 * 
 * Configure in tsconfig.json:
 * {
 *   "compilerOptions": {
 *     "typeRoots": ["./node_modules/@types"],
 *     "types": ["node", "jest"]  // Only include specific types
 *   }
 * }
 */

console.log("@types packages from DefinitelyTyped");


// ============================================================================
// 8. WRITING DECLARATION FILES FOR YOUR LIBRARY
// ============================================================================

console.log("\n=== Writing Declaration Files ===");

/**
 * Creating .d.ts for your library:
 * 
 * 1. MANUAL APPROACH
 *    Write .d.ts files manually alongside .js files
 * 
 *    src/
 *      math.js
 *      math.d.ts
 *    
 *    // math.js
 *    export function add(a, b) {
 *        return a + b;
 *    }
 *    
 *    // math.d.ts
 *    export function add(a: number, b: number): number;
 * 
 * 2. AUTO-GENERATION
 *    Use TypeScript compiler to generate .d.ts
 *    
 *    tsconfig.json:
 *    {
 *      "compilerOptions": {
 *        "declaration": true,        // Generate .d.ts files
 *        "declarationMap": true,     // Generate .d.ts.map for debugging
 *        "emitDeclarationOnly": false // Emit both .js and .d.ts
 *      }
 *    }
 * 
 * 3. PACKAGE.JSON CONFIGURATION
 *    {
 *      "name": "my-library",
 *      "version": "1.0.0",
 *      "main": "dist/index.js",
 *      "types": "dist/index.d.ts",   // or "typings"
 *      "files": ["dist"]
 *    }
 */

console.log("Generate .d.ts with declaration: true");


// ============================================================================
// 9. COMPLEX DECLARATION PATTERNS
// ============================================================================

console.log("\n=== Complex Declaration Patterns ===");

/**
 * Function overloads:
 */
declare function createElement(tag: "div"): HTMLDivElement;
declare function createElement(tag: "span"): HTMLSpanElement;
declare function createElement(tag: string): HTMLElement;

/**
 * Generic declarations:
 */
declare class Container<T> {
    add(item: T): void;
    get(index: number): T;
    items: T[];
}

/**
 * Callable interfaces:
 */
interface CallableObject {
    (param: string): number;  // Call signature
    property: string;         // Property
}

/**
 * Constructor signatures:
 */
declare class Database {
    constructor(connectionString: string);
    static getInstance(): Database;
}

/**
 * Index signatures:
 */
interface StringMap {
    [key: string]: string;
}

/**
 * Conditional types in declarations:
 */
type IsString<T> = T extends string ? true : false;
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

console.log("Complex declaration patterns");


// ============================================================================
// 10. MERGING DECLARATIONS
// ============================================================================

console.log("\n=== Declaration Merging ===");

/**
 * TypeScript can merge multiple declarations:
 * 
 * // file1.d.ts
 * interface User {
 *     name: string;
 * }
 * 
 * // file2.d.ts
 * interface User {
 *     email: string;
 * }
 * 
 * // Merged result:
 * interface User {
 *     name: string;
 *     email: string;
 * }
 * 
 * Works for:
 * - Interfaces
 * - Namespaces
 * - Classes (with namespaces)
 * 
 * Does NOT work for:
 * - Types (use intersection instead)
 */

// Interface merging example
interface Product {
    id: number;
    name: string;
}

interface Product {
    price: number;
    category: string;
}

// Merged: Product has id, name, price, category

console.log("Declaration merging for interfaces and namespaces");


// ============================================================================
// 11. AMBIENT MODULES
// ============================================================================

console.log("\n=== Ambient Modules ===");

/**
 * Ambient modules = declare module without implementation
 * 
 * // custom-lib.d.ts
 * declare module 'custom-lib' {
 *     export interface Options {
 *         debug?: boolean;
 *         timeout?: number;
 *     }
 *     
 *     export function init(options: Options): void;
 *     export function process(data: string): string;
 *     
 *     export default class CustomLib {
 *         constructor(options: Options);
 *         run(): void;
 *     }
 * }
 * 
 * Usage:
 * import CustomLib, { init, process } from 'custom-lib';
 */

declare module "my-untyped-library" {
    export function doSomething(value: string): number;
    export interface Config {
        apiKey: string;
    }
}

console.log("Ambient modules for untyped libraries");


// ============================================================================
// 12. BEST PRACTICES
// ============================================================================

/**
 * DECLARATION FILE BEST PRACTICES:
 * 
 * 1. USE AUTO-GENERATION WHEN POSSIBLE
 *    declaration: true in tsconfig.json
 * 
 * 2. KEEP DECLARATIONS CLOSE TO CODE
 *    .d.ts alongside .js files
 * 
 * 3. USE @types FOR POPULAR LIBRARIES
 *    Don't write manually if available
 * 
 * 4. DOCUMENT WITH JSDOC
 *    Add documentation comments
 *    /** @param name The user's name */
 * 
 * 5. BE PRECISE WITH TYPES
 *    Avoid 'any' in declarations
 *    Use specific types and unions
 * 
 * 6. USE GENERIC TYPES
 *    Make declarations reusable
 * 
 * 7. EXPORT EVERYTHING NEEDED
 *    All public API must be exported
 * 
 * 8. VERSION YOUR TYPES
 *    Keep .d.ts in sync with code version
 * 
 * 9. TEST YOUR DECLARATIONS
 *    Create test files that import and use types
 * 
 * 10. CONTRIBUTE TO DEFINITELYTYPED
 *     Help community by submitting types
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. .d.ts files provide types without implementation");
console.log("2. declare keyword for ambient declarations");
console.log("3. @types packages from DefinitelyTyped");
console.log("4. Auto-generate with declaration: true");
console.log("5. Module declarations for external libraries");
console.log("6. Global declarations with declare global");
console.log("7. Wildcard modules for non-JS files");
console.log("8. Declaration merging for interfaces");
console.log("9. Triple-slash directives for references");
console.log("10. Package types field points to .d.ts");
console.log("=".repeat(80));
