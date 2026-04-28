# TypeScript - Technical Interview Questions

## 🟢 JUNIOR LEVEL (Fundamentals)

### Basic Types & Type Annotations

1. What are the basic primitive types in TypeScript? How do they differ from JavaScript?
2. What is the difference between `any` and `unknown`? When would you use each?
3. What is the difference between `never` and `void`? Give examples of when `never` is inferred.
4. What is type inference? When should you rely on it vs explicitly annotating types?
5. What is the difference between `const`, `let`, and `readonly` in TypeScript?
6. What are union types? Give an example of a function parameter that accepts multiple types.
7. What are intersection types? How do they differ from interfaces extending other interfaces?
8. What is a literal type? How do you create a type that only allows specific string values?
9. What is the `as` keyword used for? What is the difference between `as` and angle bracket syntax?
10. What is the `!` (non-null assertion) operator? When is it appropriate to use it?

### Interfaces & Type Aliases

11. What is the difference between `interface` and `type`? When would you choose one over the other?
12. How do you make a property optional in an interface? How do you make it readonly?
13. What is interface declaration merging? How does it differ from type aliases?
14. How do you extend an interface? How do you extend a type alias?
15. What is the `extends` keyword in generics? How does it constrain a type parameter?
16. What are index signatures? How do you define an object with dynamic keys?
17. What is the `Record<K, V>` utility type? When would you use it?
18. What is the `Partial<T>` utility type? How does it differ from `Required<T>`?
19. What is the `Pick<T, K>` utility type? How does it differ from `Omit<T, K>`?
20. What is the `Readonly<T>` utility type? How does it differ from using `readonly` on each property?

### Functions

21. How do you type function parameters and return values in TypeScript?
22. What are optional parameters? How do they differ from default parameters?
23. What are rest parameters with types? How do you type a function that accepts any number of arguments?
24. What is a function overload? Give an example of when you would use it.
25. How do you type `this` in a function? When would you need to?
26. What is the difference between `void` return type and `undefined` return type?
27. How do you type a callback function? What is a callable type?

### Arrays & Tuples

28. How do you type an array in TypeScript? What is the difference between `number[]` and `Array<number>`?
29. What is a tuple in TypeScript? How is it different from an array?
30. How do you type a tuple with optional elements? (e.g., `[string, number?]`)
31. What are labeled tuples? (e.g., `[name: string, age: number]`)
32. How do you type a readonly array? What is the difference between `ReadonlyArray<T>` and `readonly T[]`?
33. How do you type a heterogeneous array (mixed types)?

### Enums

34. What is the difference between a numeric enum and a string enum?
35. What is a const enum? How does it differ from a regular enum at runtime?
36. What is reverse mapping in numeric enums? Does it work with string enums?
37. What are the potential issues with numeric enums? (e.g., auto-increment, accidental values)

### Classes

38. How do TypeScript classes differ from JavaScript classes? What access modifiers does TypeScript add?
39. What is the difference between `public`, `protected`, and `private` in TypeScript?
40. What is the difference between TypeScript's `private` and JavaScript's `#` private fields?
41. What are parameter properties? How do they reduce boilerplate in constructors?
42. What is an abstract class? How does it differ from an interface?
43. What is the `implements` keyword? How does it differ from `extends`?
44. What is `this` type in TypeScript? How is it useful for method chaining?

### Type Assertions & Narrowing

45. What is type narrowing? Give examples of `typeof`, `instanceof`, and `in` narrowing.
46. What is a type guard? How do you create a custom type guard using `value is Type`?
47. What is the `satisfies` operator? How does it differ from type annotation?
48. What is the difference between `as const` and `const`? How does `as const` affect literal types?
49. What is the `as any` escape hatch? When is it acceptable to use it?

---

## 🟡 MID-LEVEL (Intermediate)

### Generics

