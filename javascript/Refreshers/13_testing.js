/**
 * JAVASCRIPT TESTING
 * ===================
 * Comprehensive guide to testing in JavaScript
 * Jest, testing patterns, TDD, mocking
 */

console.log("=" + "=".repeat(78) + "=");
console.log("JAVASCRIPT TESTING");
console.log("=" + "=".repeat(78) + "=");

// ============================================================================
// 1. TESTING BASICS
// ============================================================================

console.log("\n=== Testing Basics ===");

/**
 * TYPES OF TESTS:
 * 
 * 1. UNIT TESTS:
 *    - Test individual functions/methods
 *    - Fast, isolated
 *    - Most common
 * 
 * 2. INTEGRATION TESTS:
 *    - Test multiple units together
 *    - Database, API calls
 *    - Slower than unit tests
 * 
 * 3. END-TO-END (E2E) TESTS:
 *    - Test entire application flow
 *    - User perspective
 *    - Slowest, most expensive
 * 
 * TEST PYRAMID:
 *        /\
 *       /E2E\      ← Few
 *      /-----\
 *     /Integr\    ← Some
 *    /---------\
 *   /   Unit    \ ← Many
 *  /-------------\
 */


// ============================================================================
// 2. JEST BASICS
// ============================================================================

console.log("\n=== Jest Basics ===");

/**
 * INSTALLATION:
 * npm install --save-dev jest
 * 
 * package.json:
 * {
 *   "scripts": {
 *     "test": "jest",
 *     "test:watch": "jest --watch",
 *     "test:coverage": "jest --coverage"
 *   }
 * }
 */

// Example function to test
function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

/**
 * TEST FILE (math.test.js):
 * 
 * describe('Math operations', () => {
 *     test('adds 1 + 2 to equal 3', () => {
 *         expect(add(1, 2)).toBe(3);
 *     });
 *     
 *     test('subtracts 5 - 3 to equal 2', () => {
 *         expect(subtract(5, 3)).toBe(2);
 *     });
 * });
 */


// ============================================================================
// 3. JEST MATCHERS
// ============================================================================

console.log("\n=== Jest Matchers ===");

/**
 * COMMON MATCHERS:
 * 
 * // Equality
 * expect(value).toBe(expected);              // ===
 * expect(value).toEqual(expected);           // Deep equality
 * expect(value).toStrictEqual(expected);     // Strict deep equality
 * 
 * // Truthiness
 * expect(value).toBeTruthy();
 * expect(value).toBeFalsy();
 * expect(value).toBeNull();
 * expect(value).toBeUndefined();
 * expect(value).toBeDefined();
 * 
 * // Numbers
 * expect(value).toBeGreaterThan(3);
 * expect(value).toBeGreaterThanOrEqual(3);
 * expect(value).toBeLessThan(5);
 * expect(value).toBeLessThanOrEqual(5);
 * expect(value).toBeCloseTo(0.3);  // Floating point
 * 
 * // Strings
 * expect(string).toMatch(/pattern/);
 * expect(string).toContain('substring');
 * 
 * // Arrays/Iterables
 * expect(array).toContain(item);
 * expect(array).toHaveLength(3);
 * 
 * // Objects
 * expect(object).toHaveProperty('key');
 * expect(object).toHaveProperty('key', value);
 * expect(object).toMatchObject({ key: 'value' });
 * 
 * // Exceptions
 * expect(() => func()).toThrow();
 * expect(() => func()).toThrow(Error);
 * expect(() => func()).toThrow('error message');
 * 
 * // Negation
 * expect(value).not.toBe(unexpected);
 */


// ============================================================================
// 4. SETUP AND TEARDOWN
// ============================================================================

console.log("\n=== Setup and Teardown ===");

/**
 * LIFECYCLE HOOKS:
 * 
 * describe('Database tests', () => {
 *     // Run once before all tests
 *     beforeAll(() => {
 *         return initializeDatabase();
 *     });
 *     
 *     // Run before each test
 *     beforeEach(() => {
 *         return clearDatabase();
 *     });
 *     
 *     // Run after each test
 *     afterEach(() => {
 *         return cleanupTest();
 *     });
 *     
 *     // Run once after all tests
 *     afterAll(() => {
 *         return closeDatabase();
 *     });
 *     
 *     test('creates user', () => {
 *         // Test code
 *     });
 * });
 */


// ============================================================================
// 5. TESTING ASYNC CODE
// ============================================================================

console.log("\n=== Testing Async Code ===");

