/**
 * TYPESCRIPT MODULES
 * ===================
 * ES6 modules, namespaces, module resolution, ambient modules
 * Import/export syntax, module formats
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT MODULES");
console.log("=".repeat(80));

// ============================================================================
// 1. ES6 MODULE BASICS
// ============================================================================

console.log("\n=== ES6 Modules ===");

/**
 * ES6 modules in TypeScript work same as JavaScript
 * export = share code
 * import = use code from other modules
 */

// Named exports
export const PI = 3.14159;
export const E = 2.71828;

export function add(a: number, b: number): number {
    return a + b;
}

export function multiply(a: number, b: number): number {
    return a * b;
}

export class Calculator {
    constructor(public value: number = 0) {}
    
    add(n: number): this {
        this.value += n;
        return this;
    }
}

// Export interface
export interface User {
    id: number;
    name: string;
    email: string;
}

// Export type
export type UserId = number | string;

console.log("Module exports defined");


// ============================================================================
// 2. DEFAULT EXPORTS
// ============================================================================

console.log("\n=== Default Exports ===");

/**
 * Default export = one main export per module
 * Import without braces
 */

// In a separate file (example):
// export default class Database {
//     connect() {}
// }
// import Database from './database';

// Or with named exports:
// export { Database as default };

export default class Logger {
    log(message: string): void {
        console.log(`  [LOG] ${message}`);
    }
}


// ============================================================================
// 3. IMPORT SYNTAX
// ============================================================================

console.log("\n=== Import Syntax ===");

/**
 * Various import patterns:
 */

// Named imports
// import { add, multiply } from './math';
// import { User, UserId } from './types';

// Rename imports
// import { add as sum } from './math';

// Import everything as namespace
// import * as math from './math';

// Import default
// import Logger from './logger';

// Import default + named
// import Logger, { PI, E } from './logger';

// Import for side effects only
// import './setup';

// Dynamic import
// const module = await import('./module');

console.log("Various import syntaxes available");


// ============================================================================
// 4. RE-EXPORTING
// ============================================================================

console.log("\n=== Re-exporting ===");

/**
 * Re-export = export something imported from another module
 * Useful for creating index files
 */

// Re-export everything
// export * from './math';

// Re-export specific exports
// export { add, multiply } from './math';

// Re-export with rename
// export { add as sum } from './math';

// Re-export default as named
// export { default as Logger } from './logger';

// Example index.ts:
// export * from './user';
// export * from './product';
// export * from './order';
// Now consumers can: import { User, Product, Order } from './models';

console.log("Re-exporting patterns");


// ============================================================================
// 5. NAMESPACES (INTERNAL MODULES)
// ============================================================================

console.log("\n=== Namespaces ===");

/**
 * Namespaces = older TypeScript feature for organizing code
 * Less common now with ES6 modules
 */

namespace Geometry {
    export interface Point {
        x: number;
        y: number;
    }
    
    export class Circle {
        constructor(public center: Point, public radius: number) {}
        
        area(): number {
            return Math.PI * this.radius ** 2;
        }
    }
    
    export function distance(p1: Point, p2: Point): number {
        return Math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2);
    }
    
    // Not exported - internal only
    function clamp(value: number, min: number, max: number): number {
        return Math.max(min, Math.min(max, value));
    }
}

const point1: Geometry.Point = { x: 0, y: 0 };
const point2: Geometry.Point = { x: 3, y: 4 };
console.log("Distance:", Geometry.distance(point1, point2));

const circle = new Geometry.Circle({ x: 0, y: 0 }, 5);
console.log("Circle area:", circle.area().toFixed(2));

// Nested namespaces
namespace App {
    export namespace Models {
        export interface User {
            id: number;
            name: string;
        }
    }
    
    export namespace Services {
        export class UserService {
            getUser(id: number): Models.User {
                return { id, name: "Test User" };
            }
        }
    }
}

const userService = new App.Services.UserService();
console.log("User:", userService.getUser(1));


// ============================================================================
// 6. AMBIENT MODULES
// ============================================================================

console.log("\n=== Ambient Modules ===");

/**
 * Ambient modules = declare types for external libraries
 * Used in .d.ts files
 */

// Declare module without implementation
declare module "my-library" {
    export function doSomething(value: string): number;
    export default class MyClass {
        constructor(name: string);
    }
}

// Now you can import it:
// import MyClass, { doSomething } from 'my-library';

// Wildcard module declarations
declare module "*.json" {
    const value: any;
    export default value;
}

declare module "*.css" {
    const styles: { [key: string]: string };
    export default styles;
}

// Now you can:
// import data from './config.json';
// import styles from './App.css';

console.log("Ambient module declarations");


// ============================================================================
// 7. MODULE AUGMENTATION
// ============================================================================

console.log("\n=== Module Augmentation ===");

/**
 * Module augmentation = add to existing module
 */

// Augment built-in Array type
declare global {
    interface Array<T> {
        first(): T | undefined;
        last(): T | undefined;
    }
}

Array.prototype.first = function<T>(this: T[]): T | undefined {
    return this[0];
};

Array.prototype.last = function<T>(this: T[]): T | undefined {
    return this[this.length - 1];
};

const numbers = [1, 2, 3, 4, 5];
console.log("First:", numbers.first());
console.log("Last:", numbers.last());

// Augment external module
// declare module 'express' {
//     interface Request {
//         user?: { id: number; name: string };
//     }
// }