50. What are generics? Give an example of a generic function and a generic type.
51. How do you constrain a generic type parameter with `extends`?
52. What is the difference between `<T extends SomeType>` and `<T = DefaultType>`?
53. What are generic constraints with `keyof`? How do you create a type-safe property accessor?
54. What is a generic conditional type? (e.g., `T extends string ? 'yes' : 'no'`)
55. What is `infer` in conditional types? Give an example of extracting the return type of a function.
56. What is a mapped type? How do you create a type that makes all properties optional?
57. What is a template literal type? Give an example of creating event handler types.
58. What is the `Awaited<T>` utility type? How does it unwrap nested Promises?
59. What is the `ReturnType<T>` utility type? How does it differ from `Parameters<T>`?

### Advanced Types

60. What is a discriminated union? Give an example with a `type` or `kind` property.
61. What is the `ExhaustiveCheck` pattern with `never`? How do you ensure all union cases are handled?
62. What is the `brand` pattern (nominal typing)? How do you create opaque types in TypeScript?
63. What is `Flatten<T>` using conditional types? How do you unwrap nested types?
64. What is the difference between `Required<T>` and `-?` mapped type modifier?
65. What is the `Extract<T, U>` utility type? How does it differ from `Exclude<T, U>`?
66. What is the `NonNullable<T>` utility type? How does it remove `null` and `undefined`?
67. What is the `InstanceType<T>` utility type? When would you use it?

### Modules & Namespaces

68. What is the difference between internal modules (namespaces) and external modules?
69. How do you use `declare module` to augment an existing module?
70. What is a `.d.ts` file? What is its purpose?
71. How do you write type declarations for a JavaScript library that has no types?
72. What is the `triple-slash directive`? When would you use it?
73. What is the difference between `export default` and `export` in TypeScript modules?

### Configuration & Compiler

74. What does `strict: true` enable in `tsconfig.json`? List the individual strict flags.
75. What is `noImplicitAny`? Why is it important to enable?
76. What is `strictNullChecks`? What bugs does it prevent?
77. What is `target` vs `module` in `tsconfig.json`? How do they differ?
78. What is `outDir` and `rootDir`? How do they affect the output structure?
79. What is `declaration: true`? When would you need to generate `.d.ts` files?
80. What is `paths` and `baseUrl` in `tsconfig.json`? How do they simplify imports?
81. What is `esModuleInterop`? What problem does it solve with CommonJS modules?
82. What is `skipLibCheck`? When would you enable it?

### Type Manipulation

83. What is `keyof`? How does it create a union of property names?
84. What is `typeof` in a type context? How does it differ from JavaScript's `typeof`?
85. What is `in` in a mapped type? How does it iterate over union members?
86. What is `as` in a mapped type? How do you remap keys?
87. What is the difference between `Pick<T, K>` and a mapped type with `in keyof`?
88. How do you create a `DeepPartial<T>` type? What are its limitations?

### Error Handling

89. How do you type errors in TypeScript? Why is `catch (e: any)` problematic?
90. How do you create a typed error class hierarchy?
91. What is the `never` type in error handling? How does it help with exhaustive checks?
92. How do you type the result of `JSON.parse()` safely?

### DOM & Environment Types

93. How do you type DOM elements? What is the difference between `HTMLElement` and `HTMLInputElement`?
94. How do you type event handlers? What is the difference between `MouseEvent` and `KeyboardEvent`?
95. How do you type `fetch()` responses? What is the `Response` type?
96. How do you type `localStorage` operations? How do you handle the `null` case?
97. What are ambient declarations? How do you declare types for global variables?

---

## 🔴 SENIOR LEVEL (Advanced)

### Advanced Generics & Type System

