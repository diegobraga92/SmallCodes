/**
 * JAVASCRIPT MODULES
 * ===================
 * Comprehensive guide to JavaScript module systems
 * ES6 Modules (ESM) and CommonJS
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT MODULES");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. ES6 MODULES (ESM)
// ============================================================================

/**
 * ESM vs COMMONJS - WHICH TO USE?
 * ================================
 * 
 * ES6 MODULES (ESM):
 * - Syntax: import/export
 * - Standard JavaScript (official spec)
 * - STATIC imports (analyzed before runtime)
 * - Works in: Browsers, modern Node.js
 * - Better tree-shaking (dead code elimination)
 * - Asynchronous module loading
 * - File extensions: .mjs or "type": "module" in package.json
 * 
 * COMMONJS (CJS):
 * - Syntax: require()/module.exports
 * - Node.js legacy format
 * - DYNAMIC imports (runtime)
 * - Works in: Node.js (default)
 * - Synchronous loading
 * - File extensions: .js or .cjs
 * 
 * KEY DIFFERENCES:
 * 
 * 1. STATIC vs DYNAMIC:
 *    ESM:      import { x } from './file';  // Before runtime
 *    CommonJS: const { x } = require('./file');  // At runtime
 * 
 * 2. TOP-LEVEL AWAIT:
 *    ESM:      await fetch(...);  // ✓ Allowed
 *    CommonJS: await fetch(...);  // ❌ Not allowed (use async IIFE)
 * 
 * 3. TREE-SHAKING:
 *    ESM:      ✓ Unused exports removed by bundlers
 *    CommonJS: ❌ Whole module included
 * 
 * 4. THIS BINDING:
 *    ESM:      'this' is undefined at top level
 *    CommonJS: 'this' is module.exports
 * 
 * 5. __dirname, __filename:
 *    ESM:      ❌ Not available (use import.meta.url)
 *    CommonJS: ✓ Available
 * 
 * WHEN TO USE ESM:
 * ✓ New projects (2024+ standard)
 * ✓ Browser code
 * ✓ Want tree-shaking
 * ✓ Modern build tools (Vite, Webpack 5+)
 * ✓ Future-proof
 * 
 * WHEN TO USE COMMONJS:
 * ✓ Legacy Node.js projects
 * ✓ Need dynamic imports (conditional requires)
 * ✓ Compatibility with old packages
 * ✓ Simple Node.js scripts
 * 
 * INTEROPERABILITY:
 * - ESM can import CommonJS (one-way)
 * - CommonJS CANNOT require ESM directly
 * - Use dynamic import() in CommonJS for ESM
 * 
 * RECOMMENDATION FOR NEW CODE:
 * Use ESM! It's the standard and future of JavaScript modules.
 */

console.log("\n=== ES6 Modules ===");

// NAMED EXPORTS (multiple exports per file)
// math.js
/*
export function add(a, b) {
    return a + b;
}

export function subtract(a, b) {
    return a - b;
}

export const PI = 3.14159;

export class Calculator {
    multiply(a, b) {
        return a * b;
    }
}
*/

// NAMED IMPORTS
/*
import { add, subtract, PI, Calculator } from './math.js';

console.log(add(2, 3));
console.log(PI);
const calc = new Calculator();
*/

// Import with alias
/*
import { add as sum, subtract as diff } from './math.js';
console.log(sum(5, 3));
*/

// Import all as namespace
/*
import * as math from './math.js';
console.log(math.add(2, 3));
console.log(math.PI);
*/


// DEFAULT EXPORTS (one default export per file)
// user.js
/*
export default class User {
    constructor(name) {
        this.name = name;
    }
    
    greet() {
        return `Hello, ${this.name}`;
    }
}
*/

// DEFAULT IMPORT
/*
import User from './user.js';
const user = new User("Alice");
console.log(user.greet());
*/

// Can name default import anything
/*
import MyUser from './user.js';  // Same thing
*/


// MIXING DEFAULT AND NAMED EXPORTS
// utils.js
/*
export default function mainFunction() {
    return "Main";
}

export function helper1() {
    return "Helper 1";
}

export function helper2() {
    return "Helper 2";
}
*/

// IMPORT BOTH
/*
import mainFunction, { helper1, helper2 } from './utils.js';
*/


