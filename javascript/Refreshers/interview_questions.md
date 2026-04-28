# JavaScript Core - Technical Interview Questions

## 🟢 JUNIOR LEVEL (Fundamentals)

### Variables, Data Types & Type Coercion

1. What are the differences between `var`, `let`, and `const`? When would you use each?
2. What are the 7 primitive types in JavaScript? How do they differ from reference types?
3. Explain the difference between `null` and `undefined`. When would you use each intentionally?
4. What is the difference between `==` and `===`? Why is `===` generally preferred?
5. What are the 6 falsy values in JavaScript? Give an example of a common bug caused by falsy coercion.
6. Explain explicit vs implicit type coercion. Give examples of when implicit coercion can be surprising.
7. What is `NaN`? How do you check if a value is `NaN`? Why doesn't `NaN === NaN` work?
8. What is the difference between `typeof null` and `typeof undefined`? Why is `typeof null` considered a bug?
9. Explain the difference between `undefined` and "not defined" (ReferenceError).
10. What is the Temporal Dead Zone (TDZ) in relation to `let` and `const`?

### Operators & Expressions

11. What is the difference between `++x` and `x++`?
12. Explain short-circuit evaluation with `&&` and `||`. Give a practical example of each.
13. What is the nullish coalescing operator (`??`)? How does it differ from `||`?
14. What is optional chaining (`?.`) and how does it prevent errors?
15. Explain the spread operator (`...`) for arrays and objects. How does it differ from `Object.assign()`?
16. What is the ternary operator? When is it appropriate vs when should you use `if/else`?
17. What is the difference between `&&=` and `??=` logical assignment operators?

### Control Flow

18. What is the difference between `for...in` and `for...of`? When would you use each?
19. How does `break` differ from `continue` in loops? Give a practical example of each.
20. What is a labeled statement in JavaScript? When would you use `break outerLoop`?
21. Explain the `switch` statement. What happens if you forget a `break`? When is fall-through intentional?
22. What is the difference between `while` and `do...while` loops? When would you choose one over the other?
23. How do `try`, `catch`, and `finally` work together? Does `finally` always execute?

### Functions

24. What is the difference between a function declaration and a function expression? How does hoisting affect each?
25. Explain arrow functions. How do they differ from regular functions in terms of `this`, `arguments`, and `new`?
26. What are default parameters? How do they differ from checking `||` inside the function body?
27. What are rest parameters (`...args`)? How do they differ from the `arguments` object?
28. What is an IIFE (Immediately Invoked Function Expression)? What problems does it solve?
29. Explain the difference between passing by value and passing by reference in JavaScript function arguments.
30. What is a callback function? Give an example of synchronous and asynchronous callbacks.
31. What is a higher-order function? Give three examples from JavaScript's built-in methods.
32. What is function currying? How does it differ from partial application?

### Scope & Hoisting

33. What is the difference between global scope, function scope, and block scope?
34. Explain hoisting. How does `var` hoisting differ from `let`/`const` hoisting?
35. What is the scope chain? How does JavaScript resolve variable lookups?
36. What is a closure? Give a practical example (e.g., creating a private counter).
37. How do closures interact with loops? Explain the classic `var` in a loop problem and its solutions.
38. What is a memory leak caused by closures? How can you avoid it?

### `this` Keyword

39. What determines the value of `this` in a regular function? List the four binding rules.
40. How does `this` behave differently in arrow functions compared to regular functions?
41. What do `call()`, `apply()`, and `bind()` do? When would you use each?
42. What happens to `this` when you extract a method from an object? How do you fix it?
43. How does `this` work in event handlers? How do arrow functions help?

### Arrays

44. What is the difference between `map()` and `forEach()`? When would you choose one over the other?
45. Explain `filter()`, `find()`, and `some()`. When would you use each?
46. How does `reduce()` work? Give an example of summing numbers and grouping objects.
47. What is the difference between `slice()` and `splice()`? Which one mutates the original array?
48. How do you remove duplicates from an array? Give at least two approaches.
49. What is the difference between `Array.isArray()` and `typeof` for checking arrays?
50. Explain the spread operator with arrays. How do you shallow copy, merge, and add elements?
51. What is array destructuring? How do you swap variables, skip elements, and use default values?
52. How does `sort()` work? Why does `[1, 10, 2].sort()` give unexpected results? How do you fix it?

