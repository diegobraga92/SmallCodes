# React - Technical Interview Questions

## 🟢 JUNIOR LEVEL (Fundamentals)

### JSX & Rendering

1. **What is JSX? Why isn't it HTML? How does the compiler transform it?**

   *Key points: JSX is a syntax extension for JavaScript that looks like HTML. It's not HTML — it's syntactic sugar for `React.createElement()` calls. The compiler (Babel, TypeScript) transforms `<div className="x">Hello</div>` into `React.createElement('div', { className: 'x' }, 'Hello')`.*

2. **What are the rules of JSX? (single root element, closing tags, className vs class, etc.)**

   *Key points: Single root element (or Fragment). All tags must close (self-closing or paired). `className` instead of `class`. `htmlFor` instead of `for`. Attributes are camelCased (`onClick`, `tabIndex`). Expressions in `{}`, not `""`.*

3. **What is the difference between an element and a component in React?**

   *Key points: An element is a plain object describing what to render (`React.createElement` output). A component is a function or class that returns elements. Elements are immutable; components can have state and lifecycle. Components are reusable; elements are snapshots.*

4. **How do you render a list in React? Why do you need a `key` prop? What happens if you use the index as a key?**

   *Key points: Use `array.map(item => <Component key={item.id} />)`. `key` helps React identify which items changed/added/removed (reconciliation). Index as key is problematic when items are reordered, added, or removed — causes incorrect state mapping and performance issues.*

5. **What is the difference between `{}` and `{{}}` in JSX?**

   *Key points: `{}` is a JavaScript expression. `{{}}` is an object literal inside a JSX expression — the outer `{}` is the JSX expression, the inner `{}` is the object. Used for inline styles: `style={{ color: 'red' }}`.*

6. **How do you conditionally render content in React? Give at least three approaches.**

   *Key points: 1) `&&` operator: `{isLoggedIn && <Dashboard />}`. 2) Ternary: `{isLoggedIn ? <Dashboard /> : <Login />}`. 3) `if/else` outside JSX: `if (loading) return <Spinner />`. 4) IIFE inside JSX. 5) Variable assignment.*

7. **What is the difference between `if/else` and the ternary operator in JSX?**

   *Key points: `if/else` is a statement — cannot be used inside JSX `{}`. Ternary is an expression — can be used inline. Use `if/else` outside JSX for complex logic, ternary inside JSX for simple conditions.*

8. **How do you render `null`, `undefined`, and `false` in JSX? Which values produce no output?**

   *Key points: `null`, `undefined`, `false`, and `true` render nothing (no output). `0` renders "0" (pitfall with `&&`). `""` renders nothing. `NaN` renders "NaN". Be careful with `{count && <Component />}` when `count` is `0`.*

9. **What is a Fragment (`<>...</>`)? Why would you use it instead of a `<div>`?**

   *Key points: Fragment groups multiple elements without adding a DOM node. Use instead of `<div>` to avoid breaking layouts (CSS Grid/Flexbox), reducing DOM nesting, and avoiding invalid HTML (e.g., `<td>` inside `<tr>`). Short syntax `<>` or `<React.Fragment>` with `key`.*

10. **How do you add inline styles in JSX? Why are property names camelCased?**

    *Key points: `style={{ backgroundColor: 'red', fontSize: 16 }}`. CamelCase because JSX expressions are JavaScript — `background-color` is invalid JS (hyphen is subtraction). React auto-adds `px` to numeric values (except some properties).*

### Components & Props

11. **What is the difference between a functional component and a class component?**

    *Key points: Functional components are plain functions returning JSX (simpler, hooks). Class components extend `React.Component` with `render()` method (more verbose, lifecycle methods). Modern React prefers functional components with hooks.*

12. **What are props? Are they mutable? How do you pass data from parent to child?**

    *Key points: Props are read-only data passed from parent to child. They are immutable — a component should never modify its own props. Passed as HTML-like attributes: `<Child name="John" age={25} />`. Accessed as `props.name` or destructured.*

13. **What is props drilling? What problems does it cause?**

    *Key points: Props drilling is passing props through multiple intermediate components that don't use them, just to reach a deeply nested child. Problems: verbose code, hard to maintain, components become coupled, refactoring is painful. Solutions: Context API, component composition, state management.*

14. **What is the `children` prop? How do you use it for component composition?**

    *Key points: `children` is a special prop representing content between opening/closing tags. Enables composition: `<Card><p>Content</p></Card>` — Card renders `{children}`. More flexible than passing content as a regular prop. Can be any renderable value.*

15. **How do you set default values for props? (defaultProps vs default parameters)**

    *Key points: Class components: `Component.defaultProps = { name: 'Guest' }`. Functional: default parameters `function Greeting({ name = 'Guest' })`. Default parameters are preferred in modern React (simpler, no extra API).*

16. **What is the difference between controlled and uncontrolled components? Give an example of each.**

    *Key points: Controlled: React controls the value via state (`<input value={val} onChange={e => setVal(e.target.value)} />`). Uncontrolled: DOM manages its own state (`<input ref={inputRef} />`, access via ref). Controlled gives more control (validation, instant feedback).*

17. **What is a pure component? How does `React.memo()` work?**

    *Key points: Pure component only re-renders when props/state change (shallow comparison). `React.memo(Component)` wraps a functional component with memoization. If props haven't changed (shallow equality), it skips re-rendering. Use for expensive components that re-render often with same props.*

18. **What is the difference between `React.createElement()` and JSX?**

    *Key points: `React.createElement(type, props, ...children)` is the underlying API. JSX is syntactic sugar that compiles to `createElement` calls. JSX is more readable. You rarely use `createElement` directly unless building abstractions.*

### State & Lifecycle

19. **What is state in React? How does it differ from props?**

    *Key points: State is internal, mutable data managed by a component. Props are external, immutable data passed from parent. State changes trigger re-renders. Props are read-only. State is private to the component.*

20. **What does the `useState` hook return? How do you update state?**

    *Key points: `useState(initialValue)` returns an array `[state, setState]`. `setState(newValue)` updates state and triggers re-render. Can also pass a function: `setState(prev => prev + 1)`. State updates are asynchronous (batched).*

21. **Why shouldn't you mutate state directly? What happens if you do?**

    *Key points: Direct mutation (`state.count = 5`) doesn't trigger re-render because React uses reference equality to detect changes. Always use the setter function. For objects/arrays, create new copies: `setState({ ...state, count: 5 })`.*

22. **What is the difference between `useState` with a value vs a function updater?**

    *Key points: Value: `setCount(count + 1)` — uses current closure value (can be stale). Function updater: `setCount(prev => prev + 1)` — always gets latest state. Use function updater when new state depends on previous state, especially in rapid updates.*

23. **What is the `useEffect` hook? What is its purpose?**

    *Key points: `useEffect(callback, deps)` runs side effects after render. Purpose: data fetching, subscriptions, DOM manipulation, timers, logging. Runs after paint (non-blocking). Can return a cleanup function.*

24. **What is the dependency array in `useEffect`? What happens if you omit it, pass `[]`, or pass variables?**

    *Key points: Omit: runs after every render. `[]`: runs once on mount (like `componentDidMount`). `[var]`: runs when `var` changes. Missing deps cause stale closures; including unnecessary deps causes extra runs. The linter (`exhaustive-deps`) helps catch issues.*

25. **How do you clean up side effects in `useEffect`? Give an example (e.g., event listener, subscription).**

    *Key points: Return a cleanup function from the effect: `useEffect(() => { const sub = source.subscribe(handler); return () => sub.unsubscribe(); }, [])`. Cleanup runs on unmount and before re-running the effect. Prevents memory leaks.*

26. **What is the component lifecycle in a functional component with hooks?**

    *Key points: Mount: function body runs → `useEffect` (after paint). Update: function body runs → cleanup of previous effect → new effect. Unmount: cleanup runs. `useLayoutEffect` runs synchronously after DOM mutations but before paint.*

