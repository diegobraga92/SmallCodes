# TypeScript - Technical Interview Questions

## 🟢 JUNIOR LEVEL (Fundamentals)

### Basic Types & Type Annotations

1. **What are the basic primitive types in TypeScript? How do they differ from JavaScript?**

   *Key points: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`. TypeScript adds `any`, `unknown`, `never`, `void`, and literal types. In JavaScript, types are dynamic; TypeScript adds static type checking at compile time.*

2. **What is the difference between `any` and `unknown`? When would you use each?**

   *Key points: `any` disables type checking entirely (can do anything with it). `unknown` is type-safe — you must narrow it before use (typeof, type guard). Use `unknown` for values of uncertain type (API responses, user input). Avoid `any` — it defeats TypeScript's purpose.*

3. **What is the difference between `never` and `void`? Give examples of when `never` is inferred.**

   *Key points: `void` means the function returns undefined (completes normally). `never` means the function never returns (throws error, infinite loop). `never` is inferred in: `function throwError(): never { throw new Error() }`, exhaustive switch defaults, impossible intersections (`string & number`).*

4. **What is type inference? When should you rely on it vs explicitly annotating types?**

   *Key points: TypeScript automatically infers types from values. Rely on inference for: simple variable declarations (`let x = 5`), return types (TypeScript infers from implementation). Explicitly annotate when: function parameters, complex types, when inference isn't specific enough.*

5. **What is the difference between `const`, `let`, and `readonly` in TypeScript?**

   *Key points: `const` prevents reassignment (variable). `let` allows reassignment. `readonly` prevents property modification (on interfaces/types/classes). `const` is a JS concept; `readonly` is a TS type-level concept. `const` infers literal types; `let` infers wider types.*

6. **What are union types? Give an example of a function parameter that accepts multiple types.**

   *Key points: Union types (`|`) allow a value to be one of several types. Example: `function formatId(id: string | number) { return id.toString(); }`. TypeScript narrows the type within conditional blocks.*

7. **What are intersection types? How do they differ from interfaces extending other interfaces?**

   *Key points: Intersection types (`&`) combine multiple types into one: `type Admin = User & { role: 'admin' }`. Similar to `extends` but works with types (not just interfaces). Can create impossible types (`string & number` = `never`). More flexible for combining arbitrary types.*

8. **What is a literal type? How do you create a type that only allows specific string values?**

   *Key points: Literal types are exact values as types: `type Direction = 'north' | 'south' | 'east' | 'west'`. Can be string, number, or boolean literals. Combined with union types for discriminated unions. `as const` preserves literal types.*

9. **What is the `as` keyword used for? What is the difference between `as` and angle bracket syntax?**

   *Key points: `as` is a type assertion: `const value = input as string`. Angle bracket syntax: `const value = <string>input`. Both do the same thing. `as` is preferred (works in JSX, no ambiguity with JSX tags). Type assertions don't change runtime behavior.*

10. **What is the `!` (non-null assertion) operator? When is it appropriate to use it?**

    *Key points: `!` tells TypeScript a value is not null/undefined: `element!.innerHTML`. Use when you know for certain the value exists (e.g., element exists in DOM). Avoid overusing — it bypasses type safety. Prefer proper narrowing or optional chaining.*

### Interfaces & Type Aliases

11. **What is the difference between `interface` and `type`? When would you choose one over the other?**

    *Key points: Interfaces can be extended (declaration merging), types cannot. Types can represent unions, intersections, primitives, tuples. Prefer `interface` for object shapes (better error messages, merging). Prefer `type` for unions, intersections, or non-object types.*

12. **How do you make a property optional in an interface? How do you make it readonly?**

    *Key points: Optional: `name?: string` (with `?`). Readonly: `readonly name: string`. Optional properties can be `undefined` or omitted. Readonly properties can't be reassigned after creation. Both can be used together: `readonly name?: string`.*

13. **What is interface declaration merging? How does it differ from type aliases?**

    *Key points: Declaration merging: multiple declarations of the same interface are automatically merged: `interface User { name: string }` + `interface User { age: number }` = `{ name: string; age: number }`. Types cannot be redeclared. Useful for augmenting third-party types.*

14. **How do you extend an interface? How do you extend a type alias?**

    *Key points: Interface: `interface Admin extends User { role: string }`. Type: `type Admin = User & { role: string }` (intersection). Interfaces can extend multiple: `extends A, B`. Types use `&` for combination. Both achieve similar results.*

15. **What is the `extends` keyword in generics? How does it constrain a type parameter?**

    *Key points: `function getProperty<T, K extends keyof T>(obj: T, key: K)`. `extends` constrains the type parameter to a subset. Ensures the generic argument satisfies certain criteria. Used in conditional types: `T extends string ? 'yes' : 'no'`.*

16. **What are index signatures? How do you define an object with dynamic keys?**

    *Key points: `interface StringMap { [key: string]: string }`. Allows any string key with string values. Can combine with known properties: `interface Config { [key: string]: string; port: number }` (all values must match the index signature type).*

17. **What is the `Record<K, V>` utility type? When would you use it?**

    *Key points: `Record<K, V>` creates an object type with keys `K` and values `V`. Example: `type UserMap = Record<string, User>`. Shorthand for index signatures with specific key types. Useful for dictionaries, lookup tables, enum-to-value mappings.*

18. **What is the `Partial<T>` utility type? How does it differ from `Required<T>`?**

    *Key points: `Partial<T>` makes all properties optional. `Required<T>` makes all properties required. Both are mapped types. `Partial<Config>` is useful for update operations. `Required<Config>` ensures all fields are provided.*

19. **What is the `Pick<T, K>` utility type? How does it differ from `Omit<T, K>`?**

    *Key points: `Pick<T, K>` selects specific keys from T. `Omit<T, K>` removes specific keys from T. `Pick<User, 'name' | 'email'>` = `{ name: string; email: string }`. `Omit<User, 'password'>` = User without password. Both create new types from existing ones.*

20. **What is the `Readonly<T>` utility type? How does it differ from using `readonly` on each property?**

    *Key points: `Readonly<T>` makes all properties readonly. Same as adding `readonly` to each property manually. Prevents reassignment of properties after creation. Useful for immutable data patterns. Works recursively only at one level (use `DeepReadonly` for nested).*

### Functions

21. **How do you type function parameters and return values in TypeScript?**

    *Key points: `function add(a: number, b: number): number { return a + b }`. Arrow: `const add = (a: number, b: number): number => a + b`. Return type can be inferred. Parameters must be annotated (unless `noImplicitAny` is off).*

22. **What are optional parameters? How do they differ from default parameters?**

    *Key points: Optional: `function greet(name?: string)` — `name` can be `string | undefined`. Default: `function greet(name = 'Guest')` — provides default value, type is inferred. Default parameters are always optional. Optional parameters must come after required ones.*

23. **What are rest parameters with types? How do you type a function that accepts any number of arguments?**

    *Key points: `function sum(...numbers: number[]): number`. Rest parameters must be an array type. TypeScript infers the spread type. Can use tuples for typed rest: `function log(...args: [string, number, boolean])`.*

24. **What is a function overload? Give an example of when you would use it.**

    *Key points: Multiple function signatures before the implementation: `function add(a: number, b: number): number; function add(a: string, b: string): string; function add(a: any, b: any): any { return a + b }`. Use when a function returns different types based on input types.*

25. **How do you type `this` in a function? When would you need to?**

    *Key points: `function onClick(this: HTMLButtonElement, event: MouseEvent)`. The first parameter (named `this`) defines the `this` type. Needed in: event handlers, callback-based APIs, methods passed as callbacks where `this` context matters.*

26. **What is the difference between `void` return type and `undefined` return type?**

    *Key points: `void` means the return value is ignored (can return `undefined` or `null` with `strictNullChecks` off). `undefined` means the function must explicitly return `undefined`. `void` is more permissive — the caller can't use the return value.*

27. **How do you type a callback function? What is a callable type?**

    *Key points: `type Callback = (error: Error | null, result: string) => void`. Callable type: `type Greeter = { (name: string): string }`. Can also use `interface Greeter { (name: string): string }`. Callable types can have additional properties.*

### Arrays & Tuples

28. **How do you type an array in TypeScript? What is the difference between `number[]` and `Array<number>`?**

    *Key points: Both are equivalent — `number[]` is syntactic sugar for `Array<number>`. `number[]` is more common. `Array<number>` uses generic syntax. Use `Array<T>` when you need to be explicit or in complex generic contexts.*

29. **What is a tuple in TypeScript? How is it different from an array?**

    *Key points: Tuple: fixed-length array with typed elements at each position: `let pair: [string, number] = ['age', 30]`. Arrays have uniform types. Tuples have specific types per index. Tuples can have optional elements and rest elements.*

30. **How do you type a tuple with optional elements? (e.g., `[string, number?]`)**

    *Key points: `type OptTuple = [string, number?]`. Optional elements must come after required ones. Accessing an optional element returns `T | undefined`. Useful for function parameters or return types with optional trailing values.*

31. **What are labeled tuples? (e.g., `[name: string, age: number]`)**

    *Key points: `type Person = [name: string, age: number]`. Labels improve readability and IDE support. Labels don't affect type checking. Useful for function parameters and return types where positional meaning matters.*

32. **How do you type a readonly array? What is the difference between `ReadonlyArray<T>` and `readonly T[]`?**

    *Key points: Both are equivalent: `ReadonlyArray<T>` and `readonly T[]`. Prevents mutation (push, pop, splice). `readonly T[]` is more common. Use `ReadonlyArray<T>` in generic constraints. `as const` infers readonly arrays.*

33. **How do you type a heterogeneous array (mixed types)?**

    *Key points: `(string | number)[]` — array where each element can be string or number. For specific positions, use tuples: `[string, number]`. For completely mixed types: `any[]` (avoid) or `unknown[]` (type-safe).*

### Enums

34. **What is the difference between a numeric enum and a string enum?**

    *Key points: Numeric: `enum Color { Red, Green, Blue }` — auto-increments from 0. String: `enum Color { Red = 'RED', Green = 'GREEN' }` — each value must be initialized. String enums have no reverse mapping. Numeric enums have runtime reverse mapping.*

35. **What is a const enum? How does it differ from a regular enum at runtime?**

    *Key points: `const enum Color { Red, Green }` — completely inlined at compile time, no runtime object. Regular enums generate a runtime object. Const enums can't have computed members. Use const enums for performance (no runtime overhead).*

36. **What is reverse mapping in numeric enums? Does it work with string enums?**

    *Key points: Reverse mapping: `Color[0]` returns `'Red'` (name from value). Only numeric enums have reverse mapping. String enums don't — they only map name → value, not value → name. This is because numeric enums generate a bidirectional object at runtime.*

37. **What are the potential issues with numeric enums? (e.g., auto-increment, accidental values)**

    *Key points: Auto-increment can cause issues when inserting values in the middle (shifts subsequent values). Any number can be assigned to a numeric enum (no type safety). Accidental values: `Color[100]` returns `undefined` (no error). String enums are safer.*

### Classes

38. **How do TypeScript classes differ from JavaScript classes? What access modifiers does TypeScript add?**

    *Key points: TypeScript adds: `public` (default), `protected` (accessible in class and subclasses), `private` (only in class). Also adds: parameter properties, abstract classes, `implements`, `readonly`. JavaScript has `#` for private fields (ES2020+).*