### Objects & Prototypes

53. What are the different ways to create an object in JavaScript?
54. Explain the difference between dot notation and bracket notation for property access.
55. What is the difference between `Object.keys()`, `Object.values()`, and `Object.entries()`?
56. How does prototypal inheritance work? Explain the prototype chain.
57. What is the difference between `__proto__` and `prototype`?
58. How does `new` work internally? What are the four steps it performs?
59. What is `Object.create()`? How does it differ from using a constructor function?
60. Explain property descriptors (`writable`, `enumerable`, `configurable`). How do `Object.freeze()` and `Object.seal()` differ?

### ES6+ Features

61. What are template literals? How do they improve string interpolation and multi-line strings?
62. Explain object destructuring. How do you rename variables, set defaults, and handle nested objects?
63. What is the difference between `Map` and `Object`? When would you use a `Map`?
64. What is the difference between `Set` and `Array`? When would you use a `Set`?
65. What are `Symbols`? How are they used as object keys?
66. What is `BigInt`? When would you need it over regular `Number`?
67. What are numeric separators (`_`) and why are they useful?
68. Explain `String.prototype.replaceAll()`. How does it differ from `replace()` with a global regex?

### Classes (ES6)

69. How do ES6 classes differ from constructor functions? Are they truly a new inheritance model?
70. What is the purpose of `super()` in a class constructor? Why must it be called before accessing `this`?
71. What are static methods and properties? How do they differ from instance members?
72. What are getters and setters? Give an example with validation.
73. What are private fields (`#`)? How do they differ from TypeScript's `private` keyword?
74. What is the difference between `extends` and `implements` (in TypeScript context)?

---

## 🟡 MID-LEVEL (Intermediate)

### Asynchronous JavaScript

75. Explain the JavaScript event loop. How do the call stack, task queue, and microtask queue interact?
76. What is the difference between a microtask (Promise `.then()`) and a macrotask (`setTimeout`)? Which runs first?
77. What are the three states of a Promise? Can a Promise change from "fulfilled" to "rejected"?
78. Explain Promise chaining. How does returning a value vs returning a Promise affect the chain?
79. What is the difference between `Promise.all()`, `Promise.allSettled()`, `Promise.race()`, and `Promise.any()`? When would you use each?
80. How does `async/await` work? What does an `async` function always return?
81. What happens when you forget `await` before a Promise? What value do you get?
82. Explain the difference between sequential and parallel execution with `async/await`. When would you use `Promise.all()`?
83. How do you handle errors in `async/await`? Compare `try/catch` with `.catch()`.
84. What is the "callback hell" problem? How do Promises and `async/await` solve it?
85. How do you cancel an in-flight Promise or `async` function? (AbortController pattern)
86. What is promisification? How do you convert a callback-based function to return a Promise?
87. Explain the race condition problem with `async/await` and how to fix it with a cancellation flag.
88. What is `for await...of`? When would you use it?

### Error Handling

89. What are the built-in Error types in JavaScript? (SyntaxError, TypeError, ReferenceError, RangeError)
90. How do you create a custom error class? Why would you extend `Error` instead of throwing a plain object?
91. What is the difference between `throw` and `return` for error handling?
92. Explain the "Result" pattern (returning `{ success, data, error }`). When is it better than throwing?
93. What is an unhandled Promise rejection? How do you catch it globally?
94. What information does the `error.stack` property provide? How is it useful for debugging?

### Modules

95. What is the difference between ES6 modules (`import`/`export`) and CommonJS (`require`/`module.exports`)?
96. What is the difference between named exports and default exports? When would you use each?
97. What is a barrel file (index.js pattern)? How does it simplify imports?
98. What are dynamic imports (`import()`) and how do they enable code splitting?
99. What is tree-shaking? Why does it work better with ES6 modules than CommonJS?
100. How do you handle circular dependencies in JavaScript modules?