// RE-EXPORTING
// index.js (barrel file)
/*
export { add, subtract } from './math.js';
export { default as User } from './user.js';
export * from './helpers.js';  // Re-export all named exports
*/

// Use barrel file
/*
import { add, subtract, User } from './index.js';
*/


// ============================================================================
// 2. COMMONJS (Node.js Traditional)
// ============================================================================

console.log("\n=== CommonJS ===");

/**
 * COMMONJS (MODULE.EXPORTS / REQUIRE)
 * - Traditional Node.js module system
 * - Dynamic imports (runtime)
 * - Synchronous loading
 * - Still widely used in Node.js
 */

// EXPORTING
// math.js
/*
function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

module.exports = {
    add,
    subtract,
    PI: 3.14159
};
*/

// OR (single export)
/*
module.exports = class Calculator {
    multiply(a, b) {
        return a * b;
    }
};
*/

// OR (using exports shorthand)
/*
exports.add = function(a, b) {
    return a + b;
};
*/

// IMPORTING
/*
const math = require('./math.js');
console.log(math.add(2, 3));
console.log(math.PI);
*/

// Destructuring
/*
const { add, subtract } = require('./math.js');
console.log(add(2, 3));
*/


// ============================================================================
// 3. DYNAMIC IMPORTS (ESM)
// ============================================================================

console.log("\n=== Dynamic Imports ===");

/**
 * DYNAMIC IMPORTS
 * - Load modules conditionally or on-demand
 * - Returns a promise
 * - Code splitting in bundlers
 */

// Dynamic import example
async function loadModule() {
    if (someCondition) {
        const module = await import('./module.js');
        module.default();
        module.namedExport();
    }
}

// Conditional loading
async function loadHeavyFeature() {
    const { heavyFunction } = await import('./heavy-module.js');
    heavyFunction();
}

// In browsers (code splitting)
/*
button.addEventListener('click', async () => {
    const module = await import('./chart.js');
    module.renderChart(data);
});
*/


// ============================================================================
// 4. MODULE PATTERNS (PRE-ES6)
// ============================================================================

console.log("\n=== Module Patterns ===");

// IIFE Module Pattern
const MyModule = (function() {
    // Private variables
    let privateVar = "private";
    
    function privateMethod() {
        return "This is private";
    }
    
    // Public API
    return {
        publicMethod() {
            return `Public method accessing ${privateVar}`;
        },
        
        getPrivate() {
            return privateMethod();
        }
    };
})();

console.log(MyModule.publicMethod());
// console.log(MyModule.privateVar);  // undefined


// Revealing Module Pattern
const Calculator2 = (function() {
    let result = 0;
    
    function add(n) {
        result += n;
        return this;
    }
    
    function subtract(n) {
        result -= n;
        return this;
    }
    
    function getResult() {
        return result;
    }
    
    function reset() {
        result = 0;
    }
    
    // Reveal public methods
    return {
        add,
        subtract,
        getResult,
        reset
    };
})();


// ============================================================================
// 5. ESM VS COMMONJS COMPARISON
// ============================================================================

console.log("\n=== ESM vs CommonJS ===");

/**
 * ES6 MODULES (ESM):
 * ✓ Standard, works in browsers
 * ✓ Static analysis (better optimization)
 * ✓ Tree-shaking (dead code elimination)
 * ✓ Named and default exports
 * ✓ Asynchronous loading
 * ✗ Relatively newer
 * 
 * COMMONJS:
 * ✓ Widely used in Node.js
 * ✓ Synchronous (simpler mental model)
 * ✓ Dynamic requires
 * ✓ Mature ecosystem
 * ✗ Not standard
 * ✗ No tree-shaking
 * ✗ Doesn't work in browsers without bundling
 */

/**
 * WHEN TO USE WHAT:
 * 
 * Use ESM when:
 * - Writing modern JavaScript
 * - Building for browsers
 * - Want tree-shaking
 * - Using modern Node.js (>= 14)
 * 
 * Use CommonJS when:
 * - Maintaining older Node.js projects
 * - Need dynamic requires
 * - Working with packages that only support CommonJS
 */


// ============================================================================
// 6. MODULE BEST PRACTICES
// ============================================================================

console.log("\n=== Best Practices ===");