39. **What is the difference between `public`, `protected`, and `private` in TypeScript?**

    *Key points: `public`: accessible anywhere (default). `protected`: accessible within class and subclasses. `private`: only accessible within the class. These are compile-time only — no runtime enforcement. JavaScript's `#` is truly private at runtime.*

40. **What is the difference between TypeScript's `private` and JavaScript's `#` private fields?**

    *Key points: TS `private` is compile-time only — accessible at runtime via bracket notation. JS `#` is truly private at runtime (hard private). TS `private` works in older JS targets. JS `#` is ES2020+. TS also supports `#` private fields.*

41. **What are parameter properties? How do they reduce boilerplate in constructors?**

    *Key points: `constructor(public name: string, private age: number)`. Automatically creates and initializes class properties. Eliminates manual property declaration and `this.name = name` assignment. Can use `public`, `private`, `protected`, `readonly`.*

42. **What is an abstract class? How does it differ from an interface?**

    *Key points: Abstract class can have implementation (methods, properties). Interface only defines shape (no implementation). Abstract classes can have constructors. A class can extend one abstract class but implement multiple interfaces. Abstract classes can have access modifiers.*

43. **What is the `implements` keyword? How does it differ from `extends`?**

    *Key points: `implements` checks that a class satisfies an interface (structural). `extends` inherits implementation from a parent class. A class can `implement` multiple interfaces but `extend` only one class. `implements` doesn't inherit code — only enforces shape.*