### Regular Expressions

101. What is the difference between `test()` and `exec()` on a RegExp object?
102. What do the `g`, `i`, `m`, and `s` flags do in regular expressions?
103. Explain the difference between greedy and lazy quantifiers (`*` vs `*?`).
104. What are capturing groups and non-capturing groups? When would you use `(?:)`?
105. What are named capturing groups (`(?<name>)`)? How do you access them?
106. What is the difference between positive lookahead (`(?=)`) and negative lookahead (`(?!)`)?
107. How do you escape special characters in a regex when the pattern comes from user input?

### Advanced Patterns

108. Explain memoization. When would you use it? What are the trade-offs (memory vs performance)?
109. What is the difference between debouncing and throttling? Give a real-world use case for each.
110. How do you implement a simple debounce function? What happens to the `this` context?
111. Explain function composition (`compose` vs `pipe`). How does it differ from chaining?
112. What is the Observer pattern? How does it relate to event emitters?
113. What is the Singleton pattern? How do you implement it in JavaScript?
114. What is the Factory pattern? When would you use it over a constructor or class?

### Performance

115. What is the difference between deep copy and shallow copy? How do you create each?
116. How does `structuredClone()` work? When was it introduced and what are its limitations?
117. What causes layout thrashing in the browser? How do you batch DOM reads and writes?
118. What is the difference between `requestAnimationFrame()` and `setTimeout()` for animations?
119. How do you measure performance of a function? (`performance.now()`, `console.time()`)
120. What is the performance impact of `try/catch`? When should you avoid it in hot paths?
121. How do you optimize loops for large arrays? When is `for` faster than `forEach` or `reduce`?
122. What is the difference between `Map` and plain objects for frequent property lookups?

### Testing

123. What is the difference between unit tests, integration tests, and end-to-end tests?
124. Explain the AAA pattern (Arrange, Act, Assert) in testing.
125. What is the difference between a mock, a stub, and a spy?
126. How do you test asynchronous code with Jest? (Promises, async/await, callbacks)
127. What is code coverage? What metrics does it measure (statements, branches, functions, lines)?
128. What is TDD (Test-Driven Development)? Explain the Red-Green-Refactor cycle.

### `this` & Binding (Advanced)

129. What happens to `this` when a method is passed as a callback? How do you preserve the correct context?
130. How does `bind()` work internally? Does it create a new function every time?
131. What is the difference between hard binding (`.bind()`) and soft binding (arrow function wrapper)?

### Closures (Advanced)

132. How do closures enable data privacy? Give an example of the module pattern.
133. How do closures interact with `let` in a `for` loop? Why does this fix the classic closure-in-loop bug?
134. What is a "closure scope" in the debugger? How do you inspect captured variables?

### Event Loop (Advanced)

135. What is the difference between the microtask queue and the task queue? Give examples of operations that go into each.
136. Given `console.log(1); setTimeout(() => console.log(2), 0); Promise.resolve().then(() => console.log(3)); console.log(4);` — what is the output and why?
137. What is `queueMicrotask()`? When would you use it over `setTimeout(fn, 0)`?
138. How does `process.nextTick()` (Node.js) differ from `Promise.then()` in the event loop?

---

## 💡 BONUS: Problem-Solving & Behavioral

139. How would you implement a deep clone function that handles circular references?
140. How would you implement `Promise.all()` from scratch?
141. How would you implement `Array.prototype.map()` from scratch?
142. How would you implement a simple event emitter with `on`, `off`, and `emit`?
143. How would you flatten a nested array of arbitrary depth?
144. How would you group an array of objects by a property?
145. How would you implement a rate limiter that limits concurrent async operations?
146. Describe a time you debugged a tricky JavaScript bug. What tools and techniques did you use?
147. How do you stay up-to-date with new JavaScript features? Which recent feature excited you most?
148. How would you approach migrating a large codebase from ES5 to ES6+?
