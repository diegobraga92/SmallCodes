# TypeScript Refreshers

Comprehensive TypeScript guide from basics to advanced types.

## 📚 Topics Covered

### Fundamentals
- **00_basic_types.ts** - Primitives, any, unknown, never, void
- **01_type_annotations.ts** - Variables, functions, parameters
- **02_interfaces.ts** - Object shapes, optional properties, readonly
- **03_type_aliases.ts** - Type aliases vs interfaces, unions, intersections
- **04_functions.ts** - Function types, overloads, generics
- **05_arrays_tuples.ts** - Array types, readonly arrays, tuples

### Intermediate
- **06_enums.ts** - Numeric, string, const enums
- **07_classes.ts** - Classes, access modifiers, abstract classes
- **08_generics.ts** - Generic functions, constraints, defaults
- **09_utility_types.ts** - Partial, Required, Pick, Omit, Record
- **10_type_guards.ts** - typeof, instanceof, user-defined guards
- **11_union_intersection.ts** - Union types, intersection types, narrowing
- **12_literal_types.ts** - String/number literals, template literals
- **13_type_assertions.ts** - as keyword, non-null assertion

### Advanced
- **14_advanced_types.ts** - Mapped types, conditional types, infer
- **15_decorators.ts** - Class, method, property decorators
- **16_modules.ts** - Import/export, namespaces, module resolution
- **17_declaration_files.ts** - .d.ts files, @types, DefinitelyTyped
- **18_typescript_react.tsx** - React with TypeScript, props, hooks
- **19_typescript_node.ts** - Node.js with TypeScript, Express types
- **20_advanced_patterns.ts** - Builder pattern, factory pattern
- **21_performance.ts** - Compilation speed, type checking optimization
- **22_testing.ts** - Jest with TypeScript, type testing
- **23_configuration.ts** - tsconfig.json, compiler options

## 🎯 Learning Path

1. **Type Basics** (00-05)
2. **Type System** (06-13)
3. **Advanced Types** (14-17)
4. **Integration** (18-22)

## 💡 Best Practices

- Enable strict mode in tsconfig.json
- Avoid `any`, use `unknown` instead
- Use interfaces for object shapes
- Type aliases for unions/complex types
- Generics for reusable code
- Utility types for transformations
- Type guards for narrowing
- Readonly for immutability
- Const assertions for literals
- Proper error handling types

## 🚀 Quick Start

```bash
# Install TypeScript
npm install -g typescript

# Initialize tsconfig.json
tsc --init

# Compile TypeScript
tsc

# Watch mode
tsc --watch

# With ts-node (run without compilation)
npm install -D ts-node
npx ts-node app.ts
```

## 📖 Key Concepts

### Type System Benefits
- **Type Safety**: Catch errors at compile time
- **Autocompletion**: Better IDE support
- **Refactoring**: Safe code changes
- **Documentation**: Self-documenting code
- **Maintenance**: Easier to maintain large codebases

### Common tsconfig.json Options
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "**/*.spec.ts"]
}
```

### Type vs Interface
**Use Interface when:**
- Defining object shapes
- Need declaration merging
- OOP patterns

**Use Type Alias when:**
- Unions or intersections
- Mapped types
- Tuple types
- Function types

### Utility Types
- `Partial<T>` - All properties optional
- `Required<T>` - All properties required
- `Readonly<T>` - All properties readonly
- `Pick<T, K>` - Select properties
- `Omit<T, K>` - Remove properties
- `Record<K, T>` - Object type with keys
- `Exclude<T, U>` - Remove from union
- `Extract<T, U>` - Extract from union
- `NonNullable<T>` - Remove null/undefined
- `ReturnType<T>` - Extract return type
- `Parameters<T>` - Extract parameter types

---

Happy TypeScript coding! 📘