27. **What is the `useRef` hook? How does it differ from `useState`?**

    *Key points: `useRef(initialValue)` returns a mutable object `{ current: value }`. Unlike `useState`, changing `ref.current` does NOT trigger re-render. Use refs for: DOM references, storing mutable values that shouldn't cause re-renders, previous values.*

28. **How do you access a DOM element with `useRef`?**

    *Key points: `const inputRef = useRef(null); <input ref={inputRef} />`. Access via `inputRef.current` after mount. Use for: focusing, measuring, integrating with non-React libraries. Don't overuse — prefer state-driven approaches.*

### Event Handling

29. **How do event handlers work in React? How do they differ from native DOM events?**

    *Key points: React uses synthetic events (wraps native events). Handlers are attached via props (`onClick`, `onChange`), not `addEventListener`. React uses event delegation (single listener on root). Handlers receive a `SyntheticEvent` object.*

30. **What is synthetic events in React? Why does React use them?**

    *Key points: SyntheticEvent is a cross-browser wrapper around native events. Provides consistent API across browsers. React uses event delegation (one listener at root) for performance. In React 17+, events are delegated to the root DOM container, not `document`.*

31. **How do you pass arguments to an event handler? What is the difference between `onClick={handleClick}` and `onClick={() => handleClick(id)}`?**

    *Key points: `onClick={handleClick}` passes the event automatically. `onClick={() => handleClick(id)}` creates a new function each render (can cause unnecessary re-renders with `React.memo`). Alternative: `onClick={handleClick}`, define `handleClick = (id) => (event) => {...}`.*

32. **How do you prevent default behavior in React? (e.g., form submission)**

    *Key points: Call `event.preventDefault()` in the handler. React passes the synthetic event. Example: `form onSubmit={e => { e.preventDefault(); submitData(); }}`. Same as native DOM but using React's synthetic event.*

33. **How do you stop event propagation in React?**

    *Key points: Call `event.stopPropagation()` to prevent the event from bubbling up. React's synthetic events still use native propagation under the hood. `event.nativeEvent.stopImmediatePropagation()` stops other handlers on the same element.*

34. **What is event pooling in React 16? Why was it removed in React 17+?**

    *Key points: React 16 pooled synthetic events (reused the event object) — accessing `event.target` asynchronously required `event.persist()`. React 17+ removed pooling — events behave like native events. Simplifies code and avoids a common pitfall.*

### Forms

35. **How do you handle form inputs in React? What is a controlled input?**

    *Key points: Controlled input: value is controlled by React state. `<input value={val} onChange={e => setVal(e.target.value)} />`. Every keystroke updates state, which updates the input value. Gives React full control over the input.*

36. **How do you handle multiple inputs with a single change handler?**

    *Key points: Use `name` attribute on inputs. `const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })`. Each input has a unique `name` matching the state key. Reduces boilerplate.*

37. **How do you handle form submission? What is `event.preventDefault()`?**

    *Key points: `form onSubmit={handleSubmit}`. Call `e.preventDefault()` to prevent page reload. Then process form data (validation, API call). Return `false` also works but `preventDefault()` is preferred.*

38. **What is the difference between `value` and `defaultValue` in an input?**

    *Key points: `value` makes the input controlled (React manages value). `defaultValue` sets the initial value for uncontrolled inputs. Changing `defaultValue` after mount has no effect. Use `value` for controlled, `defaultValue` for uncontrolled.*

39. **How do you handle textarea, select, checkbox, and radio inputs in React?**

    *Key points: Textarea: `<textarea value={val} onChange={...} />` (value prop, not children). Select: `<select value={val} onChange={...}><option value="a">A</option></select>`. Checkbox: `checked={bool}` not `value`. Radio: `checked={selected === 'opt'}`.*

40. **How do you implement form validation in React?**

    *Key points: Validate on change, on blur, or on submit. Store errors in state. Show error messages conditionally. Use `onBlur` for field-level validation, `onSubmit` for full validation. Libraries: Formik, React Hook Form, or custom validation functions.*

### Lists & Keys

41. **Why does React need a `key` prop when rendering lists?**

    *Key points: Keys help React identify which items changed, were added, or removed during reconciliation. Without keys, React re-renders all items (inefficient). With keys, React can reuse DOM nodes and preserve component state.*

42. **What happens if you use array index as a key? When is it acceptable?**

    *Key points: Index as key causes issues when items are reordered, added at the beginning, or removed — React may reuse wrong DOM nodes, causing state bugs (e.g., wrong checkbox checked). Acceptable only for static lists that never change order.*

43. **What is a stable key? How do you generate unique keys?**

    *Key points: A stable key is unique and doesn't change between renders. Use database IDs, UUIDs, or a combination of fields. Avoid random values (causes unnecessary re-renders). `crypto.randomUUID()` or libraries like `nanoid` for generated IDs.*

44. **How does React use keys for reconciliation?**

    *Key points: React compares keys of elements in the old and new virtual DOM. Matching keys = reuse DOM node. Different key = unmount old, mount new. Keys should be stable, unique, and predictable. React uses keys to optimize list updates.*

### Conditional Rendering

45. **What are the different ways to conditionally render in React?**

    *Key points: 1) `&&` operator. 2) Ternary `? :`. 3) `if/else` outside JSX. 4) IIFE. 5) Variable assignment. 6) Early return. 7) Switch statement. 8) Enum object mapping.*

46. **Why can't you use `if/else` inside JSX? How do you work around it?**

    *Key points: `if/else` is a statement, not an expression — JSX only accepts expressions in `{}`. Workaround: use ternary, `&&`, or extract logic to a function/variable outside JSX.*

47. **What is the `&&` pattern for conditional rendering? What are its pitfalls with falsy values like `0`?**

    *Key points: `{condition && <Component />}` renders Component when condition is truthy. Pitfall: `{count && <Component />}` renders "0" when count is 0 (falsy but renderable). Fix: `{count > 0 && <Component />}` or `{!!count && <Component />}`.*

48. **What is the ternary pattern vs `&&`? When would you choose each?**

    *Key points: Ternary: `{condition ? <A /> : <B />}` — both branches. `&&`: `{condition && <A />}` — show/hide only. Use ternary when you need an else branch. Use `&&` for simple show/hide without an alternative.*

---

## 🟡 MID-LEVEL (Intermediate)

### Hooks Deep Dive

49. **What are the rules of hooks? Why must hooks be called at the top level and not inside conditions/loops?**

    *Key points: 1) Only call hooks at the top level (not in conditions, loops, nested functions). 2) Only call hooks from React functions (components or custom hooks). Reason: React relies on the order of hook calls to associate state with the correct `useState`/`useEffect` call. Conditional hooks break this order.*

50. **How does React know which state belongs to which `useState` call? (hooks linked list)**

    *Key points: React maintains a linked list of hook nodes per component. Each `useState` call creates a node in order. On re-render, React iterates the list in the same order. This is why hook order must be stable — breaking the order corrupts the state mapping.*

51. **What is the `useCallback` hook? When would you use it? What problem does it solve?**

    *Key points: `useCallback(fn, deps)` returns a memoized callback that only changes when deps change. Solves: preventing unnecessary re-renders of child components wrapped in `React.memo` that receive callback props. Without it, a new function is created every render.*

52. **What is the `useMemo` hook? How does it differ from `useCallback`?**

    *Key points: `useMemo(() => value, deps)` memoizes a computed value. `useCallback` memoizes a function. `useMemo(() => fn, deps)` is equivalent to `useCallback(fn, deps)`. Use `useMemo` for expensive calculations, `useCallback` for stable function references.*

53. **What is the difference between `useMemo` and `useEffect`? When would you use each?**

    *Key points: `useMemo` runs synchronously during render (computes a value). `useEffect` runs after render (side effects). Use `useMemo` for derived data (filtered list, computed total). Use `useEffect` for data fetching, subscriptions, DOM manipulation.*

54. **What is the `useReducer` hook? When would you choose it over `useState`?**

    *Key points: `useReducer(reducer, initialState)` returns `[state, dispatch]`. Choose over `useState` when: state logic is complex (multiple sub-values), next state depends on previous state, or you have multiple state transitions. Similar to Redux but local.*