98. How do you implement a type-safe builder pattern using generics?
99. How do you create a type that extracts all function property names from an object?
100. How do you create a type that deeply makes all properties readonly?
101. How do you implement a type-safe event emitter with typed event names and payloads?
102. How do you create a type that validates a specific object shape at compile time?
103. What is the difference between covariance and contravariance in TypeScript? How does it affect function types?
104. What is the `strictFunctionTypes` flag? What problem does it solve with function parameter bivariance?
105. How do you implement a type-safe Redux reducer using discriminated unions?
106. How do you create a type that represents a path to a nested property? (e.g., `'user.address.city'`)
107. What is the `IsEqual<T, U>` type? How do you check if two types are exactly equal?

### Conditional & Recursive Types

108. How do you create a recursive type? Give an example like `DeepReadonly<T>`.
109. What is the `JSONified<T>` type? How do you convert a type to its JSON-safe version?
110. How do you create a `UnionToIntersection<T>` type? What is the distributive conditional type trick?
111. What is the `IsNever<T>` type? How do you check if a type is `never`?
112. How do you create a `TupleToUnion<T>` type? How does it differ from `T[number]`?
113. How do you create a `UnionToTuple<T>` type? What are the challenges?
114. What is the `StringToUnion<T>` type? How do you split a string literal into a union of characters?

### Performance & Best Practices

115. What is the performance impact of complex conditional types? How do you optimize them?
116. What is the difference between `interface` and `type` for performance? Which is faster for the compiler?
117. How do you avoid "type instantiation is excessively deep and possibly infinite" errors?
118. What is the `@ts-expect-error` comment? How does it differ from `@ts-ignore`?
119. What is the `@ts-nocheck` comment? When would you use it?
120. How do you gradually migrate a JavaScript codebase to TypeScript? What `tsconfig` settings help?
121. What is the `allowJs` flag? How does it help with incremental migration?
122. How do you handle third-party libraries without types? What is `declare module`?

### Testing TypeScript

123. How do you test types? What is `expectTypeOf` from `vitest` or `@typescript-eslint/utils`?
124. How do you write negative tests (ensuring a type error occurs)?
125. What is the `IsExact<T, U>` pattern for testing type equality?
126. How do you test that a generic function rejects invalid inputs at compile time?

### Design Patterns in TypeScript

127. How do you implement the Builder pattern with type-safe method chaining?
128. How do you implement the Strategy pattern using discriminated unions?
129. How do you implement the Dependency Injection pattern without a framework?
130. How do you implement the Repository pattern with typed queries?
131. How do you implement a type-safe state machine using discriminated unions?
132. How do you implement the Command pattern with typed payloads?

### Decorators & Metadata

133. What are decorators in TypeScript? How do they differ from JavaScript decorators?
134. What is the `experimentalDecorators` flag? Why are decorators still experimental?
135. How do you use `reflect-metadata` with decorators for dependency injection?
136. What is the difference between class, method, accessor, property, and parameter decorators?

### Declaration Files (.d.ts)

137. How do you write a `.d.ts` file for a complex JavaScript library?
138. What is `declare global`? How do you augment global types?
139. How do you write overloaded function declarations in a `.d.ts` file?
140. How do you declare a namespace in a `.d.ts` file?
141. What is the `module` keyword in a `.d.ts` file? How do you declare module types?
142. How do you handle default exports in declaration files?

---

## 💡 BONUS: Problem-Solving & Behavioral

143. How would you type a `fetch` wrapper that returns typed responses based on the endpoint?
144. How would you implement a type-safe `get` function for nested object access?
145. How would you type a Redux-style `createSlice` function with inferred actions?
146. How would you type a `useState`-like hook that infers the type from the initial value?
147. How would you type a function that takes a class constructor and returns an instance?
148. How would you type a `deepMerge` function that preserves the merged type?
149. Describe a time TypeScript caught a bug that would have been difficult to find in JavaScript.
150. How do you convince a team to adopt TypeScript? What arguments do you make?
151. What is your preferred TypeScript configuration for a new project? Why?
152. How do you stay up-to-date with TypeScript releases? Which recent feature excited you most?
