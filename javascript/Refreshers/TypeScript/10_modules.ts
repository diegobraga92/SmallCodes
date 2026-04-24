/**
 * TYPESCRIPT MODULES
 * ===================
 * Import/export, module resolution, namespaces
 * TODO: Complete with comprehensive examples
 */

// ============================================================================
// 1. EXPORT/IMPORT
// ============================================================================

// Export
export interface User {
    id: number;
    name: string;
}

export class UserService {
    getUser(id: number): User {
        return { id, name: "Alice" };
    }
}

export const API_URL = "https://api.example.com";

// Default export
export default class DefaultClass {}

// ============================================================================
// 2. MODULE RESOLUTION
// ============================================================================

// TODO: Add module resolution strategies
// - Classic vs Node
// - Path mapping
// - BaseUrl

// ============================================================================
// 3. NAMESPACES (LEGACY)
// ============================================================================

// TODO: Add namespace examples (prefer modules)

/**
 * KEY TAKEAWAYS:
 * 1. Use ES6 modules (import/export)
 * 2. Configure module resolution in tsconfig
 * 3. Path aliases for cleaner imports
 * 4. Prefer modules over namespaces
 */

export {};