44. **What is `this` type in TypeScript? How is it useful for method chaining?**

    *Key points: `this` as a return type enables fluent method chaining: `class Builder { setX(x: number): this { ... return this } }`. Subclasses return the correct type (not the parent type). Useful for builder pattern and inheritance-safe chaining.*

### Type Assertions & Narrowing

45. **What is type narrowing? Give examples of `typeof`, `instanceof`, and `in` narrowing.**

    *Key points: TypeScript narrows types within conditional blocks. `typeof`: `if (typeof x === 'string')` narrows to string. `instanceof`: `if (x instanceof Date)`. `in`: `if ('name' in obj)`. Also: truthiness narrowing, discriminated unions, type guards.*

46. **What is a type guard? How do you create a custom type guard using `value is Type`?**

    *Key points: A type guard is a function that narrows types: `function isString(value: unknown): value is string { return typeof value === 'string' }`. The `value is Type` return type tells TypeScript the narrowed type. Used in `if` conditions for type narrowing.*

47. **What is the `satisfies` operator? How does it differ from type annotation?**

    *Key points: `const config = { url: 'https://api.com', port: 8080 } satisfies Config`. Checks that the value satisfies the type without widening. Unlike annotation (`: Config`), `satisfies` preserves the literal type for inference. Useful for validating shapes while keeping narrow types.*

48. **What is the difference between `as const` and `const`? How does `as const` affect literal types?**

    *Key points: `const x = 'hello'` — `x` is type `'hello'` (literal). `let y = 'hello' as const` — `y` is type `'hello'` (narrows to literal). `as const` on objects makes all properties readonly and infers literal types. `as const` on arrays makes them readonly tuples.*

49. **What is the `as any` escape hatch? When is it acceptable to use it?**

    *Key points: `as any` bypasses type checking entirely. Acceptable when: migrating JS to TS (temporary), working with untyped third-party code, complex dynamic behavior that's hard to type. Prefer `as unknown as T` for safer casting. Document why it's needed.*

---

## 🟡 MID-LEVEL (Intermediate)

### Generics

50. **What are generics? Give an example of a generic function and a generic type.**

    *Key points: Generics create reusable components that work with multiple types. Generic function: `function identity<T>(arg: T): T { return arg }`. Generic type: `type Box<T> = { value: T }`. TypeScript infers the type parameter from usage.*

51. **How do you constrain a generic type parameter with `extends`?**

    *Key points: `function getLength<T extends { length: number }>(arg: T): number { return arg.length }`. Constrains T to types that have a `length` property. Ensures the generic works only with compatible types. Provides access to the constrained type's properties.*

52. **What is the difference between `<T extends SomeType>` and `<T = DefaultType>`?**

    *Key points: `extends` constrains what T can be (upper bound). `= DefaultType` provides a default when the type isn't inferred. Can combine: `<T extends SomeType = DefaultType>`. Default types are used in generic classes and type aliases.*

53. **What are generic constraints with `keyof`? How do you create a type-safe property accessor?**

    *Key points: `function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] { return obj[key] }`. `keyof T` creates a union of property names. Ensures only valid keys are passed. Return type is the property's value type. Type-safe alternative to `obj[key]`.*

54. **What is a generic conditional type? (e.g., `T extends string ? 'yes' : 'no'`)**

    *Key points: `type IsString<T> = T extends string ? 'yes' : 'no'`. Evaluates types conditionally. Can be nested. Used for: extracting types, filtering unions, creating flexible utility types. Distributes over unions (unless wrapped).*

55. **What is `infer` in conditional types? Give an example of extracting the return type of a function.**

    *Key points: `infer` declares a type variable within a conditional type: `type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never`. `infer R` captures the return type. Used in: `Parameters<T>`, `InstanceType<T>`, `Awaited<T>`.*

56. **What is a mapped type? How do you create a type that makes all properties optional?**

    *Key points: `type MyPartial<T> = { [K in keyof T]?: T[K] }`. Iterates over keys of T and transforms properties. Built-in mapped types: `Partial`, `Required`, `Readonly`, `Pick`. Can add/remove modifiers (`?`, `readonly`) and transform property types.*

57. **What is a template literal type? Give an example of creating event handler types.**

    *Key points: `` type EventName = `on${Capitalize<string>}` ``. Template literal types create string types from patterns: `type EventHandler<K extends string> = `on${Capitalize<K>}``. Used for: event handlers, CSS properties, API paths. Combine with `infer` for parsing.*

58. **What is the `Awaited<T>` utility type? How does it unwrap nested Promises?**

    *Key points: `Awaited<Promise<string>>` = `string`. `Awaited<Promise<Promise<number>>>` = `number`. Recursively unwraps Promises. Useful for typing async function return values. Built-in version of `UnwrapPromise<T>`.*

59. **What is the `ReturnType<T>` utility type? How does it differ from `Parameters<T>`?**

    *Key points: `ReturnType<typeof fn>` extracts the return type of a function type. `Parameters<typeof fn>` extracts the parameter types as a tuple. Both use `infer` in conditional types. `ReturnType<() => string>` = `string`. `Parameters<(a: number) => void>` = `[number]`.*

### Advanced Types

60. **What is a discriminated union? Give an example with a `type` or `kind` property.**

    *Key points: `type Shape = { kind: 'circle'; radius: number } | { kind: 'square'; size: number }`. The `kind` property (discriminant) lets TypeScript narrow the type: `if (shape.kind === 'circle') { shape.radius }`. TypeScript knows the exact shape in each branch.*

