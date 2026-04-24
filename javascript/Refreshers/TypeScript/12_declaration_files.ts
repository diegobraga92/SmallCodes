/**
 * TYPESCRIPT DECLARATION FILES (.d.ts)
 * ======================================
 * Type definitions, ambient declarations, DefinitelyTyped
 * TODO: Complete with comprehensive examples
 */

// ============================================================================
// 1. AMBIENT DECLARATIONS
// ============================================================================

// Declare global variables
declare const API_KEY: string;

// Declare global functions
declare function globalFunction(param: string): void;

// ============================================================================
// 2. DECLARE MODULE
// ============================================================================

declare module "my-library" {
    export function doSomething(): void;
}

// ============================================================================
// 3. @TYPES PACKAGES
// ============================================================================

/**
 * Installing type definitions:
 * npm install --save-dev @types/node
 * npm install --save-dev @types/react
 * npm install --save-dev @types/express
 */

/**
 * KEY TAKEAWAYS:
 * 1. .d.ts files contain only type information
 * 2. Use declare keyword for ambient declarations
 * 3. @types/* packages from DefinitelyTyped
 * 4. Triple-slash directives for references
 */

export {};
