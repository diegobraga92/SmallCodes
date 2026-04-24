# TypeScript Refreshers

Comprehensive TypeScript guide from basics to advanced types.

## 📚 Topics Covered

### Fundamentals ✅
- **00_basic_types.ts** ✅ - Primitives, any, unknown, never, void
- **01_type_annotations.ts** ✅ - Variables, functions, parameters
- **02_interfaces.ts** ✅ - Object shapes, optional properties, readonly
- **03_generics.ts** ✅ - Generic functions, constraints, defaults
- **04_enums.ts** ✅ - Numeric, string, const enums
- **05_utility_types.ts** ✅ - Partial, Required, Pick, Omit, Record

### Intermediate 📝
- **06_advanced_types.ts** 📝 - Mapped types, conditional types, template literals
- **07_type_guards.ts** 📝 - typeof, instanceof, custom type guards
- **08_classes.ts** 📝 - Access modifiers, abstract classes
- **09_decorators.ts** 📝 - Class, method, property decorators
- **10_modules.ts** 📝 - Import/export, module resolution
- **11_tsconfig.ts** 📝 - Compiler options, strict mode
- **12_declaration_files.ts** 📝 - .d.ts files, @types packages
- **13_best_practices.ts** 📝 - Coding standards, patterns

### Status Legend:
- ✅ Complete with comprehensive examples
- 📝 Template/outline (ready to expand)
- ⏳ Coming soon

## 🎯 Learning Path

1. **Start Here** (00-05) - Complete foundations
2. **Intermediate** (06-10) - Advanced type features
3. **Tooling** (11-12) - Configuration and declarations
4. **Best Practices** (13) - Production-ready patterns

## 💡 Quick Tips

- Enable strict mode in tsconfig.json
- Avoid `any`, use `unknown` instead
- Use interfaces for object shapes
- Type aliases for unions/complex types
- Generics for reusable code
- Utility types for transformations
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