61. **What is the `ExhaustiveCheck` pattern with `never`? How do you ensure all union cases are handled?**

    *Key points: `function assertNever(x: never): never { throw new Error('Unexpected: ' + x) }`. In a switch: `default: assertNever(shape)`. If a new union member is added, TypeScript errors at the `assertNever` call. Ensures exhaustive handling of discriminated unions.*

62. **What is the `brand` pattern (nominal typing)? How do you create opaque types in TypeScript?**

    *Key points: `type UserId = string & { __brand: 'UserId' }`. Creates a nominal type (TypeScript is structural by default). Prevents mixing different ID types. Use a helper: `type Brand<T, B> = T & { __brand: B }`. Runtime: just a string (no overhead).*

63. **What is `Flatten<T>` using conditional types? How do you unwrap nested types?**

    *Key points: `type Flatten<T> = T extends any[] ? T[number] : T`. For arrays, extracts the element type. For objects, returns the type as-is. More complex: `type DeepFlatten<T> = T extends any[] ? DeepFlatten<T[number]> : T` for recursive flattening.*

64. **What is the difference between `Required<T>` and `-?` mapped type modifier?**

    *Key points: `Required<T>` uses `-?` internally: `{ [K in keyof T]-?: T[K] }`. `-?` removes the optional modifier. `+?` adds it (default). `Required<T>` is the built-in version. You can use `-?` directly in custom mapped types.*

65. **What is the `Extract<T, U>` utility type? How does it differ from `Exclude<T, U>`?**

    *Key points: `Extract<T, U>` extracts from T types that are assignable to U (intersection). `Exclude<T, U>` removes from T types that are assignable to U (difference). `Extract<string | number, string>` = `string`. `Exclude<string | number, string>` = `number`.*

66. **What is the `NonNullable<T>` utility type? How does it remove `null` and `undefined`?**

    *Key points: `NonNullable<T>` removes `null` and `undefined` from T. Implementation: `type NonNullable<T> = T extends null | undefined ? never : T`. `NonNullable<string | null | undefined>` = `string`. Useful for cleaning up union types.*

67. **What is the `InstanceType<T>` utility type? When would you use it?**

    *Key points: `InstanceType<typeof MyClass>` extracts the instance type from a constructor type. Implementation: `type InstanceType<T> = T extends new (...args: any[]) => infer R ? R : never`. Used in: factory functions, dependency injection, mixins.*

### Modules & Namespaces

68. **What is the difference between internal modules (namespaces) and external modules?**

    *Key points: Namespaces (internal): `namespace MyNamespace { export const x = 1 }` — used for organizing code within a file/global scope (legacy). External modules: `export const x = 1` — use ES modules (import/export). External modules are the modern standard.*

69. **How do you use `declare module` to augment an existing module?**

    *Key points: `declare module 'express' { export interface Request { user?: User } }`. Adds types to existing modules (module augmentation). Useful for extending third-party types. Must be in a module file (has `import`/`export`). Merges with existing declarations.*

70. **What is a `.d.ts` file? What is its purpose?**

    *Key points: `.d.ts` files contain type declarations only (no implementation). Purpose: provide types for JavaScript libraries, describe global types, separate types from implementation. Used by TypeScript for type checking without runtime code.*

71. **How do you write type declarations for a JavaScript library that has no types?**

    *Key points: Create a `.d.ts` file. Use `declare module 'library-name' { export function foo(): void }`. Or use `@types/library-name` if available. For global libraries: `declare namespace MyLib { ... }`. Use `declare` for functions, classes, variables.*

72. **What is the `triple-slash directive`? When would you use it?**

    *Key points: `/// <reference path="./types.d.ts" />`. Single-line comment directives for: referencing other declaration files, specifying the library target. Used in `.d.ts` files. Modern code prefers `import`/`export` over triple-slash directives.*

73. **What is the difference between `export default` and `export` in TypeScript modules?**

    *Key points: `export default` exports a single value as the default: `import X from './module'`. Named `export`: `export const X` → `import { X } from './module'`. Default exports can be imported with any name. Named exports are explicit and support tree-shaking better.*

### Configuration & Compiler

