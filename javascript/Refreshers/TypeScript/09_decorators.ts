/**
 * TYPESCRIPT DECORATORS
 * ======================
 * Class decorators, method decorators, property decorators, parameter decorators
 * Metadata reflection, decorator factories
 * Note: Experimental feature - requires "experimentalDecorators": true in tsconfig.json
 */

console.log("=".repeat(80));
console.log("TYPESCRIPT DECORATORS");
console.log("=".repeat(80));

// ============================================================================
// 1. CLASS DECORATORS
// ============================================================================

console.log("\n=== Class Decorators ===");

/**
 * Class decorator:
 * - Applied to class constructor
 * - Can modify or replace class definition
 */

// Simple class decorator
function sealed(constructor: Function) {
    console.log("  @sealed applied");
    Object.seal(constructor);
    Object.seal(constructor.prototype);
}

@sealed
class SealedClass {
    constructor(public name: string) {}
}

const sealed1 = new SealedClass("test");
console.log("Sealed instance:", sealed1.name);

// Class decorator with return
function timestamped<T extends { new(...args: any[]): {} }>(constructor: T) {
    return class extends constructor {
        createdAt = new Date();
    };
}

@timestamped
class User {
    constructor(public name: string) {}
}

const user = new User("Alice") as User & { createdAt: Date };
console.log("User created at:", user.createdAt);


// ============================================================================
// 2. DECORATOR FACTORIES
// ============================================================================

console.log("\n=== Decorator Factories ===");

/**
 * Decorator factory = function that returns decorator
 * Allows passing parameters to decorator
 */

function Component(options: { selector: string; template: string }) {
    console.log(`  @Component setup with selector: ${options.selector}`);
    
    return function<T extends { new(...args: any[]): {} }>(constructor: T) {
        return class extends constructor {
            selector = options.selector;
            template = options.template;
        };
    };
}

@Component({
    selector: 'app-root',
    template: '<div>Hello World</div>'
})
class AppComponent {
    constructor(public title: string) {}
}

const app = new AppComponent("My App") as AppComponent & { selector: string; template: string };
console.log("Component selector:", app.selector);
console.log("Component template:", app.template);


// ============================================================================
// 3. METHOD DECORATORS
// ============================================================================

console.log("\n=== Method Decorators ===");

/**
 * Method decorator:
 * - Applied to method
 * - Receives: target, propertyKey, descriptor
 * - Can modify method behavior
 */

function log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = function(...args: any[]) {
        console.log(`  Calling ${propertyKey} with args:`, args);
        const result = originalMethod.apply(this, args);
        console.log(`  ${propertyKey} returned:`, result);
        return result;
    };
    
    return descriptor;
}

class Calculator {
    @log
    add(a: number, b: number): number {
        return a + b;
    }
    
    @log
    multiply(a: number, b: number): number {
        return a * b;
    }
}

const calc = new Calculator();
calc.add(5, 3);
calc.multiply(4, 7);

// Measure execution time
function measure(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = async function(...args: any[]) {
        const start = performance.now();
        const result = await originalMethod.apply(this, args);
        const end = performance.now();
        console.log(`  ${propertyKey} took ${(end - start).toFixed(2)}ms`);
        return result;
    };
    
    return descriptor;
}

class Service {
    @measure
    async fetchData(): Promise<string> {
        await new Promise(resolve => setTimeout(resolve, 100));
        return "data";
    }
}

const service = new Service();
service.fetchData().then(data => console.log("Fetched:", data));


// ============================================================================
// 4. PROPERTY DECORATORS
// ============================================================================

console.log("\n=== Property Decorators ===");

/**
 * Property decorator:
 * - Applied to property
 * - Receives: target, propertyKey
 * - Can add metadata
 */

function readonly(target: any, propertyKey: string) {
    console.log(`  @readonly applied to ${propertyKey}`);
    
    Object.defineProperty(target, propertyKey, {
        writable: false,
        configurable: false
    });
}

