# JavaScript Core - Technical Interview Questions

## 🟢 JUNIOR LEVEL (Fundamentals)

### Variables, Data Types & Type Coercion

1. **What are the differences between `var`, `let`, and `const`? When would you use each?**

   *Key points: `var` — function-scoped, hoisted (initialized as `undefined`), can be redeclared. `let` — block-scoped, hoisted (TDZ), can be reassigned. `const` — block-scoped, hoisted (TDZ), cannot be reassigned (but objects can be mutated). Use `const` by default, `let` when reassignment needed, never `var` in modern code.*

2. **What are the 7 primitive types in JavaScript? How do they differ from reference types?**

   *Key points: Primitives: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`. Primitives are immutable, stored by value. Reference types (objects, arrays, functions) are mutable, stored by reference. Primitives are compared by value; objects by reference.*

3. **Explain the difference between `null` and `undefined`. When would you use each intentionally?**

   *Key points: `undefined` — variable declared but not assigned (default). `null` — intentional absence of value (assigned). Use `null` to explicitly clear a value, `undefined` is the default for uninitialized variables. `typeof null` returns `"object"` (historical bug).*

4. **What is the difference between `==` and `===`? Why is `===` generally preferred?**

   *Key points: `==` — loose equality (performs type coercion). `===` — strict equality (no coercion, checks type and value). Prefer `===` to avoid unexpected coercion bugs. Exception: `== null` checks both `null` and `undefined`.*

5. **What are the 6 falsy values in JavaScript? Give an example of a common bug caused by falsy coercion.**

   *Key points: `false`, `0`, `""` (empty string), `null`, `undefined`, `NaN`. Bug: `if (value)` where `value` is `0` — the condition is false even though `0` may be a valid value. Fix: check explicitly `if (value !== undefined)` or `if (typeof value === 'number')`.*

6. **Explain explicit vs implicit type coercion. Give examples of when implicit coercion can be surprising.**

   *Key points: Explicit: `Number("5")`, `String(42)`, `Boolean(0)`. Implicit: `"5" - 3` → `2`, `"5" + 3` → `"53"` (string concatenation wins). Surprising: `[] + []` → `""`, `[] + {}` → `"[object Object]"`, `null + 1` → `1`, `undefined + 1` → `NaN`.*

7. **What is `NaN`? How do you check if a value is `NaN`? Why doesn't `NaN === NaN` work?**

   *Key points: `NaN` (Not a Number) is a numeric value representing an invalid number. `NaN === NaN` is `false` (IEEE 754 spec). Check with `Number.isNaN(value)` (reliable) or `isNaN(value)` (coerces to number first). `Object.is(NaN, NaN)` returns `true`.*

8. **What is the difference between `typeof null` and `typeof undefined`? Why is `typeof null` considered a bug?**

   *Key points: `typeof null` → `"object"` (historical bug from early JS where object type tag was 0, and null pointer was 0x00). `typeof undefined` → `"undefined"`. Cannot use `typeof` to check for `null` — use `value === null`.*

9. **Explain the difference between `undefined` and "not defined" (ReferenceError).**

   *Key points: `undefined` — variable exists but has no value assigned. "Not defined" (ReferenceError) — variable was never declared. `console.log(x)` where `x` is not declared throws ReferenceError. `let x; console.log(x)` logs `undefined`.*

10. **What is the Temporal Dead Zone (TDZ) in relation to `let` and `const`?**

    *Key points: TDZ is the period between entering scope and variable declaration where `let`/`const` variables exist but cannot be accessed. Accessing throws ReferenceError. `var` doesn't have TDZ (hoisted with `undefined`). TDZ prevents accessing before initialization.*

### Operators & Expressions

11. **What is the difference between `++x` and `x++`?**

    *Key points: `++x` (pre-increment) — increments then returns new value. `x++` (post-increment) — returns original value then increments. Same for `--x` and `x--`. Example: `let a = 5; let b = ++a;` → `a=6, b=6`. `let a = 5; let b = a++;` → `a=6, b=5`.*

12. **Explain short-circuit evaluation with `&&` and `||`. Give a practical example of each.**

    *Key points: `&&` returns first falsy value or last truthy. `||` returns first truthy value or last falsy. Examples: `const name = user.name || "Guest"` (default value). `isAdmin && showAdminPanel()` (guard clause). `||` for defaults, `&&` for conditional execution.*

13. **What is the nullish coalescing operator (`??`)? How does it differ from `||`?**

    *Key points: `??` returns right side only if left is `null` or `undefined`. `||` returns right side for any falsy value (`0`, `""`, `false`). Use `??` when `0` or `""` are valid values. Example: `count ?? 10` — keeps `0`, uses `10` for `null`/`undefined`.*

14. **What is optional chaining (`?.`) and how does it prevent errors?**

    *Key points: `?.` short-circuits if the value is `null`/`undefined`, returning `undefined` instead of throwing. Examples: `user?.address?.street`, `obj?.method?.()`, `arr?.[0]`. Prevents "Cannot read property of null/undefined" errors. Works with `??` for defaults.*

15. **Explain the spread operator (`...`) for arrays and objects. How does it differ from `Object.assign()`?**

    *Key points: Spread copies own enumerable properties. Arrays: `[...arr1, ...arr2]`, `[first, ...rest]`. Objects: `{...obj1, ...obj2}` (shallow copy). `Object.assign(target, ...sources)` mutates target; spread doesn't. Spread is more concise and preferred for copying.*

16. **What is the ternary operator? When is it appropriate vs when should you use `if/else`?**

    *Key points: `condition ? exprIfTrue : exprIfFalse`. Use for simple conditional assignments: `const status = age >= 18 ? "adult" : "minor"`. Avoid for complex logic, nested ternaries (hard to read), or statements (use `if/else`). Keep ternaries short and single-purpose.*

17. **What is the difference between `&&=` and `??=` logical assignment operators?**

    *Key points: `x &&= y` — assigns `y` to `x` only if `x` is truthy (equivalent to `x && (x = y)`). `x ??= y` — assigns `y` to `x` only if `x` is nullish (equivalent to `x ?? (x = y)`). `||=` — assigns if `x` is falsy. Useful for default values and conditional updates.*

### Control Flow

18. **What is the difference between `for...in` and `for...of`? When would you use each?**

    *Key points: `for...in` iterates over enumerable property keys (including prototype chain). `for...of` iterates over iterable values (arrays, strings, Maps, Sets). Use `for...in` for objects (with `hasOwnProperty` check), `for...of` for arrays and iterables.*

19. **How does `break` differ from `continue` in loops? Give a practical example of each.**

    *Key points: `break` exits the loop entirely. `continue` skips the current iteration and moves to the next. Example: `break` — stop searching after finding an item. `continue` — skip invalid items in a loop: `if (!item.isValid) continue; process(item)`.*

20. **What is a labeled statement in JavaScript? When would you use `break outerLoop`?**

    *Key points: Labels allow `break`/`continue` to target outer loops. `outerLoop: for (...) { for (...) { if (condition) break outerLoop; } }`. Use when you need to break out of nested loops. Rarely needed — consider extracting to a function with `return` instead.*

21. **Explain the `switch` statement. What happens if you forget a `break`? When is fall-through intentional?**

    *Key points: `switch` compares with `===`. Without `break`, execution "falls through" to the next case. Fall-through is intentional when multiple cases share the same logic: `case 1: case 2: console.log("1 or 2"); break`. Always comment intentional fall-through.*

22. **What is the difference between `while` and `do...while` loops? When would you choose one over the other?**

    *Key points: `while` checks condition before executing (0+ iterations). `do...while` executes once then checks condition (1+ iterations). Use `do...while` when the body must run at least once (e.g., user input validation loop).*

23. **How do `try`, `catch`, and `finally` work together? Does `finally` always execute?**

    *Key points: `try` — code that may throw. `catch(err)` — handles the error. `finally` — always executes (after try/catch, even on return/throw). Use `finally` for cleanup (closing connections, clearing timers). Exception: `finally` doesn't run on `process.exit()` or browser tab close.*

### Functions

24. **What is the difference between a function declaration and a function expression? How does hoisting affect each?**

    *Key points: Function declaration: `function foo() {}` — hoisted (can call before definition). Function expression: `const foo = function() {}` — not hoisted (TDZ with `let`/`const`). Use declarations for named functions, expressions for callbacks and conditional assignments.*

25. **Explain arrow functions. How do they differ from regular functions in terms of `this`, `arguments`, and `new`?**

    *Key points: Arrow functions: no own `this` (inherits from enclosing scope), no `arguments` object, cannot be used as constructors (no `new`), cannot use `super`. Use arrows for callbacks and methods that need lexical `this`. Use regular functions for object methods and constructors.*

26. **What are default parameters? How do they differ from checking `||` inside the function body?**

    *Key points: `function greet(name = "Guest") {}` — default applies only when argument is `undefined`. `name || "Guest"` — applies for any falsy value (`""`, `0`, `false`). Default parameters are more precise and evaluated at call time (new default each call).*

27. **What are rest parameters (`...args`)? How do they differ from the `arguments` object?**

    *Key points: Rest parameters collect remaining arguments into a real array. `arguments` is array-like (not a real array), includes all parameters, not available in arrow functions. Rest parameters are preferred: real array, only captures unnamed params, works in arrows.*

28. **What is an IIFE (Immediately Invoked Function Expression)? What problems does it solve?**

    *Key points: `(function() { ... })()` or `(() => { ... })()`. Creates a new scope to avoid polluting the global scope. Used for: module pattern (before ES6 modules), data privacy, avoiding variable collisions. Largely replaced by `let`/`const` block scope and ES6 modules.*

29. **Explain the difference between passing by value and passing by reference in JavaScript function arguments.**

    *Key points: Primitives are passed by value (copy). Objects are passed by reference (the reference value is copied — "pass by sharing"). Reassigning a parameter inside the function doesn't affect the original. Mutating an object's properties does affect the original.*

30. **What is a callback function? Give an example of synchronous and asynchronous callbacks.**

    *Key points: A callback is a function passed as an argument to another function. Synchronous: `arr.forEach(callback)`. Asynchronous: `setTimeout(callback, 1000)`, `fs.readFile(path, callback)`. Callbacks enable asynchronous programming but can lead to "callback hell."*

31. **What is a higher-order function? Give three examples from JavaScript's built-in methods.**

    *Key points: A function that takes a function as argument or returns a function. Examples: `arr.map(fn)`, `arr.filter(fn)`, `arr.reduce(fn)`, `setTimeout(fn)`, `Function.prototype.bind()`. Higher-order functions enable functional programming patterns.*

32. **What is function currying? How does it differ from partial application?**

    *Key points: Currying transforms a function with multiple arguments into a sequence of nested functions each taking one argument: `f(a,b,c) → f(a)(b)(c)`. Partial application fixes some arguments: `const add5 = add.bind(null, 5)`. Currying is a specific form of partial application.*

### Scope & Hoisting

33. **What is the difference between global scope, function scope, and block scope?**

    *Key points: Global scope — accessible everywhere (window/global). Function scope — variables declared with `var` inside a function. Block scope — variables declared with `let`/`const` inside `{}`. `var` ignores block scope (except functions). Prefer block scope with `let`/`const`.*

34. **Explain hoisting. How does `var` hoisting differ from `let`/`const` hoisting?**

    *Key points: All declarations are hoisted (moved to top of scope). `var` — hoisted and initialized as `undefined` (accessible before declaration). `let`/`const` — hoisted but not initialized (TDZ — accessing throws ReferenceError). Function declarations are hoisted entirely.*

35. **What is the scope chain? How does JavaScript resolve variable lookups?**

    *Key points: Each execution context has a scope chain — references to outer scopes. When resolving a variable, JS looks in current scope, then parent scope, then grandparent, up to global scope. This is lexical scoping (based on where functions are defined, not called).*

36. **What is a closure? Give a practical example (e.g., creating a private counter).**

    *Key points: A closure is a function that retains access to its outer scope even after the outer function has returned. Example: `function createCounter() { let count = 0; return () => ++count; }`. The inner function "closes over" `count`, creating private state.*

37. **How do closures interact with loops? Explain the classic `var` in a loop problem and its solutions.**

    *Key points: With `var`, all closures share the same variable (final value). Fixes: use `let` (creates new binding per iteration), IIFE (`(function(i) {...})(i)`), or `.bind()`. `let` is the modern solution.*

38. **What is a memory leak caused by closures? How can you avoid it?**

    *Key points: Closures keep references to outer variables, preventing GC. Leak: large data captured in a closure that lives longer than needed. Avoid: nullify references when done, avoid capturing large objects unnecessarily, use weak references (`WeakMap`).*

### `this` Keyword

39. **What determines the value of `this` in a regular function? List the four binding rules.**

    *Key points: 1) Default binding — `this` is `window` (non-strict) or `undefined` (strict). 2) Implicit binding — `obj.method()` → `this` is `obj`. 3) Explicit binding — `.call()`, `.apply()`, `.bind()`. 4) `new` binding — `this` is the new instance. Arrow functions ignore these rules.*

40. **How does `this` behave differently in arrow functions compared to regular functions?**

    *Key points: Arrow functions don't have their own `this` — they inherit `this` from the enclosing lexical scope. Cannot be changed with `call`/`apply`/`bind`. Useful for: callbacks, event handlers, setTimeout where you want the outer `this`.*

41. **What do `call()`, `apply()`, and `bind()` do? When would you use each?**

    *Key points: `call(thisArg, arg1, arg2)` — invokes function with given `this` and arguments. `apply(thisArg, [args])` — same but arguments as array. `bind(thisArg)` — returns new function with bound `this`. Use `call` for individual args, `apply` for array args, `bind` for creating bound functions.*

42. **What happens to `this` when you extract a method from an object? How do you fix it?**

    *Key points: Extracting `const fn = obj.method` loses the implicit binding — `this` becomes `undefined` (strict) or `window`. Fix: `.bind(obj)`, arrow function wrapper `() => obj.method()`, or store as arrow function in the object.*

43. **How does `this` work in event handlers? How do arrow functions help?**

    *Key points: In regular function event handlers, `this` refers to the element that fired the event. Arrow functions inherit `this` from the enclosing scope (usually the class instance). Use regular functions when you need the element, arrows when you need the class context.*

### Arrays

44. **What is the difference between `map()` and `forEach()`? When would you choose one over the other?**

    *Key points: `map()` returns a new array (transformation). `forEach()` returns `undefined` (side effects). Use `map` for data transformation, `forEach` for side effects (logging, DOM updates). `map` is chainable; `forEach` is not.*

45. **Explain `filter()`, `find()`, and `some()`. When would you use each?**

    *Key points: `filter()` returns array of all matching elements. `find()` returns first matching element (or `undefined`). `some()` returns boolean if any match. Use: `filter` for multiple results, `find` for single item lookup, `some` for existence check.*

46. **How does `reduce()` work? Give an example of summing numbers and grouping objects.**

    *Key points: `reduce((acc, curr) => newAcc, initialValue)`. Sum: `[1,2,3].reduce((a,b) => a+b, 0)` → `6`. Group: `items.reduce((acc, item) => { (acc[item.category] ??= []).push(item); return acc; }, {})`.*

47. **What is the difference between `slice()` and `splice()`? Which one mutates the original array?**

    *Key points: `slice(start, end)` — returns new array (doesn't mutate). `splice(start, deleteCount, ...items)` — mutates original (removes/replaces elements). `slice` for copying/subarrays, `splice` for in-place modifications.*

48. **How do you remove duplicates from an array? Give at least two approaches.**

    *Key points: 1) `[...new Set(arr)]` (simple, primitives only). 2) `arr.filter((item, i) => arr.indexOf(item) === i)` (first occurrence). 3) `arr.reduce((acc, item) => acc.includes(item) ? acc : [...acc, item], [])`. Set is most concise.*

49. **What is the difference between `Array.isArray()` and `typeof` for checking arrays?**

    *Key points: `typeof []` → `"object"` (arrays are objects). `Array.isArray([])` → `true`. Always use `Array.isArray()` to check arrays. `typeof` cannot distinguish arrays from objects.*

50. **Explain the spread operator with arrays. How do you shallow copy, merge, and add elements?**

    *Key points: Copy: `const copy = [...arr]`. Merge: `const merged = [...arr1, ...arr2]`. Add: `const added = [...arr, newItem]` (end), `[newItem, ...arr]` (start). Spread creates a shallow copy — nested objects are still referenced.*

51. **What is array destructuring? How do you swap variables, skip elements, and use default values?**

    *Key points: `const [first, second] = arr`. Swap: `[a, b] = [b, a]`. Skip: `const [first, , third] = arr`. Defaults: `const [a = 1] = []`. Rest: `const [first, ...rest] = arr`. Destructuring is concise and expressive.*

52. **How does `sort()` work? Why does `[1, 10, 2].sort()` give unexpected results? How do you fix it?**

    *Key points: `sort()` converts elements to strings and compares UTF-16 code units. `[1, 10, 2].sort()` → `[1, 10, 2]` (string order). Fix: provide comparator `arr.sort((a, b) => a - b)` for ascending, `b - a` for descending.*

### Objects & Prototypes

53. **What are the different ways to create an object in JavaScript?**

    *Key points: Object literal: `const obj = { key: 'value' }`. Constructor: `new Object()`. `Object.create(proto)`. Class: `new MyClass()`. Factory function: `function createObj() { return { ... } }`. Object literal is most common.*

54. **Explain the difference between dot notation and bracket notation for property access.**

    *Key points: Dot: `obj.key` — static, must be valid identifier. Bracket: `obj["key"]` — dynamic, any string. Use dot for known property names, bracket for dynamic keys (`obj[variable]`), keys with spaces/special chars, or computed properties.*

55. **What is the difference between `Object.keys()`, `Object.values()`, and `Object.entries()`?**

    *Key points: `Object.keys(obj)` — array of own enumerable property names. `Object.values(obj)` — array of own enumerable values. `Object.entries(obj)` — array of `[key, value]` pairs. All ignore prototype chain. Useful for iteration and transformation.*

56. **How does prototypal inheritance work? Explain the prototype chain.**

    *Key points: Every object has an internal `[[Prototype]]` link to another object (its prototype). Property lookup walks up the chain until found or `null`. `Object.prototype` is at the top. `Array.prototype` → `Object.prototype` → `null`. This is prototypal inheritance.*

57. **What is the difference between `__proto__` and `prototype`?**

    *Key points: `__proto__` is the actual prototype link of an instance (deprecated, use `Object.getPrototypeOf()`). `prototype` is a property on constructor functions, assigned as `__proto__` of instances created with `new`. `Function.prototype` is the prototype object shared by all functions.*

58. **How does `new` work internally? What are the four steps it performs?**

    *Key points: 1) Creates a new empty object. 2) Sets the object's prototype to the constructor's `prototype`. 3) Calls the constructor with `this` bound to the new object. 4) Returns the new object (or the constructor's return if it's an object).*

59. **What is `Object.create()`? How does it differ from using a constructor function?**

    *Key points: `Object.create(proto, propertiesObject)` creates a new object with the specified prototype. Unlike `new`, it doesn't run a constructor. Useful for: setting up prototype chains without constructors, creating objects with `null` prototype (`Object.create(null)`).*

60. **Explain property descriptors (`writable`, `enumerable`, `configurable`). How do `Object.freeze()` and `Object.seal()` differ?**

    *Key points: `writable` — can value be changed. `enumerable` — appears in `for...in`/`Object.keys()`. `configurable` — can descriptor be changed or property deleted. `Object.freeze()` — makes all properties non-writable and non-configurable (immutable). `Object.seal()` — makes non-configurable (can't add/delete, but can modify values).*

### ES6+ Features

61. **What are template literals? How do they improve string interpolation and multi-line strings?**

    *Key points: Template literals use backticks: `` `Hello ${name}` ``. Benefits: string interpolation with `${}`, multi-line strings (preserves newlines), tagged templates for custom processing. More readable than concatenation.*

62. **Explain object destructuring. How do you rename variables, set defaults, and handle nested objects?**

    *Key points: `const { name, age } = obj`. Rename: `const { name: userName } = obj`. Defaults: `const { name = "Guest" } = obj`. Nested: `const { address: { street } } = obj`. Rest: `const { name, ...rest } = obj`.*

63. **What is the difference between `Map` and `Object`? When would you use a `Map`?**

    *Key points: `Map` — any key type (objects, functions), maintains insertion order, `size` property, better performance for frequent add/delete. `Object` — string/symbol keys only, inherits prototype keys. Use `Map` for dynamic key-value pairs, frequent iteration, non-string keys.*

64. **What is the difference between `Set` and `Array`? When would you use a `Set`?**

    *Key points: `Set` — unique values only, no index access, `has()` is O(1). `Array` — ordered, allows duplicates, index access. Use `Set` for uniqueness checks, deduplication, and membership testing. Use `Array` for ordered collections with duplicates.*

65. **What are `Symbols`? How are they used as object keys?**

    *Key points: `Symbol` is a unique, immutable primitive. `const sym = Symbol("description")`. Used as object keys to avoid name collisions: `obj[sym] = value`. Not enumerable in `for...in`/`Object.keys()`. Well-known symbols: `Symbol.iterator`, `Symbol.toStringTag`.*

66. **What is `BigInt`? When would you need it over regular `Number`?**

    *Key points: `BigInt` represents integers beyond `Number.MAX_SAFE_INTEGER` (2^53 - 1). Created with `n` suffix: `9007199254740993n`. Use for: large IDs, cryptographic operations, financial calculations requiring arbitrary precision. Cannot mix with regular `Number` in operations.*

67. **What are numeric separators (`_`) and why are they useful?**

    *Key points: Underscores in numeric literals for readability: `1_000_000`, `0xFF_FF_FF`. No runtime impact — purely visual. Improves readability of large numbers, binary/hex values, and currency amounts.*

68. **Explain `String.prototype.replaceAll()`. How does it differ from `replace()` with a global regex?**

    *Key points: `replaceAll(search, replacement)` replaces all occurrences without regex. `replace(/pattern/g, replacement)` requires global regex. `replaceAll` is simpler for string replacements, avoids regex escaping issues. Both replace all matches.*

### Classes (ES6)

69. **How do ES6 classes differ from constructor functions? Are they truly a new inheritance model?**

    *Key points: Classes are syntactic sugar over prototype-based inheritance. Differences: `class` syntax is cleaner, methods are non-enumerable, classes run in strict mode, cannot be called without `new`. Under the hood, it's still prototypal inheritance — not a new model.*

70. **What is the purpose of `super()` in a class constructor? Why must it be called before accessing `this`?**

    *Key points: `super()` calls the parent class constructor, setting up the prototype chain and initializing `this`. Must be called before `this` because the parent constructor creates the instance. Forgetting `super()` throws ReferenceError. Also used for calling parent methods: `super.method()`.*

71. **What are static methods and properties? How do they differ from instance members?**

    *Key points: Static members belong to the class itself, not instances. `static create() { return new this() }`. Called as `MyClass.create()`, not `instance.create()`. Used for factory methods, utility functions, singleton instances.*

72. **What are getters and setters? Give an example with validation.**

    *Key points: `get prop()` and `set prop(value)` define computed properties. Example: `set age(value) { if (value < 0) throw Error("Invalid age"); this._age = value; }`. Allows validation, computed values, and encapsulation with property-like syntax.*

73. **What are private fields (`#`)? How do they differ from TypeScript's `private` keyword?**

    *Key points: `#privateField` is truly private at runtime (enforced by the engine). TypeScript's `private` is only a compile-time check — accessible at runtime. Private fields cannot be accessed or modified outside the class. Only available in modern JS (ES2022+).*