/**
 * ASYNC TESTING:
 * 
 * // Promises
 * test('resolves correctly', () => {
 *     return fetchData().then(data => {
 *         expect(data).toBe('peanut butter');
 *     });
 * });
 * 
 * // Async/await
 * test('async test', async () => {
 *     const data = await fetchData();
 *     expect(data).toBe('peanut butter');
 * });
 * 
 * // Testing rejections
 * test('rejects with error', async () => {
 *     await expect(fetchData()).rejects.toThrow('error');
 * });
 * 
 * // .resolves / .rejects
 * test('resolves to value', () => {
 *     return expect(fetchData()).resolves.toBe('value');
 * });
 * 
 * test('rejects with error', () => {
 *     return expect(fetchData()).rejects.toThrow();
 * });
 */


// ============================================================================
// 6. MOCKING
// ============================================================================

console.log("\n=== Mocking ===");

/**
 * MOCKING FUNCTIONS:
 * 
 * // Create mock
 * const mockFn = jest.fn();
 * 
 * // Mock with return value
 * const mockFn = jest.fn(() => 'return value');
 * mockFn.mockReturnValue('value');
 * mockFn.mockReturnValueOnce('first call');
 * mockFn.mockResolvedValue('async value');
 * mockFn.mockRejectedValue(new Error('async error'));
 * 
 * // Check calls
 * expect(mockFn).toHaveBeenCalled();
 * expect(mockFn).toHaveBeenCalledTimes(2);
 * expect(mockFn).toHaveBeenCalledWith(arg1, arg2);
 * expect(mockFn).toHaveBeenLastCalledWith(arg1);
 * 
 * // Access mock data
 * mockFn.mock.calls;        // All calls
 * mockFn.mock.results;      // All results
 * mockFn.mock.instances;    // All instances
 * 
 * // Clear/reset
 * mockFn.mockClear();       // Clear call history
 * mockFn.mockReset();       // Clear + remove implementation
 * mockFn.mockRestore();     // Restore original (if spied)
 */

/**
 * MOCKING MODULES:
 * 
 * // Mock entire module
 * jest.mock('./api');
 * 
 * // Import mocked module
 * import { fetchData } from './api';
 * 
 * // fetchData is now a mock
 * fetchData.mockResolvedValue({ data: 'mocked' });
 * 
 * test('uses mocked data', async () => {
 *     const result = await fetchData();
 *     expect(result).toEqual({ data: 'mocked' });
 * });
 * 
 * // Partial mock
 * jest.mock('./api', () => ({
 *     ...jest.requireActual('./api'),
 *     fetchData: jest.fn()
 * }));
 */

/**
 * SPYING:
 * 
 * const obj = {
 *     method: () => 'original'
 * };
 * 
 * // Spy on method
 * const spy = jest.spyOn(obj, 'method');
 * 
 * // Method still works
 * obj.method();
 * 
 * // But we can track calls
 * expect(spy).toHaveBeenCalled();
 * 
 * // Mock implementation
 * spy.mockImplementation(() => 'mocked');
 * 
 * // Restore original
 * spy.mockRestore();
 */


// ============================================================================
// 7. SNAPSHOT TESTING
// ============================================================================

console.log("\n=== Snapshot Testing ===");

/**
 * SNAPSHOT TESTING:
 * - Capture output of component/function
 * - Store as snapshot file
 * - Compare future runs
 * - Good for React components, API responses
 * 
 * test('renders correctly', () => {
 *     const tree = renderer.create(<Component />).toJSON();
 *     expect(tree).toMatchSnapshot();
 * });
 * 
 * // Update snapshots: jest --updateSnapshot or jest -u
 */


// ============================================================================
// 8. COVERAGE
// ============================================================================

console.log("\n=== Code Coverage ===");

/**
 * CODE COVERAGE:
 * Run: jest --coverage
 * 
 * METRICS:
 * - Statement coverage: % of statements executed
 * - Branch coverage: % of branches (if/else) taken
 * - Function coverage: % of functions called
 * - Line coverage: % of lines executed
 * 
 * CONFIGURATION (jest.config.js):
 * module.exports = {
 *     collectCoverageFrom: [
 *         'src/**/*.{js,jsx}',
 *         '!src/index.js',
 *         '!src/**/*.test.js'
 *     ],
 *     coverageThreshold: {
 *         global: {
 *             statements: 80,
 *             branches: 80,
 *             functions: 80,
 *             lines: 80
 *         }
 *     }
 * };
 */


// ============================================================================
// 9. TESTING BEST PRACTICES
// ============================================================================

console.log("\n=== Testing Best Practices ===");

