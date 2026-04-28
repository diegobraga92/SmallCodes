# React - Technical Interview Questions

## 🟢 JUNIOR LEVEL (Fundamentals)

### JSX & Rendering

1. What is JSX? Why isn't it HTML? How does the compiler transform it?
2. What are the rules of JSX? (single root element, closing tags, className vs class, etc.)
3. What is the difference between an element and a component in React?
4. How do you render a list in React? Why do you need a `key` prop? What happens if you use the index as a key?
5. What is the difference between `{}` and `{{}}` in JSX?
6. How do you conditionally render content in React? Give at least three approaches.
7. What is the difference between `if/else` and the ternary operator in JSX?
8. How do you render `null`, `undefined`, and `false` in JSX? Which values produce no output?
9. What is a Fragment (`<>...</>`)? Why would you use it instead of a `<div>`?
10. How do you add inline styles in JSX? Why are property names camelCased?

### Components & Props

11. What is the difference between a functional component and a class component?
12. What are props? Are they mutable? How do you pass data from parent to child?
13. What is props drilling? What problems does it cause?
14. What is the `children` prop? How do you use it for component composition?
15. How do you set default values for props? (defaultProps vs default parameters)
16. What is the difference between controlled and uncontrolled components? Give an example of each.
17. What is a pure component? How does `React.memo()` work?
18. What is the difference between `React.createElement()` and JSX?

### State & Lifecycle

19. What is state in React? How does it differ from props?
20. What does the `useState` hook return? How do you update state?
21. Why shouldn't you mutate state directly? What happens if you do?
22. What is the difference between `useState` with a value vs a function updater?
23. What is the `useEffect` hook? What is its purpose?
24. What is the dependency array in `useEffect`? What happens if you omit it, pass `[]`, or pass variables?
25. How do you clean up side effects in `useEffect`? Give an example (e.g., event listener, subscription).
26. What is the component lifecycle in a functional component with hooks?
27. What is the `useRef` hook? How does it differ from `useState`?
28. How do you access a DOM element with `useRef`?

### Event Handling

29. How do event handlers work in React? How do they differ from native DOM events?
30. What is synthetic events in React? Why does React use them?
31. How do you pass arguments to an event handler? What is the difference between `onClick={handleClick}` and `onClick={() => handleClick(id)}`?
32. How do you prevent default behavior in React? (e.g., form submission)
33. How do you stop event propagation in React?
34. What is event pooling in React 16? Why was it removed in React 17+?

### Forms

35. How do you handle form inputs in React? What is a controlled input?
36. How do you handle multiple inputs with a single change handler?
37. How do you handle form submission? What is `event.preventDefault()`?
38. What is the difference between `value` and `defaultValue` in an input?
39. How do you handle textarea, select, checkbox, and radio inputs in React?
40. How do you implement form validation in React?

### Lists & Keys

41. Why does React need a `key` prop when rendering lists?
42. What happens if you use array index as a key? When is it acceptable?
43. What is a stable key? How do you generate unique keys?
44. How does React use keys for reconciliation?

### Conditional Rendering

45. What are the different ways to conditionally render in React?
46. Why can't you use `if/else` inside JSX? How do you work around it?
47. What is the `&&` pattern for conditional rendering? What are its pitfalls with falsy values like `0`?
48. What is the ternary pattern vs `&&`? When would you choose each?

---

## 🟡 MID-LEVEL (Intermediate)

### Hooks Deep Dive

49. What are the rules of hooks? Why must hooks be called at the top level and not inside conditions/loops?
50. How does React know which state belongs to which `useState` call? (hooks linked list)
51. What is the `useCallback` hook? When would you use it? What problem does it solve?
52. What is the `useMemo` hook? How does it differ from `useCallback`?
53. What is the difference between `useMemo` and `useEffect`? When would you use each?
54. What is the `useReducer` hook? When would you choose it over `useState`?
55. What is the `useContext` hook? How does it work with `React.createContext()`?
56. What is the `useImperativeHandle` hook? When would you use it?
57. What is the `useLayoutEffect` hook? How does it differ from `useEffect`?
58. What is the `useDebugValue` hook? How is it useful for custom hooks?
59. What is the `useTransition` hook? How does it help with urgent vs non-urgent updates?
60. What is the `useDeferredValue` hook? How does it differ from `useTransition`?
61. What is the `useId` hook? What problem does it solve for accessibility?
62. What is the `useSyncExternalStore` hook? When would you use it?

### Custom Hooks