74. **What does `strict: true` enable in `tsconfig.json`? List the individual strict flags.**

    *Key points: Enables all strict type-checking options: `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `alwaysStrict`. Recommended for all projects. Catches the most bugs.*

75. **What is `noImplicitAny`? Why is it important to enable?**

    *Key points: `noImplicitAny` errors when TypeScript can't infer a type and defaults to `any`. Prevents accidentally untyped code. Forces explicit annotations where needed. Part of `strict: true`. Catches bugs from missing type annotations.*

76. **What is `strictNullChecks`? What bugs does it prevent?**

    *Key points: `strictNullChecks` makes `null` and `undefined` distinct types. Prevents: accessing properties on null/undefined, passing null where a value is expected, forgetting to handle null cases. Forces explicit null handling (optional chaining, null checks).*

77. **What is `target` vs `module` in `tsconfig.json`? How do they differ?**

    *Key points: `target`: JS language version for output (ES2015, ES2020, ESNext). `module`: module system for output (CommonJS, ES2020, ESNext). `target` affects syntax (async/await, arrow functions). `module` affects import/export format. Can be different.*

78. **What is `outDir` and `rootDir`? How do they affect the output structure?**

    *Key points: `outDir`: output directory for compiled JS files. `rootDir`: root directory of input source files. TypeScript preserves the directory structure relative to `rootDir` in `outDir`. Example: `src/app.ts` → `dist/app.ts`. Both help organize build output.*

79. **What is `declaration: true`? When would you need to generate `.d.ts` files?**

    *Key points: Generates `.d.ts` declaration files alongside JS output. Needed when: publishing a library (consumers need types), creating a typed API for other TypeScript projects. Without it, consumers can't get type information from your library.*

80. **What is `paths` and `baseUrl` in `tsconfig.json`? How do they simplify imports?**

    *Key points: `baseUrl: '.'` sets the base directory for non-relative imports. `paths: { '@/*': ['src/*'] }` creates import aliases. Enables: `import { User } from '@/models/user'` instead of `'../../../models/user'`. Improves readability and refactoring.*

81. **What is `esModuleInterop`? What problem does it solve with CommonJS modules?**

    *Key points: Enables default imports from CommonJS modules: `import React from 'react'` (instead of `import * as React`). Adds helper code for interoperability. Without it, CommonJS modules with `module.exports` can't use default imports. Recommended for most projects.*

82. **What is `skipLibCheck`? When would you enable it?**

    *Key points: Skips type checking of declaration files (`.d.ts`). Speeds up compilation significantly. Enable when: using many third-party libraries, some libraries have type errors, you trust the library types. Disable if you need strict type checking of library types.*

### Type Manipulation

83. **What is `keyof`? How does it create a union of property names?**

    *Key points: `keyof User` creates a union of property names: `'name' | 'age' | 'email'`. Works on any object type. Used in: generic constraints, mapped types, type-safe property access. `keyof any` = `string | number | symbol`.*

84. **What is `typeof` in a type context? How does it differ from JavaScript's `typeof`?**

    *Key points: TypeScript's `typeof` (type context) gets the type of a value: `type T = typeof obj`. JavaScript's `typeof` (runtime) returns a string: `typeof 5 === 'number'`. TypeScript's `typeof` is compile-time only. Useful for extracting types from values.*

85. **What is `in` in a mapped type? How does it iterate over union members?**

    *Key points: `{ [K in 'a' | 'b']: string }` creates `{ a: string; b: string }`. `in` iterates over each member of a union type. Used in mapped types to transform each property. Can be combined with `keyof` and `as` for key remapping.*

86. **What is `as` in a mapped type? How do you remap keys?**

    *Key points: `{ [K in keyof T as `get${Capitalize<string & K>}`]: T[K] }`. `as` clause remaps property keys (TypeScript 4.1+). Can filter keys: `{ [K in keyof T as T[K] extends Function ? never : K]: T[K] }`. Creates new key names from existing ones.*

87. **What is the difference between `Pick<T, K>` and a mapped type with `in keyof`?**

    *Key points: `Pick<T, K>` selects specific keys. A mapped type `{ [K in keyof T]: T[K] }` transforms all keys. `Pick` is a specific utility; mapped types are more flexible (can add/remove modifiers, transform values, remap keys).*

88. **How do you create a `DeepPartial<T>` type? What are its limitations?**

    *Key points: `type DeepPartial<T> = T extends object ? { [P in keyof T]?: DeepPartial<T[P]> } : T`. Makes all nested properties optional. Limitations: doesn't handle arrays well, can cause infinite recursion with circular types, may not handle special types (Map, Set, Date).*

### Error Handling

89. **How do you type errors in TypeScript? Why is `catch (e: any)` problematic?**

    *Key points: `catch (e: unknown)` is safer — forces type narrowing before use. `catch (e: any)` disables type checking (can access any property without error). TypeScript 4.0+ allows `unknown` in catch clauses. Use type guards to narrow: `if (e instanceof Error)`.*

90. **How do you create a typed error class hierarchy?**

    *Key points: `class AppError extends Error { constructor(public code: number, message: string) { super(message) } }`. `class NotFoundError extends AppError { constructor() { super(404, 'Not found') } }`. Use discriminated unions for error handling: `catch (e) { if (e instanceof NotFoundError) { ... } }`.*

91. **What is the `never` type in error handling? How does it help with exhaustive checks?**

    *Key points: `function assertNever(x: never): never { throw new Error('Unexpected: ' + x) }`. In a switch/catch: `default: assertNever(action)`. If a new case is added, TypeScript errors. Ensures all error types are handled. Also used in exhaustive type narrowing.*

92. **How do you type the result of `JSON.parse()` safely?**

    *Key points: `JSON.parse()` returns `any`. Safe approach: `function parseJSON<T>(json: string): T | ParseError { try { return JSON.parse(json) as T } catch (e) { return new ParseError(e) } }`. Or use `zod` for runtime validation: `UserSchema.parse(JSON.parse(json))`.*

### DOM & Environment Types

93. **How do you type DOM elements? What is the difference between `HTMLElement` and `HTMLInputElement`?**

    *Key points: `HTMLElement` is the base type for all HTML elements. `HTMLInputElement` extends it with input-specific properties (`value`, `checked`, `type`). Use specific types for type-safe property access: `(document.getElementById('input') as HTMLInputElement).value`.*

94. **How do you type event handlers? What is the difference between `MouseEvent` and `KeyboardEvent`?**

    *Key points: `MouseEvent`: click, dblclick, mousedown, mouseup, mousemove (has `clientX`, `clientY`, `button`). `KeyboardEvent`: keydown, keyup, keypress (has `key`, `code`, `ctrlKey`). Use specific event types for type-safe handler parameters.*

95. **How do you type `fetch()` responses? What is the `Response` type?**

    *Key points: `fetch()` returns `Promise<Response>`. `Response` has: `json()`, `text()`, `status`, `ok`, `headers`. Type the parsed data: `const data: User = await response.json()`. Or use a generic wrapper: `async function fetchJSON<T>(url: string): Promise<T>`.*

96. **How do you type `localStorage` operations? How do you handle the `null` case?**

    *Key points: `localStorage.getItem(key)` returns `string | null`. Handle: `const value = localStorage.getItem('key'); if (value !== null) { parse(value) }`. Use a wrapper: `function getStorage(key: string): string | null`. `setItem` takes a string — serialize objects with `JSON.stringify`.*

97. **What are ambient declarations? How do you declare types for global variables?**

    *Key points: `declare var process: { env: { NODE_ENV: string } }`. Ambient declarations describe the shape of global variables without implementation. Used in `.d.ts` files. `declare global { interface Window { myGlobal: string } }` for augmenting global types.*

---

## 🔴 SENIOR LEVEL (Advanced)

### Advanced Generics & Type System

98. **How do you implement a type-safe builder pattern using generics?**

    *Key points: Use a generic type parameter to track built properties: `class Builder<T = {}> { withName(name: string): Builder<T & { name: string }> { ... } build(): T { ... } }`. Each method adds to the type parameter. The final `build()` returns the accumulated type.*

99. **How do you create a type that extracts all function property names from an object?**

    *Key points: `type FunctionKeys<T> = { [K in keyof T]: T[K] extends Function ? K : never }[keyof T]`. Uses mapped type + index access. Filters keys whose values are functions. `FunctionKeys<{ a: string; b: () => void }>` = `'b'`.*

100. **How do you create a type that deeply makes all properties readonly?**

    *Key points: `type DeepReadonly<T> = { readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P] }`. Recursively applies `readonly` to all nested objects. Limitations: doesn't handle arrays, Map, Set, Date. Use `as const` for simpler cases.*

101. **How do you implement a type-safe event emitter with typed event names and payloads?**

    *Key points: `type EventMap = { click: { x: number; y: number }; change: { value: string } }`. `class Emitter<T> { on<K extends keyof T>(event: K, handler: (payload: T[K]) => void): void; emit<K extends keyof T>(event: K, payload: T[K]): void }`. Maps event names to payload types.*

102. **How do you create a type that validates a specific object shape at compile time?**

    *Key points: Use `satisfies` operator: `const config = { url: 'https://api.com' } satisfies Config`. Or branded types: `type Validated<T> = T & { __valid: true }`. For runtime validation, use zod: `const schema = z.object({ name: z.string() })` with `z.infer<typeof schema>`.*

103. **What is the difference between covariance and contravariance in TypeScript? How does it affect function types?**

    *Key points: Covariance: types flow in the same direction (return types — `() => Dog` is assignable to `() => Animal`). Contravariance: types flow in opposite direction (parameter types — `(Animal) => void` is assignable to `(Dog) => void`). TypeScript is covariant for return types, bivariant for parameters by default.*

104. **What is the `strictFunctionTypes` flag? What problem does it solve with function parameter bivariance?**

    *Key points: `strictFunctionTypes` enables contravariant parameter checking (instead of bivariant). Without it: `(Dog) => void` is assignable to `(Animal) => void` (unsafe — could pass a Cat). With it: only `(Animal) => void` is assignable to `(Dog) => void` (safe). Part of `strict: true`.*

105. **How do you implement a type-safe Redux reducer using discriminated unions?**

    *Key points: `type Action = { type: 'increment' } | { type: 'set'; payload: number }`. `function reducer(state: State, action: Action): State { switch(action.type) { case 'increment': return state + 1; case 'set': return action.payload; } }`. TypeScript narrows the action type in each case branch.*

106. **How do you create a type that represents a path to a nested property? (e.g., `'user.address.city'`)**

    *Key points: `type Path<T> = T extends object ? { [K in keyof T]: K | `${K & string}.${Path<T[K]>}` }[keyof T] : never`. Recursively builds string literal unions of dot-separated paths. Complex and can hit recursion limits. Libraries like `type-fest` provide this.*

107. **What is the `IsEqual<T, U>` type? How do you check if two types are exactly equal?**

    *Key points: `type IsEqual<T, U> = (<G>() => G extends T ? 1 : 2) extends (<G>() => G extends U ? 1 : 2) ? true : false`. Uses a function comparison trick to check exact equality. Handles cases where `T extends U && U extends T` isn't sufficient (e.g., `any` vs `unknown`).*

### Conditional & Recursive Types

108. **How do you create a recursive type? Give an example like `DeepReadonly<T>`.**

    *Key points: `type DeepReadonly<T> = { readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P] }`. Recursive types reference themselves. Must have a base case (non-object types). TypeScript has recursion limits (~50 levels). Use sparingly for performance.*

109. **What is the `JSONified<T>` type? How do you convert a type to its JSON-safe version?**

    *Key points: `type JSONified<T> = T extends string | number | boolean | null ? T : T extends Date ? string : T extends Array<infer U> ? JSONified<U>[] : { [K in keyof T]: JSONified<T[K]> }`. Converts Date to string, functions to never, nested objects recursively. Useful for API response types.*

110. **How do you create a `UnionToIntersection<T>` type? What is the distributive conditional type trick?**

    *Key points: `type UnionToIntersection<U> = (U extends any ? (k: U) => void : never) extends (k: infer I) => void ? I : never`. Uses the contravariant position of `k` to convert union to intersection. `UnionToIntersection<A | B>` = `A & B`. Advanced type trick.*

111. **What is the `IsNever<T>` type? How do you check if a type is `never`?**

    *Key points: `type IsNever<T> = [T] extends [never] ? true : false`. The tuple wrapper `[T]` prevents distributive conditional type behavior. Without it, `never extends never ? true : false` returns `never` (not `true`). Essential for type-level testing.*

112. **How do you create a `TupleToUnion<T>` type? How does it differ from `T[number]`?**

    *Key points: `type TupleToUnion<T extends any[]> = T[number]`. `[string, number][number]` = `string | number`. Both are equivalent. `T[number]` is simpler. For more complex transformations, use mapped types: `{ [K in keyof T]: T[K] }[number]`.*

113. **How do you create a `UnionToTuple<T>` type? What are the challenges?**

    *Key points: Converting union to tuple is complex because unions are unordered. Requires splitting the union into individual members. Uses `UnionToIntersection` and function overload tricks. Not natively supported — unions don't have a defined order. Consider using tuples instead of unions.*

114. **What is the `StringToUnion<T>` type? How do you split a string literal into a union of characters?**

    *Key points: `type StringToUnion<S extends string> = S extends `${infer C}${infer Rest}` ? C | StringToUnion<Rest> : never`. Uses template literal type with `infer` to split character by character. `StringToUnion<'abc'>` = `'a' | 'b' | 'c'`. Recursive — limited by string length.*

### Performance & Best Practices

115. **What is the performance impact of complex conditional types? How do you optimize them?**

    *Key points: Complex conditional types slow down compilation. Optimize: avoid deep recursion, use simpler types when possible, limit conditional type nesting, use `interface` over `type` for object shapes, avoid large unions in distributive types. Profile with `tsc --generateTrace`.*

116. **What is the difference between `interface` and `type` for performance? Which is faster for the compiler?**

    *Key points: `interface` is generally faster for the compiler — it's cached, supports declaration merging, and has simpler internal representation. `type` aliases (especially with intersections) can be slower. For object types, prefer `interface`. For unions/computed types, `type` is necessary.*

117. **How do you avoid "type instantiation is excessively deep and possibly infinite" errors?**

    *Key points: Reduce recursion depth. Use simpler types. Avoid recursive conditional types with complex conditions. Limit mapped type nesting. Use `interface` instead of recursive `type`. Increase `--maxNodeModuleJsDepth` if needed. Consider using `any` as a last resort.*

118. **What is the `@ts-expect-error` comment? How does it differ from `@ts-ignore`?**

    *Key points: `@ts-expect-error` expects an error on the next line — errors if no error exists (catches outdated suppressions). `@ts-ignore` silently ignores errors regardless. Prefer `@ts-expect-error` — it's self-documenting and catches when the underlying issue is fixed.*

119. **What is the `@ts-nocheck` comment? When would you use it?**

    *Key points: `// @ts-nocheck` at the top of a file disables type checking for the entire file. Use during: migration from JS to TS (temporary), files with complex dynamic behavior that's hard to type, third-party code you don't control. Avoid in new code.*