74. **What is the difference between `extends` and `implements` (in TypeScript context)?**

    *Key points: `extends` — class inheritance (shares implementation). `implements` — TypeScript-only, ensures a class conforms to an interface (no code reuse). A class can `extend` one class and `implement` multiple interfaces.*

---

## 🟡 MID-LEVEL (Intermediate)

### Asynchronous JavaScript

75. **Explain the JavaScript event loop. How do the call stack, task queue, and microtask queue interact?**

    *Key points: Event loop continuously checks: if call stack is empty, process microtask queue (all of it), then process one macrotask from task queue. Call stack — synchronous execution. Microtask queue — Promise `.then()`, `queueMicrotask()`. Task queue — `setTimeout`, DOM events, I/O.*

76. **What is the difference between a microtask (Promise `.then()`) and a macrotask (`setTimeout`)? Which runs first?**

    *Key points: Microtasks run before macrotasks, after each macrotask. Microtask queue is fully drained before next macrotask. Example: `setTimeout(() => console.log(1), 0); Promise.resolve().then(() => console.log(2))` → logs `2`, then `1`.*

77. **What are the three states of a Promise? Can a Promise change from "fulfilled" to "rejected"?**

    *Key points: States: `pending` (initial), `fulfilled` (resolved successfully), `rejected` (failed). A Promise is settled once — it cannot transition from fulfilled to rejected or vice versa. This is a key design guarantee.*