function format(formatString: string) {
    return function(target: any, propertyKey: string) {
        let value: any;
        
        const getter = function() {
            return value;
        };
        
        const setter = function(newVal: any) {
            value = formatString.replace("{0}", newVal);
        };
        
        Object.defineProperty(target, propertyKey, {
            get: getter,
            set: setter,
            enumerable: true,
            configurable: true
        });
    };
}

class Product {
    @format("Product: {0}")
    name: string;
    
    constructor(name: string) {
        this.name = name;
    }
}

const product = new Product("Laptop");
console.log("Formatted name:", product.name);


// ============================================================================
// 5. PARAMETER DECORATORS
// ============================================================================

console.log("\n=== Parameter Decorators ===");

/**
 * Parameter decorator:
 * - Applied to method parameters
 * - Receives: target, propertyKey, parameterIndex
 * - Used for metadata
 */

function required(target: any, propertyKey: string, parameterIndex: number) {
    console.log(`  @required on parameter ${parameterIndex} of ${propertyKey}`);
    
    const existingRequiredParameters: number[] = 
        Reflect.getMetadata("required", target, propertyKey) || [];
    
    existingRequiredParameters.push(parameterIndex);
    
    Reflect.defineMetadata("required", existingRequiredParameters, target, propertyKey);
}

function validate(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const method = descriptor.value;
    
    descriptor.value = function(...args: any[]) {
        const requiredParameters: number[] = 
            Reflect.getMetadata("required", target, propertyKey) || [];
        
        for (const parameterIndex of requiredParameters) {
            if (parameterIndex >= args.length || args[parameterIndex] === undefined) {
                throw new Error(`Missing required argument at index ${parameterIndex}`);
            }
        }
        
        return method.apply(this, args);
    };
}

class Greeter {
    @validate
    greet(@required name: string, age?: number): string {
        return `Hello ${name}` + (age ? `, age ${age}` : '');
    }
}

const greeter = new Greeter();
try {
    console.log(greeter.greet("Alice", 30));
    // greeter.greet(undefined as any);  // Would throw error
} catch (e) {
    console.log("Error:", (e as Error).message);
}


// ============================================================================
// 6. DECORATOR COMPOSITION
// ============================================================================

console.log("\n=== Decorator Composition ===");

/**
 * Multiple decorators can be applied to same target
 * Executed in order: bottom-up
 */

function first() {
    console.log("  first(): factory evaluated");
    return function(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
        console.log("  first(): called");
    };
}

function second() {
    console.log("  second(): factory evaluated");
    return function(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
        console.log("  second(): called");
    };
}

class Demo {
    @first()
    @second()
    method() {}
}
// Output order:
// first(): factory evaluated
// second(): factory evaluated
// second(): called
// first(): called


// ============================================================================
// 7. METADATA REFLECTION API
// ============================================================================

console.log("\n=== Metadata Reflection ===");

/**
 * reflect-metadata library enables metadata storage
 * npm install reflect-metadata
 * import 'reflect-metadata';
 */

// Note: This example shows the API, but requires reflect-metadata package

function Route(path: string) {
    return function(target: any, propertyKey: string) {
        Reflect.defineMetadata("route", path, target, propertyKey);
    };
}

function HttpGet(target: any, propertyKey: string) {
    Reflect.defineMetadata("method", "GET", target, propertyKey);
}

class Controller {
    @Route("/users")
    @HttpGet
    getUsers() {
        return ["user1", "user2"];
    }
}

// Read metadata
const controller = new Controller();
const route = Reflect.getMetadata("route", controller, "getUsers");
const method = Reflect.getMetadata("method", controller, "getUsers");
console.log(`Route: ${method} ${route}`);


// ============================================================================
// 8. PRACTICAL EXAMPLES
// ============================================================================

console.log("\n=== Practical Examples ===");