55. **What is the `useContext` hook? How does it work with `React.createContext()`?**

    *Key points: `useContext(MyContext)` returns the current context value. Works with `React.createContext(defaultValue)` and `<MyContext.Provider value={...}>`. Components using `useContext` re-render when the context value changes. Simpler than Context.Consumer.*

56. **What is the `useImperativeHandle` hook? When would you use it?**

    *Key points: `useImperativeHandle(ref, () => ({ focus, reset }))` customizes the instance value exposed to parent refs. Use with `forwardRef`. Use when: you need to expose imperative methods (focus, scrollTo, reset) to parent components. Rarely needed.*

57. **What is the `useLayoutEffect` hook? How does it differ from `useEffect`?**

    *Key points: `useLayoutEffect` runs synchronously after DOM mutations but before the browser paints. `useEffect` runs asynchronously after paint. Use `useLayoutEffect` for: measuring DOM, animations, preventing visual flicker. Prefer `useEffect` by default.*

58. **What is the `useDebugValue` hook? How is it useful for custom hooks?**

    *Key points: `useDebugValue(value)` displays a label for custom hooks in React DevTools. Helps debugging custom hooks by showing their internal state. Can use a formatter: `useDebugValue(date, d => d.toDateString())`. Only used in custom hooks.*

59. **What is the `useTransition` hook? How does it help with urgent vs non-urgent updates?**

    *Key points: `useTransition()` returns `[isPending, startTransition]`. `startTransition` marks state updates as non-urgent (can be interrupted). Urgent updates (typing) take priority over non-urgent (filtering list). Improves perceived performance by keeping UI responsive.*

60. **What is the `useDeferredValue` hook? How does it differ from `useTransition`?**

    *Key points: `useDeferredValue(value)` returns a deferred version of the value that lags behind. Similar to `useTransition` but works with props/values, not state setters. Use when you can't control the state update (e.g., value comes from props).*

61. **What is the `useId` hook? What problem does it solve for accessibility?**

    *Key points: `useId()` generates unique IDs for accessibility attributes (`aria-describedby`, `htmlFor`). Solves: generating unique, stable IDs on both server and client (hydration-safe). Prevents ID collisions in SSR. No more `Math.random()` or `uuid` for a11y IDs.*

62. **What is the `useSyncExternalStore` hook? When would you use it?**

    *Key points: `useSyncExternalStore(subscribe, getSnapshot)` reads from external stores (Redux, Zustand, etc.) in a way that's safe for concurrent rendering. Use when building libraries that need to integrate with React's concurrent features. Ensures tear-free reads.*

### Custom Hooks

63. **What is a custom hook? How do you create one?**

    *Key points: A custom hook is a JavaScript function that starts with `use` and may call other hooks. Extracts reusable logic from components. Example: `function useWindowSize() { const [size, setSize] = useState({ width, height }); useEffect(() => { ... }, []); return size; }`.*

64. **What are the naming conventions for custom hooks? Why must they start with `use`?**

    *Key points: Custom hooks must start with `use` (e.g., `useFetch`, `useDebounce`). This is required for the React hooks lint rules to work correctly. The linter (`eslint-plugin-react-hooks`) uses the `use` prefix to detect violations of hooks rules.*

65. **How do you share logic between components without custom hooks? (HOCs, render props)**

    *Key points: Higher-Order Components (HOC): `withAuth(Component)` wraps a component to add auth logic. Render props: `<DataProvider render={data => <Component data={data} />} />`. Custom hooks are preferred (simpler, no wrapper hell, no naming collisions).*

66. **How do you create a custom hook for fetching data? How do you handle loading, error, and success states?**

    *Key points: `function useFetch(url) { const [data, setData] = useState(null); const [loading, setLoading] = useState(true); const [error, setError] = useState(null); useEffect(() => { fetch(url).then(res => res.json()).then(setData).catch(setError).finally(() => setLoading(false)); }, [url]); return { data, loading, error }; }`. Handle cleanup with AbortController.*

67. **How do you create a custom hook for debouncing input?**

    *Key points: `function useDebounce(value, delay) { const [debounced, setDebounced] = useState(value); useEffect(() => { const timer = setTimeout(() => setDebounced(value), delay); return () => clearTimeout(timer); }, [value, delay]); return debounced; }`. Used for search inputs to avoid excessive API calls.*

68. **How do you create a custom hook for `localStorage` synchronization?**

    *Key points: `function useLocalStorage(key, initial) { const [value, setValue] = useState(() => JSON.parse(localStorage.getItem(key)) ?? initial); useEffect(() => { localStorage.setItem(key, JSON.stringify(value)); }, [key, value]); return [value, setValue]; }`. Handle SSR and JSON parse errors.*

69. **How do you create a custom hook for media queries?**

    *Key points: `function useMediaQuery(query) { const [matches, setMatches] = useState(window.matchMedia(query).matches); useEffect(() => { const mq = window.matchMedia(query); const handler = (e) => setMatches(e.matches); mq.addEventListener('change', handler); return () => mq.removeEventListener('change', handler); }, [query]); return matches; }`. Used for responsive components.*

70. **How do you create a custom hook for `useInterval`?**

    *Key points: `function useInterval(callback, delay) { const savedCallback = useRef(callback); useEffect(() => { savedCallback.current = callback; }); useEffect(() => { if (delay !== null) { const id = setInterval(() => savedCallback.current(), delay); return () => clearInterval(id); } }, [delay]); }`. Avoids closure issues with stale callbacks.*

71. **How do you create a custom hook for `usePrevious`?**

    *Key points: `function usePrevious(value) { const ref = useRef(); useEffect(() => { ref.current = value; }); return ref.current; }`. Returns the previous value from the last render. Useful for comparing current vs previous props/state.*

72. **How do you test a custom hook? (`renderHook` from React Testing Library)**

    *Key points: `const { result } = renderHook(() => useCustomHook()); expect(result.current).toBe(expected)`. `rerender` to test updates. `waitForNextUpdate` for async hooks. `renderHook` creates a test component that runs the hook.*

### Context API

73. **What is the Context API? What problem does it solve?**

    *Key points: Context provides a way to pass data through the component tree without props drilling. Solves: sharing global data (theme, user, locale) across many components without passing props through every level. `React.createContext()` + `<Provider>` + `useContext()`.*

74. **How do you create a context? How do you provide and consume it?**

    *Key points: Create: `const ThemeContext = React.createContext('light')`. Provide: `<ThemeContext.Provider value="dark"><App /></ThemeContext.Provider>`. Consume: `const theme = useContext(ThemeContext)`. Or with `<ThemeContext.Consumer>{value => ...}</ThemeContext.Consumer>`.*

75. **What is the difference between `useContext` and Context.Consumer?**

    *Key points: `useContext` is a hook (simpler, used in functional components). Context.Consumer uses render props (works in class components). `useContext` is preferred — less nesting, more readable. Context.Consumer is only needed in class components.*

76. **What are the performance implications of Context? How does it cause unnecessary re-renders?**

    *Key points: When context value changes, ALL consumers re-render, even if they only use a part of the value. This can cause performance issues in large trees. Unlike props, you can't use `React.memo` to prevent context-triggered re-renders.*

77. **How do you optimize Context to prevent re-renders? (memoization, splitting contexts)**

    *Key points: 1) Split contexts (separate `ThemeContext` and `UserContext`). 2) Memoize context value with `useMemo`. 3) Split providers to different levels. 4) Use libraries like `use-context-selector` for fine-grained subscriptions. 5) Keep context values small.*

78. **When should you use Context vs prop drilling vs a state management library?**

    *Key points: Use Context for low-frequency, app-wide data (theme, locale, auth). Use prop drilling for simple, shallow hierarchies. Use state management (Redux, Zustand) for complex state logic, frequent updates, or when you need devtools/middleware.*

79. **How do you create a context with a custom hook for type safety?**

    *Key points: `const AuthContext = createContext<AuthContextType | undefined>(undefined)`. Custom hook: `function useAuth() { const ctx = useContext(AuthContext); if (!ctx) throw new Error('useAuth must be used within AuthProvider'); return ctx; }`. Ensures context is used within provider.*