78. **Explain Promise chaining. How does returning a value vs returning a Promise affect the chain?**

    *Key points: `.then()` returns a new Promise. Returning a value wraps it in resolved Promise. Returning a Promise flattens it (no nesting). Returning a rejected Promise skips to next `.catch()`. This enables sequential async operations without nesting.*

79. **What is the difference between `Promise.all()`, `Promise.allSettled()`, `Promise.race()`, and `Promise.any()`? When would you use each?**

    *Key points: `Promise.all()` — resolves when all resolve, rejects if any rejects (all-or-nothing). `Promise.allSettled()` — resolves when all settle (each result has status). `Promise.race()` — settles with first settled Promise (resolve or reject). `Promise.any()` — resolves with first fulfilled, rejects if all reject. Use: `all` for parallel dependencies, `allSettled` for independent tasks, `race` for timeouts, `any` for first success.*

80. **How does `async/await` work? What does an `async` function always return?**

    *Key points: `async` function always returns a Promise. `await` pauses execution until the Promise settles (non-blocking). Under the hood, the compiler generates a state machine (similar to generators). `async/await` is syntactic sugar over Promises.*

81. **What happens when you forget `await` before a Promise? What value do you get?**

    *Key points: Without `await`, you get the Promise object itself, not the resolved value. The Promise still executes, but you can't access the result. This can cause race conditions or unexpected behavior. Always `await` Promises unless you intentionally want the Promise.*