120. **How do you gradually migrate a JavaScript codebase to TypeScript? What `tsconfig` settings help?**

    *Key points: 1) Add `tsconfig.json` with `allowJs: true`, `checkJs: false`. 2) Rename files to `.ts` gradually. 3) Enable `strict: true` incrementally. 4) Use `@ts-check` in JS files. 5) Add `// @ts-nocheck` to complex files. 6) Use `any` temporarily. 7) Enable `noImplicitAny` last.*

121. **What is the `allowJs` flag? How does it help with incremental migration?**

    *Key points: `allowJs: true` lets TypeScript process JavaScript files alongside TypeScript files. Enables incremental migration — mix `.js` and `.ts` files. TypeScript checks JS files if `checkJs: true`. Allows importing JS modules from TS files during migration.*

122. **How do you handle third-party libraries without types? What is `declare module`?**

    *Key points: Create a `.d.ts` file with `declare module 'library-name' { export function foo(): void }`. Or use `@types/library-name` if available. For quick fixes: `declare module 'library-name'` (any type). For better safety, add specific type declarations.*

### Testing TypeScript

123. **How do you test types? What is `expectTypeOf` from `vitest` or `@typescript-eslint/utils`?**

    *Key points: `expectTypeOf(result).toEqualTypeOf<ExpectedType>()` (vitest). Asserts types at compile time. `@typescript-eslint/utils` has `expectType`. Type testing catches type regressions. Use in test files alongside runtime tests. Ensures generic functions return correct types.*