// ============================================================================
// 8. TRIPLE-SLASH DIRECTIVES
// ============================================================================

console.log("\n=== Triple-Slash Directives ===");

/**
 * Triple-slash directives = compiler instructions
 * Used at top of file
 */

// Reference another file
/// <reference path="./types.d.ts" />

// Reference library
/// <reference lib="es2015" />
/// <reference lib="dom" />

// Reference types package
/// <reference types="node" />
/// <reference types="jest" />

// Note: Mostly replaced by tsconfig.json
console.log("Triple-slash directives (legacy)");


// ============================================================================
// 9. MODULE RESOLUTION STRATEGIES
// ============================================================================

console.log("\n=== Module Resolution ===");

/**
 * TypeScript has two module resolution strategies:
 * 
 * 1. CLASSIC (legacy)
 *    - For non-relative imports, looks in parent directories
 *    - import { a } from 'moduleA'
 *      /root/src/folder/file.ts
 *      -> /root/src/folder/moduleA.ts
 *      -> /root/src/folder/moduleA.d.ts
 *      -> /root/src/moduleA.ts
 *      -> /root/src/moduleA.d.ts
 *      -> /root/moduleA.ts
 *      -> /root/moduleA.d.ts
 * 
 * 2. NODE (default)
 *    - Mimics Node.js module resolution
 *    - Looks in node_modules
 *    - import { a } from 'moduleA'
 *      /root/src/folder/file.ts
 *      -> /root/src/folder/node_modules/moduleA.ts
 *      -> /root/src/folder/node_modules/moduleA/package.json (types)
 *      -> /root/src/folder/node_modules/moduleA/index.ts
 *      -> /root/src/node_modules/moduleA.ts
 *      -> /root/node_modules/moduleA.ts
 * 
 * Configure in tsconfig.json:
 * "moduleResolution": "node"  // or "classic"
 */

console.log("Module resolution strategies: classic vs node");


// ============================================================================
// 10. PATH MAPPING
// ============================================================================

console.log("\n=== Path Mapping ===");

/**
 * Path mapping = custom module paths
 * Configure in tsconfig.json
 */

// tsconfig.json:
// {
//   "compilerOptions": {
//     "baseUrl": ".",
//     "paths": {
//       "@app/*": ["src/app/*"],
//       "@components/*": ["src/components/*"],
//       "@utils/*": ["src/utils/*"]
//     }
//   }
// }

// Now you can import:
// import { Button } from '@components/Button';
// import { api } from '@utils/api';

// Instead of:
// import { Button } from '../../../components/Button';
// import { api } from '../../utils/api';

console.log("Path mapping for cleaner imports");


// ============================================================================
// 11. PRACTICAL PATTERNS
// ============================================================================

console.log("\n=== Practical Patterns ===");

// Barrel exports (index.ts pattern)
// src/models/index.ts:
// export * from './user';
// export * from './product';
// export * from './order';

// Usage:
// import { User, Product, Order } from './models';

// Factory pattern with modules
export class ServiceFactory {
    private static services = new Map<string, any>();
    
    static register<T>(name: string, service: T): void {
        this.services.set(name, service);
    }
    
    static get<T>(name: string): T {
        return this.services.get(name);
    }
}

// Singleton pattern with modules
export class DatabaseConnection {
    private static instance: DatabaseConnection;
    
    private constructor() {}
    
    static getInstance(): DatabaseConnection {
        if (!this.instance) {
            this.instance = new DatabaseConnection();
        }
        return this.instance;
    }
    
    connect(): void {
        console.log("  Database connected");
    }
}

const db1 = DatabaseConnection.getInstance();
const db2 = DatabaseConnection.getInstance();
console.log("Same instance:", db1 === db2);


// ============================================================================
// 12. BEST PRACTICES
// ============================================================================

/**
 * MODULE BEST PRACTICES:
 * 
 * 1. PREFER ES6 MODULES OVER NAMESPACES
 *    Better tooling support
 * 
 * 2. USE BARREL EXPORTS
 *    Cleaner imports with index.ts
 * 
 * 3. ONE MODULE PER FILE
 *    Better code splitting and tree shaking
 * 
 * 4. EXPLICIT IMPORTS
 *    import { specific } instead of import *
 *    Better for tree shaking
 * 
 * 5. PATH MAPPING FOR DEEP IMPORTS
 *    Avoid ../../.. hell
 * 
 * 6. TYPE-ONLY IMPORTS (TS 3.8+)
 *    import type { Type } from './module';
 *    Clearly indicates type-only import
 * 
 * 7. ORGANIZE BY FEATURE
 *    feature/
 *      components/
 *      services/
 *      types/
 *      index.ts
 * 
 * 8. AVOID CIRCULAR DEPENDENCIES
 *    Use interfaces and dependency injection
 * 
 * 9. DOCUMENT PUBLIC API
 *    Clear what's exported and why
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. ES6 modules: export/import");
console.log("2. Named exports vs default exports");
console.log("3. Re-exporting for barrel pattern");
console.log("4. Namespaces (legacy, prefer modules)");
console.log("5. Ambient modules for external libraries");
console.log("6. Module augmentation to extend types");
console.log("7. Module resolution: node vs classic");
console.log("8. Path mapping for cleaner imports");
console.log("9. Type-only imports for clarity");
console.log("10. Organize by feature, use barrel exports");
console.log("=".repeat(80));

export {};