82. **Explain the difference between sequential and parallel execution with `async/await`. When would you use `Promise.all()`?**

    *Key points: Sequential: `const a = await fetchA(); const b = await fetchB()` — waits for A before starting B. Parallel: `const [a, b] = await Promise.all([fetchA(), fetchB()])` — runs concurrently. Use `Promise.all()` for independent async operations to improve performance.*

83. **How do you handle errors in `async/await`? Compare `try/catch` with `.catch()`.**

    *Key points: `try/catch` — familiar syntax, catches all errors in the block. `.catch()` — Promise-style, can be chained. Both work; `try/catch` is more readable for complex logic. Mixing both is fine: `await promise.catch(handleError)` for specific error handling.*

84. **What is the "callback hell" problem? How do Promises and `async/await` solve it?**

    *Key points: Callback hell is deeply nested callbacks (pyramid of doom), making code hard to read and error-prone. Promises flatten with chaining (`.then().then().catch()`). `async/await` makes async code look synchronous (linear, readable).*

85. **How do you cancel an in-flight Promise or `async` function? (AbortController pattern)**

    *Key points: Use `AbortController`: `const controller = new AbortController(); fetch(url, { signal: controller.signal }); controller.abort()`. The `signal` propagates to the async operation. For custom async: check `signal.aborted` periodically. Promises themselves are not cancellable — AbortController is the standard pattern.*