/**
 * BEST PRACTICES:
 * 
 * 1. ONE MODULE PER FILE
 *    - Keep modules focused
 *    - Single responsibility
 * 
 * 2. USE NAMED EXPORTS FOR UTILITIES
 *    - Better for tree-shaking
 *    - Explicit imports
 * 
 * 3. USE DEFAULT EXPORTS FOR COMPONENTS/CLASSES
 *    - One main thing per file
 *    - React components
 * 
 * 4. AVOID CIRCULAR DEPENDENCIES
 *    - Module A imports B, B imports A
 *    - Can cause issues
 * 
 * 5. BARREL FILES (index.js)
 *    - Group related exports
 *    - Simplify imports
 *    
 *    // components/index.js
 *    export { Button } from './Button.js';
 *    export { Input } from './Input.js';
 *    
 *    // Usage
 *    import { Button, Input } from './components';
 * 
 * 6. ABSOLUTE IMPORTS
 *    - Use path aliases in bundler config
 *    import { utils } from '@/utils';  // vs ../../../../utils
 * 
 * 7. IMPORT ORDER
 *    - External packages first
 *    - Internal modules second
 *    - Relative imports last
 *    
 *    import React from 'react';           // External
 *    import { Button } from '@/components'; // Internal
 *    import './styles.css';               // Relative
 */


// ============================================================================
// 7. NODE.JS ESM USAGE
// ============================================================================

console.log("\n=== Using ESM in Node.js ===");

/**
 * ENABLE ESM IN NODE.JS:
 * 
 * Option 1: Use .mjs extension
 * - file.mjs
 * 
 * Option 2: Add to package.json
 * {
 *   "type": "module"
 * }
 * 
 * Option 3: Use .cjs for CommonJS when "type": "module"
 * - file.cjs
 * 
 * DIFFERENCES IN NODE.JS:
 * - No __dirname, __filename in ESM
 * - Use import.meta.url instead
 * 
 * import { fileURLToPath } from 'url';
 * import { dirname } from 'path';
 * 
 * const __filename = fileURLToPath(import.meta.url);
 * const __dirname = dirname(__filename);
 */


// ============================================================================
// 8. INTEROPERABILITY
// ============================================================================

console.log("\n=== ESM and CommonJS Interop ===");

/**
 * IMPORTING COMMONJS IN ESM:
 * Works fine, CommonJS module becomes default export
 * 
 * // CommonJS module
 * module.exports = { foo: 'bar' };
 * 
 * // ESM import
 * import pkg from './commonjs-module.cjs';
 * console.log(pkg.foo);
 * 
 * IMPORTING ESM IN COMMONJS:
 * Can only use dynamic import()
 * 
 * // CommonJS file
 * async function loadESM() {
 *     const esmModule = await import('./esm-module.mjs');
 *     console.log(esmModule.default);
 * }
 */


// ============================================================================
// 9. COMMON PITFALLS
// ============================================================================

console.log("\n=== Common Pitfalls ===");

/**
 * 1. MIXING module.exports AND exports
 *    // DON'T
 *    exports.foo = 'bar';
 *    module.exports = { baz: 'qux' };  // Overwrites exports.foo
 * 
 * 2. FORGETTING FILE EXTENSIONS IN ESM
 *    // DON'T (in Node.js ESM)
 *    import { foo } from './module';
 *    
 *    // DO
 *    import { foo } from './module.js';
 * 
 * 3. CIRCULAR DEPENDENCIES
 *    // file-a.js
 *    import { b } from './file-b.js';
 *    export const a = 1;
 *    
 *    // file-b.js
 *    import { a } from './file-a.js';
 *    export const b = 2;
 *    
 *    // Can cause undefined or partial initialization
 * 
 * 4. USING require() IN ESM
 *    // DON'T
 *    const module = require('./module');  // Error in ESM!
 *    
 *    // DO
 *    import module from './module.js';
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Use ESM (import/export) for modern JavaScript");
console.log("2. Named exports for utilities, default for main component");
console.log("3. Use dynamic import() for code splitting");
console.log("4. CommonJS still common in Node.js ecosystem");
console.log("5. Avoid circular dependencies");
console.log("6. Use barrel files (index.js) to organize exports");
console.log("7. Static imports enable tree-shaking");
console.log("8. Include .js extension in Node.js ESM");
console.log("=".repeat(80));