### Refs & DOM

80. **What is the difference between `useRef` and `createRef`?**

    *Key points: `useRef` is a hook — creates a ref that persists across renders (same object). `createRef` creates a new ref every render — only useful in class components. In functional components, always use `useRef`.*

81. **How do you use refs for DOM manipulation? When is it appropriate vs using state?**

    *Key points: Use refs for: focusing, text selection, media playback, integrating with non-React libraries (D3, charts). Use state for: data that affects rendering. Rule: if it doesn't affect visual output, use refs. If it does, use state.*

82. **What is callback ref? When would you use it?**

    *Key points: Callback ref is a function ref: `<div ref={node => { if (node) measure(node); }} />`. Called when the ref is attached/detached. Use when: you need to run code when the ref changes, or you need dynamic refs (list of items).*

83. **What is ref forwarding? How does `forwardRef` work?**

    *Key points: `forwardRef` lets a parent component pass a ref through to a child's DOM element. `const FancyInput = forwardRef((props, ref) => <input ref={ref} />)`. Parent: `<FancyInput ref={inputRef} />`. Used for reusable component libraries.*

84. **How do you use refs with third-party libraries that need DOM nodes?**

    *Key points: Pass `ref.current` to the library after mount: `useEffect(() => { if (ref.current) { new Chart(ref.current, options); } }, [])`. Clean up on unmount. Use callback refs if the DOM node can change.*

85. **What is the difference between refs and state for values that don't trigger re-renders?**

    *Key points: Refs: mutable, don't trigger re-render, synchronous. State: immutable updates, triggers re-render, async batching. Use refs for: interval IDs, previous values, DOM nodes. Use state for: data displayed in UI.*

### Error Handling

86. **What is an error boundary? How do you create one?**

    *Key points: Error boundary is a class component that catches JavaScript errors in its child tree, logs them, and displays a fallback UI. Uses `static getDerivedStateFromError(error)` and `componentDidCatch(error, info)`. Cannot be implemented with hooks (must be class component).*

87. **What lifecycle methods do error boundaries use? (`componentDidCatch`, `getDerivedStateFromError`)**

    *Key points: `static getDerivedStateFromError(error)` — updates state to show fallback UI (render phase). `componentDidCatch(error, info)` — logs error info (commit phase). Both are class component methods. No hook equivalent exists yet.*

88. **Can error boundaries catch errors in event handlers? Why or why not?**

    *Key points: No — error boundaries don't catch errors in event handlers because they run outside the render cycle. Use regular `try/catch` in event handlers. Error boundaries only catch errors during rendering, lifecycle methods, and constructors.*

89. **How do you handle errors in async operations (e.g., API calls)?**

    *Key points: Use `try/catch` in async functions. Set error state: `setError(error.message)`. Show error UI conditionally. Use error boundaries for rendering errors, not async errors. Libraries like React Query have built-in error handling.*

90. **How do you create a reusable error boundary component?**

    *Key points: `class ErrorBoundary extends React.Component { state = { error: null }; static getDerivedStateFromError(error) { return { error } }; render() { if (this.state.error) return this.props.fallback || <h1>Something went wrong</h1>; return this.props.children; } }`. Use: `<ErrorBoundary fallback={<ErrorUI />}><MyComponent /></ErrorBoundary>`.*

### Performance

91. **What is reconciliation in React? How does the diffing algorithm work?**

    *Key points: Reconciliation is the process of comparing the new virtual DOM with the previous one. The diffing algorithm: 1) Different element types = rebuild tree. 2) Same type = update props. 3) Keys for lists. 4) Recursive comparison. Optimized with O(n) heuristics.*

92. **What is the Fiber architecture? How does it enable concurrent features?**

    *Key points: Fiber is React 16+'s new reconciliation engine. Breaks work into units (fibers) that can be paused, resumed, or aborted. Enables: incremental rendering, concurrent mode, Suspense, and prioritization of urgent updates over non-urgent ones.*

93. **What causes unnecessary re-renders? How do you diagnose them? (React DevTools Profiler)**

    *Key points: Causes: parent re-render, context changes, stale props, inline objects/functions. Diagnose with: React DevTools Profiler (flamegraph, component renders), `console.log('render')`, `React.memo` + `why-did-you-render` library.*

94. **How does `React.memo()` prevent re-renders? What are its limitations?**

    *Key points: `React.memo(Component)` does shallow comparison of props. If props haven't changed, it skips re-rendering. Limitations: shallow comparison only (nested objects still cause re-renders), doesn't prevent context-triggered re-renders, adds comparison overhead.*

95. **How does `useMemo` and `useCallback` help with performance? When can they hurt performance?**

    *Key points: Help by: preventing expensive recalculations, stabilizing references for child memoization. Hurt when: overused (overhead of memoization > computation cost), incorrect dependency arrays (stale values), used for trivial calculations.*

96. **What is code splitting in React? How does `React.lazy()` and `Suspense` work?**

    *Key points: Code splitting splits the bundle into smaller chunks loaded on demand. `const LazyComp = React.lazy(() => import('./Component'))`. Wrapped in `<Suspense fallback={<Loading />}>`. The chunk loads when the component is first rendered.*

97. **What is virtualization? How do libraries like `react-window` improve performance with large lists?**

    *Key points: Virtualization renders only the visible items in a scrollable list (not all items). `react-window` calculates which items are visible based on scroll position and renders only those. Dramatically reduces DOM nodes and memory for large lists (10k+ items).*

98. **What is the `key` prop's role in reconciliation? How does changing a key affect the DOM?**

    *Key points: Keys help React match elements between renders. Changing a key causes React to unmount the old component and mount a new one (state is reset). Stable keys preserve component state. Useful for forcing a component to reset by changing its key.*

99. **What is the difference between `useMemo` and `React.memo`?**

    *Key points: `useMemo` is a hook that memoizes a value within a component. `React.memo` is a HOC that memoizes an entire component (prevents re-render if props haven't changed). `useMemo` optimizes computations; `React.memo` optimizes component rendering.*

100. **How do you profile a React application? What tools do you use?**

    *Key points: React DevTools Profiler (flamegraph, timeline, component renders). `console.profile()` / `console.profileEnd()`. Chrome DevTools Performance tab. `why-did-you-render` library. Lighthouse for production metrics.*

### Styling Approaches

101. **What are the different ways to style React components? (CSS modules, styled-components, Tailwind, inline styles)**

    *Key points: 1) Global CSS (import 'styles.css'). 2) CSS Modules (import styles from './Comp.module.css'). 3) CSS-in-JS (styled-components, Emotion). 4) Utility-first (Tailwind CSS). 5) Inline styles (style={{}}). Each has trade-offs in scoping, performance, and DX.*

102. **What is CSS-in-JS? What are the pros and cons?**

    *Key points: CSS-in-JS writes CSS in JavaScript files (styled-components, Emotion). Pros: scoped styles, dynamic styling, no class name collisions, co-located. Cons: runtime overhead, larger bundle, slower initial render, harder debugging.*

103. **How does styled-components work? What is the `styled` API?**

    *Key points: `styled.button\`color: red;\`` creates a React component with scoped styles. Uses tagged template literals. Generates unique class names. Supports props: `styled.div\`color: ${p => p.color};\``. Works with `ThemeProvider` for theming.*

104. **What is CSS Modules? How does it differ from global CSS?**

    *Key points: CSS Modules automatically scope class names locally (generates unique names like `Button_style_1a2b3`). Imported as `import styles from './Button.module.css'`. Used as `className={styles.btn}`. Prevents global naming conflicts without runtime overhead.*

105. **What is Tailwind CSS with React? How does it compare to component libraries?**

    *Key points: Tailwind provides utility classes (flex, p-4, text-lg) applied directly in JSX. Faster prototyping, consistent design system, small production bundle (purges unused CSS). Less abstraction than component libraries (MUI, Chakra). Good for custom designs.*

### Testing

106. **What is the difference between React Testing Library and Enzyme?**

    *Key points: RTL tests behavior (what users see/do), Enzyme tests implementation (state, props, instance methods). RTL is the recommended approach (React docs). Enzyme is legacy. RTL philosophy: "test how users use it, not how it's implemented."*