86. **What is promisification? How do you convert a callback-based function to return a Promise?**

    *Key points: Promisification wraps a callback-based function to return a Promise. Example: `const fsReadFile = util.promisify(fs.readFile)` or manually: `new Promise((resolve, reject) => { fs.readFile(path, (err, data) => err ? reject(err) : resolve(data)) })`. Node.js has `util.promisify()` built-in.*

87. **Explain the race condition problem with `async/await` and how to fix it with a cancellation flag.**

    *Key points: Race condition: starting a new async operation while a previous one is still running — both may update the same state. Fix: use a cancellation flag `let cancelled = false; if (cancelled) return;` or use `AbortController`. Also: debouncing, or ignoring stale responses.*

88. **What is `for await...of`? When would you use it?**

    *Key points: `for await (const item of asyncIterable)` iterates over async iterables (`IAsyncEnumerable`). Use for: streaming data (fetch responses with `response.body.getReader()`), paginated API results, processing async generators. Requires async context.*

### Error Handling

89. **What are the built-in Error types in JavaScript? (SyntaxError, TypeError, ReferenceError, RangeError)**

    *Key points: `Error` — base type. `SyntaxError` — invalid syntax (eval, JSON.parse). `TypeError` — wrong type (calling non-function, accessing null property). `ReferenceError` — accessing undeclared variable. `RangeError` — value out of range (array length). `URIError` — malformed URI.*

90. **How do you create a custom error class? Why would you extend `Error` instead of throwing a plain object?**

    *Key points: `class ValidationError extends Error { constructor(message) { super(message); this.name = 'ValidationError'; } }`. Extending `Error` preserves stack trace, `instanceof` checking, and consistent error handling. Plain objects lack these debugging benefits.*

91. **What is the difference between `throw` and `return` for error handling?**

    *Key points: `throw` — unwinds the stack, can be caught by `try/catch` up the call chain. `return` — normal flow, caller must check return value. Use `throw` for exceptional/unexpected errors. Use `return` (or Result pattern) for expected failure cases (validation, not-found).*

92. **Explain the "Result" pattern (returning `{ success, data, error }`). When is it better than throwing?**

    *Key points: Result pattern returns an object indicating success/failure instead of throwing. Better when: errors are expected (validation, API calls), you want type safety, you want to avoid try/catch overhead, or errors are part of normal flow. Common in functional programming.*

93. **What is an unhandled Promise rejection? How do you catch it globally?**

    *Key points: A Promise that rejects without a `.catch()` handler. In browsers: `window.addEventListener('unhandledrejection', handler)`. In Node.js: `process.on('unhandledRejection', handler)`. Always handle Promise rejections to avoid silent failures.*

