/**
 * NODE.JS MODULES
 * ===============
 * CommonJS, ES Modules, require vs import
 * TODO: Complete with comprehensive examples
 */

// ============================================================================
// 1. COMMONJS (TRADITIONAL NODE.JS)
// ============================================================================

// Exporting
// module.exports = { ... }
// exports.func = function() { }

// Importing
// const module = require('./module');

// ============================================================================
// 2. ES MODULES (MODERN)
// ============================================================================

// Exporting
// export const func = () => { }
// export default class { }

// Importing
// import { func } from './module.js';
// import Module from './module.js';

/**
 * KEY TAKEAWAYS:
 * 1. CommonJS uses require/module.exports
 * 2. ES Modules use import/export
 * 3. Enable ESM with "type": "module" in package.json
 * 4. .mjs extension for ESM files
 */

export {};