124. **How do you write negative tests (ensuring a type error occurs)?**

    *Key points: `// @ts-expect-error` before a line that should error. If no error occurs, TypeScript reports an unused directive. Example: `// @ts-expect-error - should reject string` then `const x: number = 'hello'`. Ensures type guards reject invalid inputs.*

125. **What is the `IsExact<T, U>` pattern for testing type equality?**

    *Key points: `type IsExact<T, U> = (<G>() => G extends T ? 1 : 2) extends (<G>() => G extends U ? 1 : 2) ? true : false`. Checks exact type equality (not just assignability). Used in type tests to ensure types haven't changed unexpectedly.*

126. **How do you test that a generic function rejects invalid inputs at compile time?**

    *Key points: Use `// @ts-expect-error` before invalid calls: `// @ts-expect-error - should reject string` then `identity<string>(42)`. If the function incorrectly accepts the input, TypeScript reports an unused `@ts-expect-error`. Ensures generic constraints work correctly.*

### Design Patterns in TypeScript

127. **How do you implement the Builder pattern with type-safe method chaining?**

    *Key points: Use `this` as return type: `class QueryBuilder { where<K extends keyof T>(key: K, value: T[K]): this { ... return this } }`. Or use generics to track state: `class Builder<T = {}> { withName(name: string): Builder<T & { name: string }> { ... } }`. Enables fluent API with correct types.*

128. **How do you implement the Strategy pattern using discriminated unions?**

    *Key points: `type Strategy = { type: 'percentage'; value: number } | { type: 'fixed'; value: number } | { type: 'freeShipping' }`. `function calculate(strategy: Strategy): number { switch(strategy.type) { ... } }`. TypeScript narrows the strategy in each case. No classes needed — pure types.*

129. **How do you implement the Dependency Injection pattern without a framework?**

    *Key points: Use a container: `class Container { private services = new Map<string, any>(); register<T>(key: string, instance: T): void { this.services.set(key, instance) }; resolve<T>(key: string): T { return this.services.get(key) as T } }`. Type-safe with generics. Simple and framework-free.*

130. **How do you implement the Repository pattern with typed queries?**

    *Key points: `interface Repository<T> { findById(id: string): Promise<T | null>; findAll(filter?: Partial<T>): Promise<T[]>; create(data: Omit<T, 'id'>): Promise<T>; update(id: string, data: Partial<T>): Promise<T>; delete(id: string): Promise<void> }`. Generic CRUD operations with full type safety.*

131. **How do you implement a type-safe state machine using discriminated unions?**

    *Key points: `type State = { status: 'idle' } | { status: 'loading' } | { status: 'success'; data: T } | { status: 'error'; error: Error }`. `function transition(state: State, event: Event): State { switch(state.status) { ... } }`. TypeScript ensures each state has the correct properties.*

132. **How do you implement the Command pattern with typed payloads?**

    *Key points: `type Command = { type: 'createUser'; payload: { name: string; email: string } } | { type: 'deleteUser'; payload: { id: string } }`. `function execute(command: Command) { switch(command.type) { case 'createUser': createUser(command.payload); ... } }`. Type-safe command handling.*

### Decorators & Metadata

133. **What are decorators in TypeScript? How do they differ from JavaScript decorators?**

    *Key points: TypeScript decorators (experimental) use a different syntax and API than the TC39 proposal. TS: `@decorator` on classes/methods/properties. JS (stage 3): different parameter order and capabilities. TS requires `experimentalDecorators: true`. JS decorators are not yet standardized.*