94. **What information does the `error.stack` property provide? How is it useful for debugging?**

    *Key points: `error.stack` provides a stack trace — function calls, file paths, and line numbers leading to the error. Useful for: identifying exact error location, understanding call chain, debugging production issues. Non-standard but widely supported.*

### Modules

95. **What is the difference between ES6 modules (`import`/`export`) and CommonJS (`require`/`module.exports`)?**

    *Key points: ES6 — static (imports are hoisted, tree-shakeable), async loading, named/default exports. CommonJS — dynamic (can `require` conditionally), synchronous, `module.exports`. ES6 is standard for browsers; CommonJS is Node.js default. Interop exists with `.mjs`/`.cjs` extensions.*

96. **What is the difference between named exports and default exports? When would you use each?**

    *Key points: Named: `export const foo = ...` — import with exact name `{ foo }`. Default: `export default ...` — import with any name. Use named for multiple exports from a module (utilities). Use default for the main export of a module (a single class/function).*

97. **What is a barrel file (index.js pattern)? How does it simplify imports?**

    *Key points: A barrel file re-exports from multiple modules: `export { a } from './a'; export { b } from './b'`. Simplifies imports: `import { a, b } from './components'` instead of multiple paths. Reduces import depth and centralizes module boundaries.*

98. **What are dynamic imports (`import()`) and how do they enable code splitting?**

    *Key points: `import('./module.js').then(mod => ...)` loads modules on demand. Enables code splitting — bundlers create separate chunks loaded only when needed. Reduces initial bundle size. Works with `async/await`: `const mod = await import('./module.js')`.*

99. **What is tree-shaking? Why does it work better with ES6 modules than CommonJS?**

    *Key points: Tree-shaking removes unused exports during bundling. Works with ES6 modules because imports/exports are static (known at compile time). CommonJS is dynamic (`require` can be conditional), making dead code elimination harder. ES6 enables smaller bundles.*

100. **How do you handle circular dependencies in JavaScript modules?**

     *Key points: Circular dependencies occur when A imports B and B imports A. Solutions: restructure code (extract shared logic to a third module), use dynamic imports (`import()`), use dependency injection. ES6 modules handle circular deps better than CommonJS (hoisted bindings).*

### Regular Expressions

101. **What is the difference between `test()` and `exec()` on a RegExp object?**

     *Key points: `test(string)` returns boolean (whether match exists). `exec(string)` returns match object (full match, groups, index, input) or `null`. Use `test` for existence checks, `exec` for extracting matched content. Both maintain `lastIndex` with global flag.*

102. **What do the `g`, `i`, `m`, and `s` flags do in regular expressions?**

     *Key points: `g` — global (find all matches, not just first). `i` — case-insensitive. `m` — multiline (`^`/`$` match line boundaries). `s` — dotAll (`.` matches newlines). Combine: `/pattern/gim`.*

103. **Explain the difference between greedy and lazy quantifiers (`*` vs `*?`).**

     *Key points: Greedy (`*`, `+`, `?`, `{n,m}`) matches as much as possible. Lazy (`*?`, `+?`, `??`, `{n,m}?`) matches as little as possible. Example: `/<.*>/` on `<div>text</div>` matches the whole string. `/<.*?>/` matches `<div>` only.*

104. **What are capturing groups and non-capturing groups? When would you use `(?:)`?**

     *Key points: Capturing groups `(pattern)` store matched content (accessible via `$1`, `$2`). Non-capturing groups `(?:pattern)` group without storing. Use non-capturing for grouping only (alternation, quantifiers) when you don't need the captured value.*

105. **What are named capturing groups (`(?<name>)`)? How do you access them?**

     *Key points: `(?<year>\d{4})` creates a named group. Access via `match.groups.year` or `$<year>` in replacement strings. More readable than numeric indices. Supported in modern JS (ES2018).*

106. **What is the difference between positive lookahead (`(?=)`) and negative lookahead (`(?!)`)?**

     *Key points: Positive lookahead `x(?=y)` — matches `x` only if followed by `y`. Negative lookahead `x(?!y)` — matches `x` only if not followed by `y`. Lookaheads don't consume characters. Also: lookbehinds `(?<=y)x` and `(?<!y)x` (ES2018).*

107. **How do you escape special characters in a regex when the pattern comes from user input?**

     *Key points: Escape with `string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')`. Never pass user input directly to `new RegExp(input)` without escaping — it can cause regex injection or unexpected behavior.*

### Advanced Patterns

108. **Explain memoization. When would you use it? What are the trade-offs (memory vs performance)?**

     *Key points: Memoization caches function results by arguments. Use for: expensive pure functions (recursive Fibonacci, complex calculations), repeated calls with same inputs. Trade-offs: memory usage (cache grows), cache invalidation, not suitable for impure functions.*

109. **What is the difference between debouncing and throttling? Give a real-world use case for each.**

     *Key points: Debouncing — delays execution until after a pause (search input, auto-save). Throttling — limits execution rate (scroll handler, resize handler). Debounce: "wait until idle." Throttle: "at most once per interval."*

110. **How do you implement a simple debounce function? What happens to the `this` context?**

     *Key points: `function debounce(fn, delay) { let timer; return function(...args) { clearTimeout(timer); timer = setTimeout(() => fn.apply(this, args), delay); }; }`. The arrow function preserves `this` from the wrapper. The wrapper uses `function` to capture `this` from the call site.*

111. **Explain function composition (`compose` vs `pipe`). How does it differ from chaining?**

     *Key points: `compose(f, g)(x)` = `f(g(x))` (right-to-left). `pipe(f, g)(x)` = `g(f(x))` (left-to-right). Chaining is method-based (`obj.method1().method2()`). Composition is function-based. Composition is more flexible (works with any functions, not just methods).*

112. **What is the Observer pattern? How does it relate to event emitters?**

     *Key points: Observer pattern: subject maintains a list of observers, notifies them of state changes. Event emitters (Node.js `EventEmitter`, DOM events) implement this pattern. `emitter.on('event', handler)` subscribes, `emitter.emit('event', data)` notifies.*

113. **What is the Singleton pattern? How do you implement it in JavaScript?**

     *Key points: Singleton ensures only one instance exists. Implementation: `const singleton = { method() {} }` (object literal), or class with static instance: `class Singleton { static getInstance() { if (!this._instance) this._instance = new this(); return this._instance; } }`. Module-level singletons are natural in ES6 modules.*