107. **What is the guiding philosophy of React Testing Library? ("test how users use it")**

    *Key points: Test components from the user's perspective — query by accessible roles, labels, text. Avoid testing internal state, props, or implementation details. Tests that resemble user interactions are more resilient to refactoring.*

108. **How do you render a component for testing? (`render` from RTL)**

    *Key points: `const { container, getByText, debug } = render(<MyComponent prop="value" />)`. Renders into a virtual DOM (jsdom). Returns helper functions for querying. Automatically cleans up between tests.*

109. **How do you query elements in RTL? (`getBy`, `queryBy`, `findBy` — what's the difference?)**

    *Key points: `getBy*` — throws if not found (assert existence). `queryBy*` — returns null if not found (assert absence). `findBy*` — returns Promise, waits for element to appear (async). Also: `getAllBy`, `queryAllBy`, `findAllBy` for multiple matches.*

110. **How do you simulate user interactions in tests? (`fireEvent` vs `userEvent`)**

    *Key points: `fireEvent` dispatches DOM events directly (lower-level). `userEvent` simulates real user interactions (typing, clicking, tabbing) with multiple events. Prefer `userEvent` — more realistic, catches more bugs. `userEvent.setup()` for async interactions.*

111. **How do you test async behavior? (waitFor, findBy queries)**

    *Key points: `await waitFor(() => expect(screen.getByText('Loaded')).toBeInTheDocument())`. `findByText` is shorthand for `waitFor + getByText`. Use for: data fetching, animations, timeouts. Set custom timeout: `waitFor(..., { timeout: 5000 })`.*

112. **How do you test custom hooks? (`renderHook` from RTL)**

    *Key points: `const { result } = renderHook(() => useCounter(0))`. `act(() => result.current.increment())`. `rerender` to test prop changes. `waitForNextUpdate` for async hooks. Tests hook logic without a wrapping component.*

113. **How do you mock API calls in component tests? (MSW, jest.mock)**

    *Key points: MSW (Mock Service Worker): intercepts network requests at the service worker level — most realistic. `jest.mock('../api')`: replaces module with mock. MSW is preferred (works with real fetch, no module mocking).*

114. **How do you test error boundaries?**

    *Key points: Render a component that throws inside the error boundary. Use `jest.spyOn(console, 'error').mockImplementation()` to suppress expected errors. Assert that the fallback UI renders. Test both error and non-error states.*

115. **What is snapshot testing? When is it useful? What are its pitfalls?**

    *Key points: Snapshot testing captures the rendered output and compares against a stored snapshot. Useful for: detecting unexpected UI changes, regression testing. Pitfalls: large snapshots (hard to review), false positives (trivial changes), over-reliance.*

### State Management

116. **What is the difference between local state, lifted state, and global state?**

    *Key points: Local state: `useState` within a component. Lifted state: moved to a common parent for sharing between siblings. Global state: accessible by any component (Redux, Context, Zustand). Choose the simplest option that works.*

117. **When should you use `useReducer` vs `useState`?**

    *Key points: Use `useReducer` when: state has complex logic (multiple sub-values), next state depends on previous, multiple state transitions, or you want to centralize update logic. Use `useState` for simple, independent values.*

118. **What is Redux? What problem does it solve?**

    *Key points: Redux is a predictable state container for JavaScript apps. Solves: sharing state across components, predictable state updates (reducers), time-travel debugging, middleware for side effects. Follows Flux pattern: action → reducer → store update.*

119. **What is the difference between Redux and Context API?**

    *Key points: Redux: external library, predictable updates (reducers), middleware, devtools, performance optimizations (selectors). Context: built-in, simpler setup, no middleware, causes re-renders of all consumers. Use Context for simple global state, Redux for complex state logic.*

120. **What is Redux Toolkit? How does it simplify Redux?**

    *Key points: RTK is the official, opinionated Redux toolset. Simplifies: `createSlice` (reducers + actions in one), `configureStore` (includes middleware), Immer (mutable syntax), RTK Query (data fetching). Reduces boilerplate significantly.*

121. **What are Redux slices? How do you create one?**

    *Key points: A slice is a portion of Redux state with its reducers and actions. `createSlice({ name: 'counter', initialState: 0, reducers: { increment: (state) => state + 1 } })`. Auto-generates action creators and action types.*

122. **What is the difference between Redux Thunk and Redux Saga?**

    *Key points: Thunk: simple middleware for async logic (functions that dispatch actions). Saga: uses generators for complex side effects (debouncing, race conditions, parallel tasks). Thunk is simpler; Saga is more powerful for complex workflows.*

123. **What is Zustand? How does it compare to Redux?**

    *Key points: Zustand is a minimal state management library. Simpler API: `const useStore = create((set) => ({ count: 0, inc: () => set(s => ({ count: s.count + 1 })) }))`. No boilerplate, no providers, no reducers. Smaller bundle. Good for simpler state needs.*

124. **What is Jotai or Recoil? How does atomic state management differ from Redux?**

    *Key points: Atomic state management uses small, independent atoms of state (like `useState` but global). Atoms can reference each other. Unlike Redux (single store), atoms are granular — only components using a specific atom re-render when it changes.*

125. **What is the Flux pattern? How does Redux implement it?**

    *Key points: Flux is a unidirectional data flow pattern: Action → Dispatcher → Store → View. Redux implements it with: actions (plain objects with type), reducer (pure function), store (single source of truth), dispatch (sends actions). View dispatches actions.*

### Routing

126. **What is React Router? How does it differ from traditional server-side routing?**

    *Key points: React Router is a client-side routing library. No full page reloads — components are swapped based on URL. Enables SPA navigation. Server-side routing requests a new page from the server (full reload). React Router uses the History API.*

127. **What is the difference between `BrowserRouter` and `HashRouter`?**

    *Key points: `BrowserRouter` uses the History API (clean URLs like `/about`). Requires server config to handle client-side routes. `HashRouter` uses URL hash (`/#/about`) — works without server config. Use `BrowserRouter` for production, `HashRouter` for simple static hosting.*

128. **How do you create routes with React Router v6? (`createBrowserRouter`, `<Routes>`, `<Route>`)**

    *Key points: `createBrowserRouter([{ path: '/', element: <Home />, children: [...] }])` with `<RouterProvider>`. Or JSX: `<Routes><Route path="/" element={<Home />} /></Routes>`. Nested routes with `<Outlet>`. Loaders and actions for data fetching.*

129. **What is the difference between `<Link>` and `<NavLink>`?**

    *Key points: Both navigate without page reload. `<NavLink>` additionally provides an `isActive` class/prop for styling the active link. Use `<Link>` for simple navigation, `<NavLink>` for navigation menus where you need active state styling.*

130. **How do you navigate programmatically? (`useNavigate` hook)**

    *Key points: `const navigate = useNavigate()`. `navigate('/about')` — go to path. `navigate(-1)` — go back. `navigate('/dashboard', { replace: true })` — replace history entry. Use in event handlers, effects, or after form submission.*

131. **How do you read URL parameters? (`useParams` hook)**

    *Key points: `const { id } = useParams()`. Route: `<Route path="/user/:id" />`. URL: `/user/42`. `id` = "42". Returns an object of all dynamic segments. Works with nested routes.*

132. **How do you read query parameters? (`useSearchParams` hook)**

    *Key points: `const [searchParams, setSearchParams] = useSearchParams()`. `searchParams.get('q')` — read param. `setSearchParams({ q: 'react' })` — update params. Similar to `URLSearchParams`. Useful for search/filter state in URL.*

133. **What is nested routing? How do you create layouts with `<Outlet>`?**

    *Key points: Nested routes render child routes inside parent layouts. Parent route uses `<Outlet />` as a placeholder for child content. Example: `<Route element={<Layout />}><Route path="dashboard" element={<Dashboard />} /></Route>`. Layout renders `<Outlet />`.*

134. **What are route loaders and actions in React Router v6?**

    *Key points: Loaders fetch data before rendering a route: `loader: () => fetch('/api/data')`. Actions handle form submissions: `action: async ({ request }) => { ... }`. Both run on the server (if using Remix) or client. Access via `useLoaderData()` and `useActionData()`.*

135. **How do you protect routes (authentication)? What is a ProtectedRoute component?**

    *Key points: Create a wrapper component: `function ProtectedRoute({ children }) { const { user } = useAuth(); return user ? children : <Navigate to="/login" />; }`. Use: `<Route element={<ProtectedRoute />}><Route path="dashboard" element={<Dashboard />} /></Route>`.*

---

## 🔴 SENIOR LEVEL (Advanced)

### Advanced Patterns

136. **What is the render props pattern? How does it compare to hooks for sharing logic?**

    *Key points: Render props: a component receives a function prop that returns JSX: `<DataProvider render={data => <Component data={data} />} />`. Hooks are simpler and more readable. Render props can cause "wrapper hell." Hooks are the modern replacement.*

137. **What is the Higher-Order Component (HOC) pattern? What are its drawbacks?**

    *Key points: HOC: a function that takes a component and returns an enhanced component: `const withAuth = (Component) => (props) => <Component {...props} />`. Drawbacks: naming collisions, wrapper hell, unclear source of props, harder to type with TypeScript.*

138. **What is compound components? Give an example (e.g., `<Select>`, `<Select.Option>`).**

    *Key points: Compound components are a set of components that work together implicitly sharing state via Context. Example: `<Select><Select.Option value="1">One</Select.Option></Select>`. Internal state (selected value) is managed by the parent and shared via Context.*

139. **What is the state reducer pattern? How does it give users control over internal state?**

    *Key points: The component accepts a `reducer` prop that wraps its internal reducer. Users can override specific state transitions. Popularized by Downshift. Example: `<Autocomplete stateReducer={(state, changes) => changes}>`. Gives users fine-grained control without forking the component.*

140. **What is the provider pattern? How do you create a flexible, typed provider?**

    *Key points: Provider pattern uses Context to share data across the tree. Create: `const [ThemeProvider, useTheme] = createContext<Theme>()`. Flexible: accept props for configuration, compose multiple providers. Type-safe: generic context with TypeScript.*

141. **What is the controlled vs uncontrolled component pattern? How do you build a component that supports both?**

    *Key points: A component can be controlled (value prop + onChange) or uncontrolled (internal state). Support both: check if `value` prop is provided — if yes, controlled; if no, use internal state. Pattern: `const [internalValue, setInternalValue] = useState(defaultValue)`.*

142. **What is the polymorphic component pattern? (e.g., `as` prop like in Chakra UI)**

    *Key points: A component that can render as different HTML elements: `<Text as="h1">Title</Text>` renders `<h1>`. Implementation: `const Text = React.forwardRef(({ as: Tag = 'p', ...props }, ref) => <Tag ref={ref} {...props} />)`. Type-safe with TypeScript generics.*

143. **What is the slot pattern? How does it differ from `children`?**

    *Key points: Slots allow passing multiple named content areas: `<Card header={<Header />} footer={<Footer />}><Content /></Card>`. More flexible than single `children` — components can render content in specific positions. Similar to Vue slots or Web Components slots.*

144. **What is the proxy component pattern? When would you use it?**

    *Key points: A proxy component wraps a third-party component to provide a simplified or customized API. Example: `const MyButton = (props) => <MuiButton variant="contained" color="primary" {...props} />`. Use for: design system consistency, simplifying complex APIs.*

### Concurrent React & Suspense

145. **What is Concurrent React? How does it differ from synchronous rendering?**

    *Key points: Concurrent React can interrupt rendering to handle higher-priority updates. Synchronous rendering blocks the main thread until complete. Concurrent rendering is interruptible, prioritizes urgent updates, and can render in the background.*

146. **What is Suspense? How does it work with `React.lazy()`?**

    *Key points: Suspense lets components "wait" for something before rendering. With `React.lazy()`: `<Suspense fallback={<Loading />}><LazyComponent /></Suspense>`. Shows fallback while the lazy-loaded chunk downloads. Also works for data fetching (React 18+).*

147. **What is Suspense for data fetching? How does it differ from `useEffect` + loading state?**

    *Key points: Suspense for data fetching lets components throw a promise while loading — React suspends rendering and shows the nearest fallback. Unlike `useEffect` + loading state (manual loading flags, race conditions), Suspense is declarative and integrates with concurrent features.*

148. **What is the difference between `startTransition` and `useTransition`?**

    *Key points: `startTransition(callback)` is a function that marks updates as transitions. `useTransition()` returns `[isPending, startTransition]` — same but also provides `isPending` for showing loading state. Both mark updates as non-urgent.*

149. **What is the difference between urgent and non-urgent updates in Concurrent React?**

    *Key points: Urgent updates: typing, clicking, scrolling — need immediate response. Non-urgent: filtering a large list, rendering results — can be deferred. Concurrent React prioritizes urgent updates, interrupting non-urgent ones to keep UI responsive.*

150. **How does Concurrent React improve perceived performance?**

    *Key points: Keeps UI responsive during heavy rendering. Prioritizes user interactions. Shows stale UI briefly instead of freezing. Uses `startTransition` to defer non-critical updates. Results in smoother interactions and fewer dropped frames.*

151. **What is the `flushSync` API? When would you use it?**

    *Key points: `flushSync(callback)` forces React to flush updates synchronously. Use when: you need the DOM to update immediately (e.g., measuring layout, third-party integration). Overrides React's batching. Use sparingly — can hurt performance.*

### Server Components

152. **What are React Server Components (RSC)? How do they differ from client components?**

    *Key points: RSC run on the server, send zero JavaScript to the client. They can access databases, file systems directly. Client components run in the browser with full interactivity. RSC reduce bundle size and improve initial load.*

153. **What is the `'use client'` directive? When do you need it?**

    *Key points: `'use client'` marks a file as a client component (runs in browser). Needed when: using state, effects, event handlers, browser APIs, or any interactivity. Files without `'use client'` are server components by default in frameworks like Next.js.*

154. **What are the benefits of Server Components? (reduced bundle size, direct database access)**

    *Key points: 1) Zero JavaScript sent to client. 2) Direct database/file system access (no API endpoints needed). 3) Automatic code splitting. 4) Smaller bundles. 5) Better SEO. 6) Faster initial page load. 7) Keep sensitive logic on server.*