63. What is a custom hook? How do you create one?
64. What are the naming conventions for custom hooks? Why must they start with `use`?
65. How do you share logic between components without custom hooks? (HOCs, render props)
66. How do you create a custom hook for fetching data? How do you handle loading, error, and success states?
67. How do you create a custom hook for debouncing input?
68. How do you create a custom hook for `localStorage` synchronization?
69. How do you create a custom hook for media queries?
70. How do you create a custom hook for `useInterval`?
71. How do you create a custom hook for `usePrevious`?
72. How do you test a custom hook? (renderHook from React Testing Library)

### Context API

73. What is the Context API? What problem does it solve?
74. How do you create a context? How do you provide and consume it?
75. What is the difference between `useContext` and Context.Consumer?
76. What are the performance implications of Context? How does it cause unnecessary re-renders?
77. How do you optimize Context to prevent re-renders? (memoization, splitting contexts)
78. When should you use Context vs prop drilling vs a state management library?
79. How do you create a context with a custom hook for type safety?

### Refs & DOM

80. What is the difference between `useRef` and `createRef`?
81. How do you use refs for DOM manipulation? When is it appropriate vs using state?
82. What is callback ref? When would you use it?
83. What is ref forwarding? How does `forwardRef` work?
84. How do you use refs with third-party libraries that need DOM nodes?
85. What is the difference between refs and state for values that don't trigger re-renders?

### Error Handling

86. What is an error boundary? How do you create one?
87. What lifecycle methods do error boundaries use? (`componentDidCatch`, `getDerivedStateFromError`)
88. Can error boundaries catch errors in event handlers? Why or why not?
89. How do you handle errors in async operations (e.g., API calls)?
90. How do you create a reusable error boundary component?

### Performance

91. What is reconciliation in React? How does the diffing algorithm work?
92. What is the Fiber architecture? How does it enable concurrent features?
93. What causes unnecessary re-renders? How do you diagnose them? (React DevTools Profiler)
94. How does `React.memo()` prevent re-renders? What are its limitations?
95. How does `useMemo` and `useCallback` help with performance? When can they hurt performance?
96. What is code splitting in React? How does `React.lazy()` and `Suspense` work?
97. What is virtualization? How do libraries like `react-window` improve performance with large lists?
98. What is the `key` prop's role in reconciliation? How does changing a key affect the DOM?
99. What is the difference between `useMemo` and `React.memo`?
100. How do you profile a React application? What tools do you use?

### Styling Approaches

101. What are the different ways to style React components? (CSS modules, styled-components, Tailwind, inline styles)
102. What is CSS-in-JS? What are the pros and cons?
103. How does styled-components work? What is the `styled` API?
104. What is CSS Modules? How does it differ from global CSS?
105. What is Tailwind CSS with React? How does it compare to component libraries?

### Testing

