/**
 * TYPESCRIPT TYPE GUARDS
 * =======================
 * typeof, instanceof, custom type guards, type predicates
 * TODO: Complete with comprehensive examples
 */

// ============================================================================
// 1. TYPEOF TYPE GUARDS
// ============================================================================

function processValue(value: string | number) {
    if (typeof value === "string") {
        return value.toUpperCase();
    } else {
        return value.toFixed(2);
    }
}

// ============================================================================
// 2. INSTANCEOF TYPE GUARDS
// ============================================================================

class Dog { bark() { console.log("Woof!"); } }
class Cat { meow() { console.log("Meow!"); } }

function makeSound(animal: Dog | Cat) {
    if (animal instanceof Dog) {
        animal.bark();
    } else {
        animal.meow();
    }
}

// ============================================================================
// 3. CUSTOM TYPE GUARDS (TYPE PREDICATES)
// ============================================================================

interface Fish { swim(): void; }
interface Bird { fly(): void; }

function isFish(pet: Fish | Bird): pet is Fish {
    return (pet as Fish).swim !== undefined;
}

// ============================================================================
// 4. IN OPERATOR
// ============================================================================

// TODO: Add 'in' operator examples

// ============================================================================
// 5. DISCRIMINATED UNIONS
// ============================================================================

// TODO: Add discriminated unions (tagged unions)

/**
 * KEY TAKEAWAYS:
 * 1. typeof for primitives
 * 2. instanceof for classes
 * 3. Custom type guards with 'is' keyword
 * 4. 'in' operator for property checks
 * 5. Discriminated unions for type narrowing
 */

export {};