155. **How do Server Components interact with client components?**

    *Key points: Server components can render client components. Client components cannot import server components. Server components can pass serializable props to client components. Client components can't pass server components as children (but can pass JSX as children).*

156. **What can't Server Components do? (no state, no effects, no event handlers)**

    *Key points: No `useState`, `useEffect`, `useReducer`. No event handlers (`onClick`, `onSubmit`). No browser APIs (`window`, `document`). No hooks that depend on client state. No interactivity. They are rendered once on the server and sent as static HTML/stream.*

157. **How does Next.js implement Server Components?**

    *Key points: Next.js 13+ uses Server Components by default. Files are server components unless marked `'use client'`. Supports streaming (Suspense boundaries). Integrates with App Router. Server Components can fetch data directly with `async` component functions.*

### Architecture & Design

158. **How do you structure a large React application? (feature-based vs file-type-based)**

    *Key points: Feature-based: group files by feature (`users/`, `products/`, `cart/`). File-type-based: group by type (`components/`, `hooks/`, `utils/`). Feature-based scales better — related code is co-located, easier to navigate, and teams own features.*

159. **What is the container/presentational component pattern? Is it still relevant with hooks?**

    *Key points: Container: handles logic/state. Presentational: handles rendering (receives props). With hooks, the pattern is less necessary — hooks encapsulate logic, and components can be both. Still useful for separation of concerns in complex components.*

160. **How do you handle authentication and authorization in a React app?**

    *Key points: Auth: store user/token in context, protect routes with `<ProtectedRoute>`, persist token (localStorage/cookies), refresh tokens. Authorization: check user roles/permissions, conditionally render UI, protect API routes on server.*

