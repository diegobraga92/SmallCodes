# 🟢 Junior Ruby Developer (Foundations)

## 1. Ruby Language Basics
- Syntax, variables, constants  
- Primitive types: String, Integer, Float, Boolean, Nil  
- Control flow (`if`, `unless`, `case`, loops)  
- Methods (definition, parameters, return values)  
- Blocks and basic iteration (`each`, `map`, `select`)  

## 2. Core Data Structures
- Arrays and Hashes (creation, manipulation, iteration)  
- Symbols vs Strings  
- Common enumerable methods  
- Basic algorithmic thinking (searching, filtering, transforming)

## 3. Object-Oriented Programming (OOP)
- Classes and objects  
- Instance vs class methods  
- Attributes (`attr_reader`, `attr_writer`, `attr_accessor`)  
- Inheritance  
- Basic encapsulation  
- `self` context in different scopes.

## 4. Ruby Standard Library Basics
- File I/O (`File`, reading/writing files)  
- Working with JSON (`json` library)  
- Time and Date handling  
- Basic use of built-in modules  

## 5. Error Handling
- Exceptions (`begin`, `rescue`, `ensure`)  
- Raising custom errors  
- Understanding common Ruby errors  

## 6. Command Line & Tooling
- Running Ruby scripts  
- Using `irb` / `pry`  
- Basic debugging techniques (`puts`, `pp`)  

## 7. Version Control
- Git fundamentals  
- Basic workflows (branching, commits, pull requests)  

## 8. Testing Fundamentals
- Basic unit testing concepts  
- Intro to frameworks like RSpec or Minitest  
- Writing simple test cases  


# 🟡 Mid-Level Ruby Developer (Deeper Mastery)

## 1. Advanced OOP & Design
- Composition vs inheritance  
- Modules and mixins  
- Dependency injection  
- SOLID principles applied in Ruby  
- Design patterns (Factory, Strategy, Decorator)

## 2. Blocks, Procs, and Lambdas (Deep Dive)
- Differences between blocks, procs, lambdas  
- Closures  
- Yielding and custom iterators  

## 3. Metaprogramming
- `define_method`, `method_missing`
- Reflection (`send`, `respond_to?`)  
- `class_eval` vs. `instance_eval`
- Open classes and monkey patching (and risks)  

## 4. Enumerables & Functional Patterns
- Deep understanding of `Enumerable`  
- Lazy enumerators  
- Functional chaining and transformations  

## 5. Memory & Performance
- Object allocation basics  
- Garbage collection overview  
- Performance pitfalls (e.g., excessive object creation)  
- Benchmarking (`Benchmark` module)  

## 6. Concurrency & Parallelism
- Threads in Ruby  
- GIL (Global Interpreter Lock) concepts  
- Mutexes and thread safety  
- Intro to processes and forking  
- Fibers: Understanding their lightweight, cooperative nature (even if not used daily, knowing they exist is key).
- The GVL (Global VM Lock) and its implications.

## 7. Gems & Dependency Management
- Creating and structuring a gem  
- Using Bundler  
- Semantic versioning  
- Understanding gem dependencies  

## 8. Testing (Intermediate)
- Test organization and structure  
- Mocks and stubs  
- Test-driven development (TDD)  
- Edge case testing  

## 9. CLI Applications
- Building command-line tools  
- Argument parsing (`OptionParser`)  
- Structuring maintainable CLI apps  

## 10. Code Quality & Maintainability
- Refactoring techniques  
- Linting tools (e.g., RuboCop)  
- Writing idiomatic Ruby  
- Code readability and conventions  

## 11. Working with External Systems
- HTTP requests (`Net::HTTP`, `Faraday`)  
- Parsing APIs (JSON/XML)  
- Basic authentication patterns  

## 12. Debugging & Observability
- Advanced debugging (`pry`, stack traces)  
- Logging best practices  
- Tracing issues in production-like environments  

## 13. Ruby's Object Model (The "Hidden" Complexity):
- The lookup path: `class`, `superclass`, and `ancestors`.
- Singleton classes (eigenclasses).
- `include` vs. `prepend` vs. `extend`.
- How `require` and `load` work.


# 🔵 Optional (Strong Mid-Level → Pre-Senior Edge)

- DSL (Domain-Specific Language) design  
- Event-driven patterns  
- Background job concepts (non-framework-specific)  
- Basic system design thinking  