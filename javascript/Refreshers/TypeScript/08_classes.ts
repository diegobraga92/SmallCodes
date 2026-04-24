/**
 * TYPESCRIPT CLASSES
 * ===================
 * Classes with TypeScript: access modifiers, abstract classes, implements
 * TODO: Complete with comprehensive examples
 */

// ============================================================================
// 1. BASIC CLASSES WITH TYPES
// ============================================================================

class Person {
    name: string;
    age: number;
    
    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
    
    greet(): string {
        return `Hello, I'm ${this.name}`;
    }
}

// ============================================================================
// 2. ACCESS MODIFIERS
// ============================================================================

class BankAccount {
    public readonly accountNumber: string;
    private balance: number;
    protected ownerName: string;
    
    constructor(accountNumber: string, initialBalance: number, ownerName: string) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
        this.ownerName = ownerName;
    }
}

// ============================================================================
// 3. PARAMETER PROPERTIES (SHORTHAND)
// ============================================================================

class User {
    constructor(
        public name: string,
        private email: string,
        readonly id: number
    ) {}
}

// ============================================================================
// 4. ABSTRACT CLASSES
// ============================================================================

// TODO: Add abstract classes and methods

// ============================================================================
// 5. IMPLEMENTS INTERFACE
// ============================================================================

// TODO: Add interface implementation examples

/**
 * KEY TAKEAWAYS:
 * 1. public, private, protected access modifiers
 * 2. readonly prevents modification after initialization
 * 3. Parameter properties shorthand
 * 4. Abstract classes for inheritance
 * 5. Implement interfaces with classes
 */

export {};