161. **How do you implement role-based access control (RBAC) in React?**

    *Key points: Define roles and permissions. Create a `usePermissions()` hook that checks user roles. Create `<Can permission="edit" />` component that conditionally renders children. Check permissions on both client (UI) and server (API).*

162. **How do you handle internationalization (i18n) in React?**

    *Key points: Libraries: react-i18next, react-intl. Pattern: `useTranslation()` hook, `<Trans>` component for rich text. Store translations in JSON files. Detect locale from browser/URL. Format dates/numbers with `Intl` API. Lazy-load translation files.*

163. **How do you implement a theme system (dark/light mode) in React?**

    *Key points: Use Context to store theme. CSS custom properties for theme values. `useTheme()` hook to access current theme. Toggle button updates context. Persist preference in localStorage. Respect `prefers-color-scheme` media query for initial value.*

164. **How do you handle optimistic updates in React?**

    *Key points: Update UI immediately before API response. Revert on error. Libraries: React Query (`onMutate`, `onError` rollback), SWR. Pattern: `setState(optimisticValue); try { await api.update(data); } catch { setState(originalValue); }`.*

165. **How do you implement infinite scrolling in React?**

    *Key points: Use Intersection Observer on a sentinel element at the bottom. When visible, fetch next page. Append new data to existing list. Libraries: react-infinite-scroll-component, react-intersection-observer. Handle loading, error, and "no more data" states.*

166. **How do you handle real-time updates (WebSockets) in React?**

    *Key points: Connect in `useEffect`, clean up on unmount. Store connection in ref. Update state on message. Libraries: Socket.IO client. Pattern: `useEffect(() => { const ws = new WebSocket(url); ws.onmessage = (e) => setData(JSON.parse(e.data)); return () => ws.close(); }, [url])`.*

167. **How do you implement undo/redo in a React application?**

    *Key points: Store history as an array of states with current index. `undo`: go to previous index. `redo`: go to next index. Push new states, truncating future states. Libraries: use-undo, zustand/middleware. Limit history size to prevent memory issues.*

### Performance Optimization (Advanced)

168. **What is the Virtual DOM? How does it differ from the Shadow DOM?**

    *Key points: Virtual DOM: in-memory representation of the real DOM, used for diffing and batching updates (React concept). Shadow DOM: browser technology for encapsulating DOM and styles (Web Components). Different purposes — Virtual DOM for performance, Shadow DOM for encapsulation.*

169. **How does React batch state updates? What changed in React 18?**

    *Key points: React batches multiple state updates into a single re-render. React 18 introduced automatic batching — even in timeouts, promises, and native event handlers. Previously, only React event handlers were batched. Reduces unnecessary renders.*

170. **What is the `flushSync` API? When would you use it?**

    *Key points: `flushSync(callback)` forces React to flush updates synchronously. Use when: you need the DOM to update immediately (e.g., measuring layout, third-party integration). Overrides React's batching. Use sparingly — can hurt performance.*

171. **How do you measure and improve Largest Contentful Paint (LCP) in a React app?**

    *Key points: LCP measures when the largest content element becomes visible. Improve: optimize images (next/image), lazy-load below-fold content, minimize render-blocking resources, use SSR/SSG, code-split, optimize fonts, reduce JavaScript bundle size.*

172. **How do you measure and improve Cumulative Layout Shift (CLS) in a React app?**

    *Key points: CLS measures visual stability. Improve: set explicit dimensions on images/videos, reserve space for dynamic content (ads, embeds), use `aspect-ratio` CSS, avoid inserting content above existing content, use skeleton loaders.*

173. **What is the `useEvent` hook (proposed)? What problem does it solve?**

    *Key points: `useEvent(callback)` (proposed) returns a stable function reference that always calls the latest callback. Solves: the problem where `useCallback` with no deps captures stale values, but adding deps causes re-renders. Not yet released.*

174. **How do you optimize images in a React application?**

    *Key points: Use `next/image` (Next.js) or `react-lazy-load-image-component`. Lazy loading (`loading="lazy"`). Responsive images (`srcSet`, `sizes`). WebP/AVIF formats. CDN for image optimization. Blur placeholder while loading.*

175. **How do you implement virtual scrolling for large lists?**

    *Key points: Libraries: react-window, react-virtuoso. Render only visible items + overscan. Fixed or dynamic item heights. Pattern: `<FixedSizeList height={600} itemCount={10000} itemSize={50}>{({ index, style }) => <div style={style}>Item {index}</div>}</FixedSizeList>`.*

176. **How do you optimize context to prevent cascading re-renders?**

    *Key points: Split contexts (separate concerns). Memoize context value with `useMemo`. Use `React.memo` on consumers (doesn't prevent context re-renders but helps with child re-renders). Libraries: `use-context-selector` for fine-grained subscriptions.*

177. **What is the `React.memo` comparison function? How do you customize it?**

    *Key points: `React.memo(Component, (prevProps, nextProps) => boolean)`. Return `true` to skip re-render (props are equal). Default: shallow comparison. Customize for: deep comparison, comparing specific props, ignoring irrelevant changes.*

### Build Tools & Bundling

178. **What is the difference between Create React App, Vite, and Next.js?**

    *Key points: CRA: webpack-based, no config, slow dev server, legacy. Vite: esbuild-based, fast HMR, modern, minimal config. Next.js: full framework (SSR, SSG, routing, API routes), opinionated, production-ready. Vite for SPAs, Next.js for full-featured apps.*

179. **How does Vite differ from webpack? Why is it faster?**

    *Key points: Vite uses esbuild for pre-bundling (Go-based, 10-100x faster than webpack). Dev server serves native ES modules (no bundling needed). HMR is instant (only updates changed modules). Webpack bundles everything upfront. Vite is significantly faster in development.*

180. **What is tree-shaking? How does it work with React?**

    *Key points: Tree-shaking removes unused exports during bundling. Works with ES modules (static imports). React supports tree-shaking — import only what you use: `import { useState } from 'react'` instead of `import React from 'react'`. Reduces bundle size.*

181. **How do you configure code splitting in a React app?**

    *Key points: Dynamic `import()` + `React.lazy()` + `<Suspense>`. Route-based splitting: `const Home = lazy(() => import('./Home'))`. Component-based splitting for heavy components (charts, editors). Configure chunk naming in bundler.*

182. **What is the difference between dynamic `import()` and `React.lazy()`?**

    *Key points: Dynamic `import()` is a JavaScript feature that returns a Promise of a module. `React.lazy()` wraps dynamic `import()` to create a component that can be rendered with Suspense. `React.lazy()` is React-specific; dynamic `import()` is general-purpose.*

183. **How do you set up a React project from scratch without a CLI?**

    *Key points: 1) `npm init`. 2) Install: `react`, `react-dom`, bundler (Vite/webpack), Babel/preset-react. 3) Configure bundler (vite.config.js / webpack.config.js). 4) Create `index.html`, `src/main.jsx`, `src/App.jsx`. 5) Add build/dev scripts. Vite makes this simpler.*

### TypeScript with React