// Memoization decorator
function memoize(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    const cache = new Map<string, any>();
    
    descriptor.value = function(...args: any[]) {
        const key = JSON.stringify(args);
        
        if (cache.has(key)) {
            console.log(`  Cache hit for ${propertyKey}(${args.join(", ")})`);
            return cache.get(key);
        }
        
        const result = originalMethod.apply(this, args);
        cache.set(key, result);
        return result;
    };
    
    return descriptor;
}

class MathService {
    @memoize
    fibonacci(n: number): number {
        if (n <= 1) return n;
        return this.fibonacci(n - 1) + this.fibonacci(n - 2);
    }
}

const mathService = new MathService();
console.log("Fib(10):", mathService.fibonacci(10));
console.log("Fib(10) again:", mathService.fibonacci(10));

// Deprecation warning
function deprecated(message?: string) {
    return function(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
        const originalMethod = descriptor.value;
        
        descriptor.value = function(...args: any[]) {
            console.warn(`  Warning: ${propertyKey} is deprecated. ${message || ''}`);
            return originalMethod.apply(this, args);
        };
        
        return descriptor;
    };
}

class OldAPI {
    @deprecated("Use newMethod() instead")
    oldMethod(): void {
        console.log("  Old method called");
    }
    
    newMethod(): void {
        console.log("  New method called");
    }
}

const api = new OldAPI();
api.oldMethod();

// Retry decorator
function retry(times: number = 3) {
    return function(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
        const originalMethod = descriptor.value;
        
        descriptor.value = async function(...args: any[]) {
            for (let i = 0; i < times; i++) {
                try {
                    return await originalMethod.apply(this, args);
                } catch (error) {
                    if (i === times - 1) throw error;
                    console.log(`  Retry ${i + 1}/${times} for ${propertyKey}`);
                }
            }
        };
        
        return descriptor;
    };
}

class NetworkService {
    private attempts = 0;
    
    @retry(3)
    async unreliableFetch(): Promise<string> {
        this.attempts++;
        if (this.attempts < 3) {
            throw new Error("Network error");
        }
        return "success";
    }
}

const netService = new NetworkService();
netService.unreliableFetch()
    .then(result => console.log("Fetch result:", result))
    .catch(err => console.error("Fetch failed:", err));


// ============================================================================
// 9. BEST PRACTICES
// ============================================================================

/**
 * DECORATOR BEST PRACTICES:
 * 
 * 1. USE DECORATOR FACTORIES FOR PARAMETERS
 *    More flexible and reusable
 * 
 * 2. PRESERVE 'THIS' CONTEXT
 *    Use arrow functions or .apply(this)
 * 
 * 3. RETURN DESCRIPTOR
 *    Maintain proper typing
 * 
 * 4. DOCUMENT DECORATOR BEHAVIOR
 *    Side effects not obvious from code
 * 
 * 5. HANDLE ASYNC METHODS PROPERLY
 *    Consider Promise return types
 * 
 * 6. USE METADATA FOR CONFIGURATION
 *    reflect-metadata for complex scenarios
 * 
 * 7. KEEP DECORATORS SIMPLE
 *    Complex logic belongs elsewhere
 * 
 * 8. TEST DECORATED CODE
 *    Decorators can hide bugs
 */


console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Decorators = special declarations for classes, methods, properties");
console.log("2. Class decorators modify/replace class definition");
console.log("3. Method decorators can intercept method calls");
console.log("4. Property decorators add metadata or modify behavior");
console.log("5. Decorator factories allow parameterization");
console.log("6. Multiple decorators compose bottom-up");
console.log("7. reflect-metadata enables advanced metadata");
console.log("8. Use for cross-cutting concerns (logging, caching, validation)");
console.log("9. Experimental feature - enable in tsconfig");
console.log("10. Keep decorators simple and well-documented");
console.log("=".repeat(80));

export {};