114. **What is the Factory pattern? When would you use it over a constructor or class?**

     *Key points: Factory function returns an object without `new`. Use when: creation logic is complex, you need to return different types based on input, you want to avoid `new` (forgetting it causes bugs), or you need closures for private state.*

### Performance

115. **What is the difference between deep copy and shallow copy? How do you create each?**

     *Key points: Shallow copy copies top-level properties (nested objects are shared). Methods: spread `{...obj}`, `Object.assign()`, `Array.from()`. Deep copy copies all levels. Methods: `structuredClone(obj)` (modern), `JSON.parse(JSON.stringify(obj))` (limited — no functions, undefined, circular refs), or libraries (lodash `cloneDeep`).*

116. **How does `structuredClone()` work? When was it introduced and what are its limitations?**

     *Key points: `structuredClone(value)` creates a deep copy using the structured clone algorithm (same as `postMessage`). Introduced in ES2022. Limitations: cannot clone functions, DOM nodes, Error objects, WeakMaps/WeakSets, RegExp (cloned but loses lastIndex), Symbols, prototype chain is not preserved.*

117. **What causes layout thrashing in the browser? How do you batch DOM reads and writes?**

     *Key points: Layout thrashing occurs when JS repeatedly reads then writes to the DOM, forcing synchronous layout recalculations. Fix: batch reads together, then batch writes. Use `requestAnimationFrame` for writes. Libraries like FastDOM automate this. Example: read all sizes first, then apply all changes.*

118. **What is the difference between `requestAnimationFrame()` and `setTimeout()` for animations?**

     *Key points: `requestAnimationFrame` runs before the next paint (syncs with refresh rate, 60fps), pauses when tab is hidden (saves resources). `setTimeout` runs after specified delay regardless of paint cycle, may cause jank. Always use `requestAnimationFrame` for visual updates.*

119. **How do you measure performance of a function? (`performance.now()`, `console.time()`)**

     *Key points: `console.time('label')` / `console.timeEnd('label')` — simple timing. `performance.now()` — high-resolution timestamp (sub-millisecond). `performance.mark()` / `performance.measure()` — User Timing API for detailed profiling. Use `performance.now()` for precise measurements.*

120. **What is the performance impact of `try/catch`? When should you avoid it in hot paths?**

     *Key points: `try/catch` has minimal overhead when no exception is thrown (V8 optimizes it). Avoid in hot paths only if the catch block is frequently hit. The real cost is in the exception itself (stack unwinding). Use `try/catch` for exceptional cases, not control flow.*

121. **How do you optimize loops for large arrays? When is `for` faster than `forEach` or `reduce`?**

     *Key points: Traditional `for` loop is fastest (minimal overhead). `for...of` is slightly slower. `forEach`/`map`/`reduce` have function call overhead. For large arrays (>100k), use `for` or `while`. For readability with small/medium arrays, use array methods. Avoid creating intermediate arrays in hot paths.*

122. **What is the difference between `Map` and plain objects for frequent property lookups?**

     *Key points: `Map` is optimized for frequent additions/deletions and has O(1) lookup. Objects have prototype chain overhead and integer-key optimization issues. For dynamic keys and frequent lookups, `Map` is faster. For static keys and small sets, objects are fine.*

### Testing

123. **What is the difference between unit tests, integration tests, and end-to-end tests?**

     *Key points: Unit tests — test individual functions/modules in isolation (mocked dependencies). Integration tests — test how modules work together (real database, API). End-to-end tests — test the full system from user perspective (Cypress, Playwright). Unit tests are fastest; E2E are most comprehensive.*

124. **Explain the AAA pattern (Arrange, Act, Assert) in testing.**

     *Key points: Arrange — set up test data and conditions. Act — execute the function being tested. Assert — verify the result matches expectations. Example: `const arr = [3, 1, 2]; arr.sort(); expect(arr).toEqual([1, 2, 3])`. AAA makes tests readable and structured.*

125. **What is the difference between a mock, a stub, and a spy?**

     *Key points: Mock — fake object with pre-programmed behavior and expectations (verify interactions). Stub — provides canned answers (no verification). Spy — wraps a real function, recording calls and arguments. Jest: `jest.fn()` (mock), `jest.spyOn()` (spy).*

126. **How do you test asynchronous code with Jest? (Promises, async/await, callbacks)**

     *Key points: Return a Promise: `return fetchData().then(data => expect(data).toBeDefined())`. Use `async/await`: `const data = await fetchData(); expect(data).toBeDefined()`. Use `.resolves`/`.rejects`: `expect(fetchData()).resolves.toBeDefined()`. For callbacks: use `done` callback or `jest.useFakeTimers()`.*

127. **What is code coverage? What metrics does it measure (statements, branches, functions, lines)?**

     *Key points: Code coverage measures how much of the code is executed during tests. Metrics: statement coverage (each statement), branch coverage (each if/else path), function coverage (each function called), line coverage (each line). 100% coverage doesn't mean bug-free.*

128. **What is TDD (Test-Driven Development)? Explain the Red-Green-Refactor cycle.**

     *Key points: TDD: write failing test first (Red), write minimal code to pass (Green), improve code quality (Refactor). Benefits: better design, test coverage, confidence in refactoring. Cycle: Red → Green → Refactor → repeat.*

### `this` & Binding (Advanced)

129. **What happens to `this` when a method is passed as a callback? How do you preserve the correct context?**

     *Key points: `const fn = obj.method; fn()` loses `this` binding (becomes `undefined` in strict mode). Preserve with: `.bind(obj)`, arrow function `() => obj.method()`, or store method as arrow function. In React class components, bind in constructor or use class property arrows.*

130. **How does `bind()` work internally? Does it create a new function every time?**

     *Key points: `bind()` returns a new function with bound `this` and optional preset arguments. Yes, it creates a new function every call. The new function has `[[BoundThis]]` and `[[BoundArgs]]` internal slots. Avoid calling `bind` in hot paths or render loops (use class property arrows instead).*