184. **How do you type props in a React component? (`React.FC` vs direct type annotation)**

    *Key points: `type Props = { name: string }`. `const Comp = ({ name }: Props) => ...`. `React.FC<Props>` is discouraged (adds implicit `children`, doesn't work with generics). Direct annotation is preferred — explicit, flexible, no implicit children.*

185. **How do you type `useState`? When does TypeScript infer the type vs needing explicit annotation?**

    *Key points: `const [count, setCount] = useState(0)` — inferred as `number`. Explicit: `useState<string | null>(null)`. Need explicit when: initial value doesn't fully represent the type (null, union types), or complex initial state.*

186. **How do you type `useRef`? What is the difference between `useRef<HTMLInputElement>(null)` and `useRef<HTMLInputElement | null>(null)`?**

    *Key points: `useRef<HTMLInputElement>(null)` — type is `MutableRefObject<HTMLInputElement | null>` (readonly `current`). `useRef<HTMLInputElement | null>(null)` — type is `MutableRefObject<HTMLInputElement | null>` (mutable `current`). First is for DOM refs, second for mutable values.*

187. **How do you type event handlers? (`React.ChangeEvent`, `React.MouseEvent`, `React.FormEvent`)**

    *Key points: `onChange: (e: React.ChangeEvent<HTMLInputElement>) => void`. `onClick: (e: React.MouseEvent<HTMLButtonElement>) => void`. `onSubmit: (e: React.FormEvent<HTMLFormElement>) => void`. TypeScript infers these automatically when using inline handlers.*

188. **How do you type `useReducer` with discriminated unions?**

    *Key points: `type Action = { type: 'increment' } | { type: 'set', payload: number }`. `const reducer = (state: State, action: Action): State => { switch(action.type) { case 'increment': return state + 1; case 'set': return action.payload; } }`. TypeScript narrows the action type in each case.*

189. **How do you type `forwardRef`? What is the `Ref` type?**

    *Key points: `const Comp = forwardRef<HTMLInputElement, Props>((props, ref) => <input ref={ref} />)`. `Ref<T>` is `RefCallback<T> | RefObject<T> | null`. Use `useImperativeHandle` to expose custom methods: `forwardRef<CustomHandle, Props>`.*

190. **How do you type `children`? (`React.ReactNode` vs `React.ReactElement`)**

    *Key points: `React.ReactNode` — anything renderable (string, number, JSX, fragments, null, undefined). `React.ReactElement` — only JSX elements (not strings/numbers). Use `ReactNode` for `children` (most flexible). Use `ReactElement` when you need a single JSX element.*

191. **How do you type generic components? (e.g., a `List<T>` component)**

    *Key points: `function List<T>({ items, render }: { items: T[], render: (item: T) => ReactNode })`. TypeScript infers `T` from usage: `<List items={users} render={user => user.name} />`. Use generic constraints: `<T extends { id: string }>`.*

192. **How do you type higher-order components?**

    *Key points: `function withAuth<P extends object>(Component: React.ComponentType<P>): React.FC<P & { user: User }>`. Returns a new component with injected props. Use `Omit` to remove injected props from the returned component's props type.*

193. **How do you type context with a default value?**

    *Key points: `const AuthContext = createContext<AuthContextType | undefined>(undefined)`. Custom hook: `function useAuth() { const ctx = useContext(AuthContext); if (!ctx) throw new Error('...'); return ctx; }`. Or provide a sensible default: `createContext<AuthContextType>(defaultAuth)`.*

### Testing (Advanced)

194. **How do you test component behavior, not implementation details?**

    *Key points: Query by accessible roles, labels, text (not class names, test IDs, state). Test user interactions and outcomes. Avoid testing internal state, prop calls, or lifecycle methods. Tests should pass after refactoring if behavior is unchanged.*

195. **How do you test accessibility with React Testing Library?**

    *Key points: Use `jest-axe` or `@testing-library/jest-dom` matchers. `expect(screen.getByRole('button')).toBeInTheDocument()`. `await axe(container)` for automated a11y audits. Test keyboard navigation, focus management, aria attributes.*

196. **How do you test animations and transitions?**

    *Key points: Mock timers (`jest.useFakeTimers()`). Use `waitFor` to wait for animation to complete. Test initial and final states. For CSS transitions, test class changes. For JS animations, mock the animation library. Avoid testing animation internals.*

197. **How do you test drag-and-drop interactions?**

    *Key points: Use `fireEvent.dragStart`, `fireEvent.dragOver`, `fireEvent.drop`. Libraries: `@testing-library/user-event` (limited DnD support). For complex DnD, use `react-dnd-test-utils` or `@dnd-kit` test utilities. Test both successful and failed drops.*

198. **How do you test components that use `react-router`?**

    *Key points: Wrap in `MemoryRouter`: `render(<MemoryRouter initialEntries={['/users/42']}><UserPage /></MemoryRouter>)`. Test navigation: `await userEvent.click(screen.getByText('Home'))` and assert new content appears. Mock `useNavigate` if needed.*

199. **How do you test components that use Redux or Context?**

    *Key points: Wrap in provider: `render(<Provider store={store}><MyComponent /></Provider>)`. Create a test wrapper with custom render function. For Context: `render(<ThemeContext.Provider value="dark"><MyComponent /></ThemeContext.Provider>)`.*

200. **How do you write integration tests for a full feature flow?**

    *Key points: Render the full page/feature. Mock API at the network level (MSW). Simulate user interactions (click, type, navigate). Assert on UI changes and navigation. Test happy path and error states. Use `waitFor` for async assertions.*

---

## 💡 BONUS: Problem-Solving & Behavioral

201. **How would you build a reusable data table component with sorting, filtering, and pagination?**

    *Key points: Accept `columns` and `data` props. Use `useState` for sort/filter/page state. Compute derived data (sorted, filtered, paginated). Render table with headers, rows, pagination controls. Make it generic with TypeScript. Consider virtualization for large datasets.*

202. **How would you build a typeahead/autocomplete component from scratch?**

    *Key points: Controlled input with debounced value. Fetch suggestions on input change. Render dropdown with keyboard navigation (arrow keys, enter, escape). Handle: loading, error, empty states, click outside to close, accessibility (aria-combobox).*

203. **How would you implement a modal/dialog component with focus trapping and keyboard navigation?**

    *Key points: Portal to document body. Overlay + content. Focus trap: on open, focus first focusable element; Tab cycles within modal; Escape closes. `aria-modal="true"`, `role="dialog"`. Prevent body scroll. Animate enter/exit.*

204. **How would you implement a drag-and-drop file upload component?**

    *Key points: Drop zone with `onDragOver`, `onDrop`. Read files from `dataTransfer.files`. Show preview (images). Upload with progress. Handle: multiple files, drag state styling, file type/size validation, error handling. Libraries: react-dropzone.*

205. **How would you implement a carousel/slider component?**

    *Key points: Track current index. Render items with `transform: translateX`. Auto-play with interval. Navigation dots and arrows. Touch/swipe support. Infinite loop option. Pause on hover. Accessible with `aria-roledescription="carousel"`.*

206. **How would you implement a toast notification system?**

    *Key points: Create a `ToastContext` with `addToast`, `removeToast`. Render toasts in a portal. Each toast has: message, type (success/error), auto-dismiss timer, close button. Animate enter/exit. Stack multiple toasts. Use `useReducer` for toast state management.*

207. **How would you implement an undo/redo system for a drawing app?**

    *Key points: Store history as array of canvas snapshots. `undo`: restore previous snapshot. `redo`: restore next snapshot. Limit history size. Use `useReducer` for predictable state transitions. Consider command pattern for granular undo.*

208. **How would you implement a real-time collaborative editor?**

    *Key points: WebSocket connection for real-time communication. Operational Transform (OT) or CRDT for conflict resolution. Libraries: ShareDB, Yjs, Liveblocks. Handle: cursor positions, selection, presence, offline support, merge conflicts.*

209. **Describe a time you optimized a slow React component. What tools did you use?**

    *Key points: Identify with React DevTools Profiler. Common fixes: `React.memo`, `useMemo`, `useCallback`, virtualization, code splitting, lazy loading, reducing re-renders, optimizing context, debouncing/throttling. Measure before/after with Profiler.*

210. **How do you decide when to use a state management library vs Context vs local state?**

    *Key points: Local state: component-specific data. Lifted state: shared between few siblings. Context: app-wide, low-frequency updates. State management (Redux/Zustand): complex state logic, frequent updates, middleware needs, devtools, cross-component communication.*

211. **How do you approach migrating a class component to a functional component with hooks?**

    *Key points: 1) Convert class to function. 2) Replace `this.state` + `setState` with `useState`/`useReducer`. 3) Replace lifecycle methods with `useEffect`. 4) Replace `this.method` with functions. 5) Replace HOCs with hooks. 6) Test behavior is unchanged.*

212. **How do you stay up-to-date with React? Which recent feature excited you most?**

    *Key points: Follow React blog, RFCs, GitHub discussions. Twitter/X: @reactjs, @acdlite, @dan_abramov. Podcasts: React Podcast, Syntax. Conferences: React Conf, React Summit. Recent exciting features: Server Components, `use()` hook, React Forget (auto-memoization).*