106. What is the difference between React Testing Library and Enzyme?
107. What is the guiding philosophy of React Testing Library? ("test how users use it")
108. How do you render a component for testing? (`render` from RTL)
109. How do you query elements in RTL? (`getBy`, `queryBy`, `findBy` — what's the difference?)
110. How do you simulate user interactions in tests? (`fireEvent` vs `userEvent`)
111. How do you test async behavior? (waitFor, findBy queries)
112. How do you test custom hooks? (`renderHook` from RTL)
113. How do you mock API calls in component tests? (MSW, jest.mock)
114. How do you test error boundaries?
115. What is snapshot testing? When is it useful? What are its pitfalls?

### State Management

116. What is the difference between local state, lifted state, and global state?
117. When should you use `useReducer` vs `useState`?
118. What is Redux? What problem does it solve?
119. What is the difference between Redux and Context API?
120. What is Redux Toolkit? How does it simplify Redux?
121. What are Redux slices? How do you create one?
122. What is the difference between Redux Thunk and Redux Saga?
123. What is Zustand? How does it compare to Redux?
124. What is Jotai or Recoil? How does atomic state management differ from Redux?
125. What is the Flux pattern? How does Redux implement it?

### Routing

126. What is React Router? How does it differ from traditional server-side routing?
127. What is the difference between `BrowserRouter` and `HashRouter`?
128. How do you create routes with React Router v6? (`createBrowserRouter`, `<Routes>`, `<Route>`)
129. What is the difference between `<Link>` and `<NavLink>`?
130. How do you navigate programmatically? (`useNavigate` hook)
131. How do you read URL parameters? (`useParams` hook)
132. How do you read query parameters? (`useSearchParams` hook)
133. What is nested routing? How do you create layouts with `<Outlet>`?
134. What are route loaders and actions in React Router v6?
135. How do you protect routes (authentication)? What is a ProtectedRoute component?

---

## 🔴 SENIOR LEVEL (Advanced)

### Advanced Patterns

136. What is the render props pattern? How does it compare to hooks for sharing logic?
137. What is the Higher-Order Component (HOC) pattern? What are its drawbacks?
138. What is compound components? Give an example (e.g., `<Select>`, `<Select.Option>`).
139. What is the state reducer pattern? How does it give users control over internal state?
140. What is the provider pattern? How do you create a flexible, typed provider?
141. What is the controlled vs uncontrolled component pattern? How do you build a component that supports both?
142. What is the polymorphic component pattern? (e.g., `as` prop like in Chakra UI)
143. What is the slot pattern? How does it differ from `children`?
144. What is the proxy component pattern? When would you use it?

### Concurrent React & Suspense

145. What is Concurrent React? How does it differ from synchronous rendering?
146. What is Suspense? How does it work with `React.lazy()`?
147. What is Suspense for data fetching? How does it differ from `useEffect` + loading state?
148. What is the difference between `startTransition` and `useTransition`?
149. What is the difference between urgent and non-urgent updates in Concurrent React?
150. How does Concurrent React improve perceived performance?
151. What is the `flushSync` API? When would you use it?

### Server Components

152. What are React Server Components (RSC)? How do they differ from client components?
153. What is the `'use client'` directive? When do you need it?
154. What are the benefits of Server Components? (reduced bundle size, direct database access)
155. How do Server Components interact with client components?
156. What can't Server Components do? (no state, no effects, no event handlers)
157. How does Next.js implement Server Components?

### Architecture & Design

158. How do you structure a large React application? (feature-based vs file-type-based)
159. What is the container/presentational component pattern? Is it still relevant with hooks?
160. How do you handle authentication and authorization in a React app?
161. How do you implement role-based access control (RBAC) in React?
162. How do you handle internationalization (i18n) in React?
163. How do you implement a theme system (dark/light mode) in React?
164. How do you handle optimistic updates in React?
165. How do you implement infinite scrolling in React?
166. How do you handle real-time updates (WebSockets) in React?
167. How do you implement undo/redo in a React application?

### Performance Optimization (Advanced)

168. What is the Virtual DOM? How does it differ from the Shadow DOM?
169. How does React batch state updates? What changed in React 18?
170. What is the `flushSync` API? When would you use it?
171. How do you measure and improve Largest Contentful Paint (LCP) in a React app?
172. How do you measure and improve Cumulative Layout Shift (CLS) in a React app?
173. What is the `useEvent` hook (proposed)? What problem does it solve?
174. How do you optimize images in a React application?
175. How do you implement virtual scrolling for large lists?
176. How do you optimize context to prevent cascading re-renders?
177. What is the `React.memo` comparison function? How do you customize it?

### Build Tools & Bundling

178. What is the difference between Create React App, Vite, and Next.js?
179. How does Vite differ from webpack? Why is it faster?
180. What is tree-shaking? How does it work with React?
181. How do you configure code splitting in a React app?
182. What is the difference between dynamic `import()` and `React.lazy()`?
183. How do you set up a React project from scratch without a CLI?

### TypeScript with React

184. How do you type props in a React component? (`React.FC` vs direct type annotation)
185. How do you type `useState`? When does TypeScript infer the type vs needing explicit annotation?
186. How do you type `useRef`? What is the difference between `useRef<HTMLInputElement>(null)` and `useRef<HTMLInputElement | null>(null)`?
187. How do you type event handlers? (`React.ChangeEvent`, `React.MouseEvent`, `React.FormEvent`)
188. How do you type `useReducer` with discriminated unions?
189. How do you type `forwardRef`? What is the `Ref` type?
190. How do you type `children`? (`React.ReactNode` vs `React.ReactElement`)
191. How do you type generic components? (e.g., a `List<T>` component)
192. How do you type higher-order components?
193. How do you type context with a default value?

### Testing (Advanced)

194. How do you test component behavior, not implementation details?
195. How do you test accessibility with React Testing Library?
196. How do you test animations and transitions?
197. How do you test drag-and-drop interactions?
198. How do you test components that use `react-router`?
199. How do you test components that use Redux or Context?
200. How do you write integration tests for a full feature flow?

---

## 💡 BONUS: Problem-Solving & Behavioral

201. How would you build a reusable data table component with sorting, filtering, and pagination?
202. How would you build a typeahead/autocomplete component from scratch?
203. How would you implement a modal/dialog component with focus trapping and keyboard navigation?
204. How would you implement a drag-and-drop file upload component?
205. How would you implement a carousel/slider component?
206. How would you implement a toast notification system?
207. How would you implement an undo/redo system for a drawing app?
208. How would you implement a real-time collaborative editor?
209. Describe a time you optimized a slow React component. What tools did you use?
210. How do you decide when to use a state management library vs Context vs local state?
211. How do you approach migrating a class component to a functional component with hooks?
212. How do you stay up-to-date with React? Which recent feature excited you most?