131. **What is the difference between hard binding (`.bind()`) and soft binding (arrow function wrapper)?**

     *Key points: Hard binding (`.bind()`) permanently binds `this` — cannot be overridden by `call`/`apply`. Soft binding (arrow function `() => obj.method()`) creates a new function each time but allows the inner method's `this` to be rebound. Arrow functions are more flexible for dynamic contexts.*

### Closures (Advanced)

132. **How do closures enable data privacy? Give an example of the module pattern.**

     *Key points: Closures create private state inaccessible from outside. Module pattern: `const counter = (() => { let count = 0; return { increment: () => ++count, getCount: () => count }; })()`. `count` is private — only accessible through returned methods.*

133. **How do closures interact with `let` in a `for` loop? Why does this fix the classic closure-in-loop bug?**

     *Key points: `let` creates a new binding for each iteration (block-scoped). Each closure captures a different `count` variable. With `var`, all closures share the same variable. `let`'s per-iteration binding is the modern fix for the classic closure-in-loop bug.*

134. **What is a "closure scope" in the debugger? How do you inspect captured variables?**

     *Key points: In browser DevTools, the "Closure" scope shows variables captured by closures. Inspect by: setting breakpoints inside the closure, checking the Scope panel. Variables appear under "Closure" (or "Closure (name)"). Useful for debugging closure-related bugs.*

### Event Loop (Advanced)

135. **What is the difference between the microtask queue and the task queue? Give examples of operations that go into each.**

     *Key points: Microtask queue: Promise `.then()`/`.catch()`/`.finally()`, `queueMicrotask()`, `MutationObserver`, `process.nextTick()` (Node.js). Task queue (macrotask): `setTimeout`, `setInterval`, `setImmediate`, I/O callbacks, DOM events. Microtasks run before the next macrotask.*

136. **Given `console.log(1); setTimeout(() => console.log(2), 0); Promise.resolve().then(() => console.log(3)); console.log(4);` — what is the output and why?**

     *Key points: Output: `1, 4, 3, 2`. Explanation: `1` and `4` are synchronous. Promise `.then()` is a microtask — runs after current script but before next macrotask. `setTimeout(0)` is a macrotask — runs last. Microtask queue is drained before task queue.*

137. **What is `queueMicrotask()`? When would you use it over `setTimeout(fn, 0)`?**

     *Key points: `queueMicrotask(fn)` queues a microtask. Use over `setTimeout(fn, 0)` when: you need to run before the next macrotask (before rendering), you want higher priority, or you're batching state updates. Microtasks are faster and more predictable than `setTimeout(0)`.*

138. **How does `process.nextTick()` (Node.js) differ from `Promise.then()` in the event loop?**

     *Key points: `process.nextTick()` runs before Promise microtasks in Node.js (it has its own "nextTick queue" that's checked first). `Promise.then()` runs in the microtask queue. `nextTick` has the highest priority. Use `nextTick` sparingly — it can starve the event loop.*

---

## 💡 BONUS: Problem-Solving & Behavioral

139. **How would you implement a deep clone function that handles circular references?**

     *Key points: Use a `WeakMap` to track visited objects. When encountering an already-cloned object, return the cached clone. Recursively copy properties. Handle arrays, objects, Date, RegExp, Map, Set. `structuredClone()` handles this natively in modern environments.*

140. **How would you implement `Promise.all()` from scratch?**

     *Key points: Return a new Promise. Track results array and completed count. For each input Promise, `.then(result => { results[index] = result; completed++; if (completed === total) resolve(results); }).catch(reject)`. Handle empty array (resolve immediately).*

141. **How would you implement `Array.prototype.map()` from scratch?**

     *Key points: `function myMap(arr, callback) { const result = []; for (let i = 0; i < arr.length; i++) { result.push(callback(arr[i], i, arr)); } return result; }`. Handle sparse arrays, `thisArg`, and edge cases (empty array).*

142. **How would you implement a simple event emitter with `on`, `off`, and `emit`?**

     *Key points: Store events in a `Map<string, Set<Function>>`. `on(event, handler)` — add to set. `off(event, handler)` — remove from set. `emit(event, ...args)` — iterate handlers and call with args. Return unsubscribe function from `on` for convenience.*

143. **How would you flatten a nested array of arbitrary depth?**

     *Key points: Recursive: `function flatten(arr) { return arr.reduce((acc, item) => acc.concat(Array.isArray(item) ? flatten(item) : item), []); }`. Iterative: use a stack. Built-in: `arr.flat(Infinity)` (ES2019).*

144. **How would you group an array of objects by a property?**

     *Key points: `function groupBy(arr, key) { return arr.reduce((acc, item) => { const k = typeof key === 'function' ? key(item) : item[key]; (acc[k] ??= []).push(item); return acc; }, {}); }`. ES2024 has `Object.groupBy(arr, callback)` built-in.*

145. **How would you implement a rate limiter that limits concurrent async operations?**

     *Key points: Use a queue and a counter. Track running count. When a task is added: if running < limit, execute immediately; otherwise, enqueue. When a task completes, dequeue and execute next. Use Promises for the queue. Similar to `p-limit` library.*

146. **Describe a time you debugged a tricky JavaScript bug. What tools and techniques did you use?**

     *Key points: Tools: browser DevTools (breakpoints, watch, scope), `console.log` strategically, `debugger` statement, React DevTools, Redux DevTools, network tab. Techniques: binary search on code, reproduce consistently, isolate the minimal case, check assumptions, rubber duck debugging.*

147. **How do you stay up-to-date with new JavaScript features? Which recent feature excited you most?**

     *Key points: Follow: TC39 proposals (GitHub), MDN Web Docs, JavaScript Weekly newsletter, blogs (2ality, V8 blog), conferences (JSConf). Recent exciting features: Temporal API (modern date/time), `Array.groupBy()`, `Promise.withResolvers()`, decorators, `using` declarations (explicit resource management).*

148. **How would you approach migrating a large codebase from ES5 to ES6+?**

     *Key points: 1) Set up transpilation (Babel). 2) Add linting (ESLint with ES6 rules). 3) Incrementally replace: `var` → `const`/`let`, function expressions → arrows (carefully with `this`), `for` loops → array methods, callbacks → Promises/async-await. 4) Add tests. 5) Use codemods for automated transformations. 6) Update module system to ES6 imports.*