/**
 * BEST PRACTICES:
 * 
 * 1. AAA PATTERN (Arrange-Act-Assert):
 *    test('adds numbers', () => {
 *        // Arrange
 *        const a = 1;
 *        const b = 2;
 *        
 *        // Act
 *        const result = add(a, b);
 *        
 *        // Assert
 *        expect(result).toBe(3);
 *    });
 * 
 * 2. ONE ASSERTION PER TEST (when possible):
 *    // BAD
 *    test('user operations', () => {
 *        expect(createUser()).toBeTruthy();
 *        expect(getUser()).toBeTruthy();
 *        expect(deleteUser()).toBeTruthy();
 *    });
 *    
 *    // GOOD
 *    test('creates user', () => {
 *        expect(createUser()).toBeTruthy();
 *    });
 *    test('gets user', () => {
 *        expect(getUser()).toBeTruthy();
 *    });
 * 
 * 3. DESCRIPTIVE TEST NAMES:
 *    // BAD
 *    test('test 1', () => {});
 *    
 *    // GOOD
 *    test('returns user when valid ID is provided', () => {});
 * 
 * 4. TEST EDGE CASES:
 *    test('handles empty string', () => {});
 *    test('handles null input', () => {});
 *    test('handles large numbers', () => {});
 * 
 * 5. DON'T TEST IMPLEMENTATION DETAILS:
 *    // BAD - Testing internal variable
 *    expect(component.state.count).toBe(1);
 *    
 *    // GOOD - Testing output
 *    expect(component.text()).toBe('Count: 1');
 * 
 * 6. KEEP TESTS INDEPENDENT:
 *    - Tests should not depend on each other
 *    - Should be able to run in any order
 *    - Use beforeEach for setup
 * 
 * 7. AVOID LOGIC IN TESTS:
 *    - Tests should be simple
 *    - No loops, conditionals if possible
 *    - Easy to understand
 * 
 * 8. USE MEANINGFUL TEST DATA:
 *    // BAD
 *    const user = { name: 'a', age: 1 };
 *    
 *    // GOOD
 *    const user = { name: 'Alice', age: 30 };
 */


// ============================================================================
// 10. TDD (TEST-DRIVEN DEVELOPMENT)
// ============================================================================

console.log("\n=== Test-Driven Development ===");

/**
 * TDD CYCLE (Red-Green-Refactor):
 * 
 * 1. RED: Write failing test
 *    test('adds numbers', () => {
 *        expect(add(1, 2)).toBe(3);
 *    });
 *    // Test fails - 'add' doesn't exist
 * 
 * 2. GREEN: Write minimum code to pass
 *    function add(a, b) {
 *        return a + b;
 *    }
 *    // Test passes
 * 
 * 3. REFACTOR: Improve code
 *    const add = (a, b) => a + b;
 *    // Test still passes
 * 
 * BENEFITS:
 * ✓ Forces you to think about requirements
 * ✓ Ensures tests are written
 * ✓ Results in testable code
 * ✓ Quick feedback loop
 * ✓ Confidence in refactoring
 */


// ============================================================================
// 11. COMMON TESTING PATTERNS
// ============================================================================

console.log("\n=== Common Testing Patterns ===");

/**
 * 1. TESTING FUNCTIONS:
 *    test('pure function', () => {
 *        expect(add(1, 2)).toBe(3);
 *    });
 * 
 * 2. TESTING OBJECTS:
 *    test('creates user object', () => {
 *        const user = createUser('Alice', 30);
 *        expect(user).toEqual({ name: 'Alice', age: 30 });
 *    });
 * 
 * 3. TESTING ARRAYS:
 *    test('filters array', () => {
 *        const result = filterEven([1, 2, 3, 4]);
 *        expect(result).toEqual([2, 4]);
 *    });
 * 
 * 4. TESTING ERRORS:
 *    test('throws on invalid input', () => {
 *        expect(() => divide(1, 0)).toThrow('Division by zero');
 *    });
 * 
 * 5. TESTING CALLBACKS:
 *    test('calls callback', () => {
 *        const callback = jest.fn();
 *        processData([1, 2, 3], callback);
 *        expect(callback).toHaveBeenCalledTimes(3);
 *    });
 * 
 * 6. TESTING PROMISES:
 *    test('fetches data', async () => {
 *        const data = await fetchData();
 *        expect(data).toHaveProperty('id');
 *    });
 * 
 * 7. TESTING CLASSES:
 *    test('counter increments', () => {
 *        const counter = new Counter();
 *        counter.increment();
 *        expect(counter.getValue()).toBe(1);
 *    });
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Write tests (unit > integration > e2e pyramid)");
console.log("2. Use Jest for JavaScript testing");
console.log("3. Follow AAA pattern (Arrange-Act-Assert)");
console.log("4. Mock external dependencies");
console.log("5. Test edge cases and error conditions");
console.log("6. Keep tests simple and independent");
console.log("7. Use descriptive test names");
console.log("8. Aim for high coverage, but don't obsess");
console.log("9. Consider TDD for better design");
console.log("10. Run tests frequently (CI/CD)");
console.log("=".repeat(80));