134. **What is the `experimentalDecorators` flag? Why are decorators still experimental?**

    *Key points: Enables TypeScript's legacy decorator implementation. Still experimental because the TC39 decorators proposal has changed significantly. TypeScript's implementation may not match the final spec. Use with caution — may need migration later.*

135. **How do you use `reflect-metadata` with decorators for dependency injection?**

    *Key points: `Reflect.defineMetadata('design:paramtypes', [Logger], target)`. Decorators can read metadata: `Reflect.getMetadata('design:paramtypes', target)`. Used by Angular, InversifyJS for DI. Requires `import 'reflect-metadata'`. Enables runtime type information.*

136. **What is the difference between class, method, accessor, property, and parameter decorators?**

    *Key points: Class decorator: receives constructor. Method decorator: receives target, key, descriptor. Accessor decorator: same as method (getter/setter). Property decorator: receives target, key (no descriptor). Parameter decorator: receives target, key, parameter index. Each has different capabilities and use cases.*

### Declaration Files (.d.ts)

137. **How do you write a `.d.ts` file for a complex JavaScript library?**

    *Key points: Use `declare module 'library' { export function foo(): void; export class Bar { ... } }`. For global libraries: `declare namespace MyLib { ... }`. Use `export =` for CommonJS. Test with `tsc --noEmit`. Publish types via `@types` or bundled `.d.ts`.*

138. **What is `declare global`? How do you augment global types?**

    *Key points: `declare global { interface Window { myApp: MyApp } }`. Augments global types from within a module file. Must be in a module (has `import`/`export`). Useful for adding properties to `Window`, `String`, `Array`, etc. Merges with existing declarations.*

139. **How do you write overloaded function declarations in a `.d.ts` file?**

    *Key points: `declare function add(a: number, b: number): number; declare function add(a: string, b: string): string;`. Multiple signatures without implementation. TypeScript picks the correct overload based on argument types. Order matters — more specific overloads first.*

140. **How do you declare a namespace in a `.d.ts` file?**

    *Key points: `declare namespace MyLib { function foo(): void; namespace inner { const bar: number } }`. Namespaces can be nested. Used for: global libraries, organizing related types. Modern code prefers ES modules over namespaces.*

141. **What is the `module` keyword in a `.d.ts` file? How do you declare module types?**

    *Key points: `declare module 'some-library' { export const version: string }`. Declares types for a module that can be imported. Module names can be patterns: `declare module '*.svg' { const src: string; export default src }`. Wildcard declarations for asset types.*

142. **How do you handle default exports in declaration files?**

    *Key points: `declare module 'library' { const main: () => void; export default main }`. Or `export =` for CommonJS: `declare module 'library' { const main: () => void; export = main }`. Use `esModuleInterop` for compatibility with default imports.*

---

## 💡 BONUS: Problem-Solving & Behavioral

143. **How would you type a `fetch` wrapper that returns typed responses based on the endpoint?**

    *Key points: `type API = { '/users': User[]; '/users/:id': User; '/posts': Post[] }`. `async function fetchAPI<T extends keyof API>(url: T): Promise<API[T]>`. Use a map of endpoint → response type. For dynamic segments, use template literal types or a generic parameter.*

144. **How would you implement a type-safe `get` function for nested object access?**

    *Key points: `function get<T, P extends Path<T>>(obj: T, path: P): PathValue<T, P>`. Uses recursive template literal types to parse dot-separated paths. Returns the type at the path. Complex to implement — libraries like `type-fest` provide `Get` type.*

145. **How would you type a Redux-style `createSlice` function with inferred actions?**

    *Key points: `function createSlice<State, Cases extends Record<string, (state: State, action: any) => State>>(config: { name: string; initialState: State; reducers: Cases })`. Returns typed action creators and reducer. Uses mapped types to infer action types from reducer names.*

146. **How would you type a `useState`-like hook that infers the type from the initial value?**

    *Key points: `function useMyState<T>(initial: T): [T, (value: T | ((prev: T) => T)) => void]`. TypeScript infers `T` from the initial value. The setter accepts both direct values and updater functions. Same pattern as React's `useState`.*

147. **How would you type a function that takes a class constructor and returns an instance?**

    *Key points: `function createInstance<T>(ctor: new (...args: any[]) => T, ...args: any[]): T { return new ctor(...args) }`. `new (...args: any[]) => T` is a constructor signature. Returns the instance type. Can be constrained: `ctor: new (...args: any[]) => BaseClass`.*

148. **How would you type a `deepMerge` function that preserves the merged type?**

    *Key points: `function deepMerge<A, B>(a: A, b: B): A & B`. Simple version returns intersection. For recursive merge: `type DeepMerge<A, B> = { [K in keyof A | keyof B]: K extends keyof A & keyof B ? DeepMerge<A[K], B[K]> : K extends keyof A ? A[K] : B[K] }`. Complex but type-safe.*

149. **Describe a time TypeScript caught a bug that would have been difficult to find in JavaScript.**

    *Key points: Common examples: accessing undefined properties, incorrect API response handling, wrong function argument types, null reference errors, type mismatches in complex data transformations. TypeScript catches these at compile time instead of runtime.*

150. **How do you convince a team to adopt TypeScript? What arguments do you make?**

    *Key points: Catches bugs at compile time (40% reduction in production bugs). Better IDE support (autocomplete, refactoring, navigation). Self-documenting code (types as documentation). Easier onboarding (types clarify code intent). Gradual adoption possible. Industry standard.*

151. **What is your preferred TypeScript configuration for a new project? Why?**

    *Key points: `strict: true` (catches most bugs). `target: ES2020` (modern features). `module: ESNext` (tree-shaking). `esModuleInterop: true` (easier imports). `skipLibCheck: true` (faster compilation). `outDir: ./dist`, `rootDir: ./src`. Adjust based on project needs (Node.js, React, library).*

152. **How do you stay up-to-date with TypeScript releases? Which recent feature excited you most?**

    *Key points: Follow TypeScript blog, GitHub releases, `@typescript` on Twitter/X. Watch Anders Hejlsberg talks. Recent exciting features: `satisfies` operator (4.9), `const` type parameters (5.0), decorators (5.0), `using` declarations (5.2), `import` types (5.5), isolated declarations (5.5).*
