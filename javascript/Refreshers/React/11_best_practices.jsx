/**
 * REACT BEST PRACTICES
 * =====================
 * Folder structure, patterns, anti-patterns, accessibility, error handling
 */

import React from 'react';

console.log("=".repeat(80));
console.log("REACT BEST PRACTICES");
console.log("=".repeat(80));

// ============================================================================
// 1. FOLDER STRUCTURE
// ============================================================================

/*
   Feature-based structure (recommended for medium-large apps):
   
   src/
   ├── features/
   │   ├── auth/
   │   │   ├── components/
   │   │   │   ├── LoginForm.tsx
   │   │   │   └── ProtectedRoute.tsx
   │   │   ├── hooks/
   │   │   │   └── useAuth.ts
   │   │   ├── api/
   │   │   │   └── authApi.ts
   │   │   └── index.ts
   │   ├── users/
   │   │   ├── components/
   │   │   ├── hooks/
   │   │   └── api/
   │   └── dashboard/
   ├── shared/
   │   ├── components/    (Button, Card, Modal)
   │   ├── hooks/         (useDebounce, useFetch)
   │   ├── utils/         (formatDate, cn)
   │   └── types/         (shared TypeScript types)
   ├── layouts/
   ├── pages/
   ├── routes/
   ├── store/
   └── App.tsx
*/

// ============================================================================
// 2. COMPONENT COMPOSITION PATTERNS
// ============================================================================

// --- Compound Components ---
// function Tabs({ children, defaultIndex = 0 }) {
//     const [activeIndex, setActiveIndex] = React.useState(defaultIndex);
//
//     const childrenArray = React.Children.toArray(children);
//     const tabList = childrenArray.map((child, index) => (
//         <TabHeader
//             key={index}
//             isActive={index === activeIndex}
//             onClick={() => setActiveIndex(index)}
//         >
//             {child.props.label}
//         </TabHeader>
//     ));
//
//     return (
//         <div>
//             <div role="tablist">{tabList}</div>
//             {childrenArray[activeIndex]}
//         </div>
//     );
// }
//
// Tabs.Tab = function Tab({ children }) {
//     return <div role="tabpanel">{children}</div>;
// };
//
// // Usage:
// // <Tabs>
// //     <Tabs.Tab label="Profile">Profile content</Tabs.Tab>
// //     <Tabs.Tab label="Settings">Settings content</Tabs.Tab>
// // </Tabs>

// --- Render Props Pattern ---
// function DataFetcher({ url, children }) {
//     const { data, loading, error } = useFetch(url);
//     return children({ data, loading, error });
// }
//
// // Usage:
// // <DataFetcher url="/api/users">
// //     {({ data, loading }) => loading ? <Spinner /> : <UserList users={data} />}
// // </DataFetcher>

// ============================================================================
// 3. ERROR BOUNDARIES
// ============================================================================

/*
   Error boundaries catch JavaScript errors in their child component tree.
   They prevent the entire app from crashing.
   
   Note: Error boundaries must be class components (hooks don't support them yet).
*/

// class ErrorBoundary extends React.Component {
//     constructor(props) {
//         super(props);
//         this.state = { hasError: false, error: null };
//     }
//
//     static getDerivedStateFromError(error) {
//         return { hasError: true, error };
//     }
//
//     componentDidCatch(error, errorInfo) {
//         console.error('Error caught:', error, errorInfo);
//         // Send to error reporting service (Sentry, LogRocket, etc.)
//     }
//
//     render() {
//         if (this.state.hasError) {
//             return this.props.fallback || (
//                 <div role="alert">
//                     <h2>Something went wrong</h2>
//                     <button onClick={() => this.setState({ hasError: false })}>
//                         Try again
//                     </button>
//                 </div>
//             );
//         }
//         return this.props.children;
//     }
// }

// Usage:
// <ErrorBoundary fallback={<ErrorScreen />}>
//     <UserProfile userId={userId} />
// </ErrorBoundary>

// ============================================================================
// 4. ACCESSIBILITY (a11y)
// ============================================================================

/*
   Accessible React components ensure your app works for all users.
*/

// --- Semantic HTML ---
// function AccessibleArticle({ title, body }) {
//     return (
//         <article aria-labelledby="article-title">
//             <h1 id="article-title">{title}</h1>
//             <p>{body}</p>
//         </article>
//     );
// }

// --- ARIA attributes ---
// function Menu({ items }) {
//     return (
//         <nav aria-label="Main navigation">
//             <ul role="menubar">
//                 {items.map(item => (
//                     <li key={item} role="none">
//                         <a href="#" role="menuitem">{item}</a>
//                     </li>
//                 ))}
//             </ul>
//         </nav>
//     );
// }

// --- Keyboard navigation ---
// function Modal({ isOpen, onClose, children }) {
//     const modalRef = React.useRef(null);
//
//     React.useEffect(() => {
//         if (isOpen) {
//             modalRef.current?.focus();
//             document.body.style.overflow = 'hidden';
//         }
//         return () => { document.body.style.overflow = ''; };
//     }, [isOpen]);
//
//     const handleKeyDown = (e) => {
//         if (e.key === 'Escape') onClose();
//         if (e.key === 'Tab') {
//             // Trap focus within modal
//             const focusable = modalRef.current?.querySelectorAll(
//                 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
//             );
//             if (focusable) {
//                 const first = focusable[0];
//                 const last = focusable[focusable.length - 1];
//                 if (e.shiftKey && document.activeElement === first) {
//                     e.preventDefault();
//                     last.focus();
//                 } else if (!e.shiftKey && document.activeElement === last) {
//                     e.preventDefault();
//                     first.focus();
//                 }
//             }
//         }
//     };
//
//     if (!isOpen) return null;
//
//     return (
//         <div
//             role="dialog"
//             aria-modal="true"
//             aria-labelledby="modal-title"
//             onKeyDown={handleKeyDown}
//             ref={modalRef}
//             tabIndex={-1}
//         >
//             <h2 id="modal-title">Modal Title</h2>
//             {children}
//             <button onClick={onClose} aria-label="Close modal">X</button>
//         </div>
//     );
// }

// ============================================================================
// 5. COMMON ANTI-PATTERNS TO AVOID
// ============================================================================

/*
   Anti-pattern 1: Prop drilling (passing props through many levels)
   Fix: Use Context or composition
   
   Anti-pattern 2: Big component doing too much
   Fix: Split into smaller components with single responsibility
   
   Anti-pattern 3: Using index as key in lists
   Fix: Use unique, stable IDs
   
   Anti-pattern 4: Mutating state directly
   Fix: Always use setState with immutable updates
   
   Anti-pattern 5: Overusing useEffect for derived state
   Fix: Compute derived values during render (useMemo)
   
   Anti-pattern 6: Fetching in useEffect without cleanup
   Fix: Use AbortController or custom hooks
   
   Anti-pattern 7: Putting everything in global state
   Fix: Keep state local, lift only when needed
   
   Anti-pattern 8: Not handling loading/error states
   Fix: Always handle all states (loading, success, error, empty)
*/

// ============================================================================
// 6. CUSTOM HOOKS FOR LOGIC EXTRACTION
// ============================================================================

/*
   Extract reusable logic into custom hooks.
   Keeps components clean and logic testable.
*/

// Instead of this in a component:
// const [isOnline, setIsOnline] = React.useState(navigator.onLine);
// React.useEffect(() => {
//     const handleOnline = () => setIsOnline(true);
//     const handleOffline = () => setIsOnline(false);
//     window.addEventListener('online', handleOnline);
//     window.addEventListener('offline', handleOffline);
//     return () => {
//         window.removeEventListener('online', handleOnline);
//         window.removeEventListener('offline', handleOffline);
//     };
// }, []);

// Extract to:
// function useOnlineStatus() {
//     const [isOnline, setIsOnline] = React.useState(navigator.onLine);
//
//     React.useEffect(() => {
//         const handleOnline = () => setIsOnline(true);
//         const handleOffline = () => setIsOnline(false);
//         window.addEventListener('online', handleOnline);
//         window.addEventListener('offline', handleOffline);
//         return () => {
//             window.removeEventListener('online', handleOnline);
//             window.removeEventListener('offline', handleOffline);
//         };
//     }, []);
//
//     return isOnline;
// }

// ============================================================================
// 7. PERFORMANCE CHECKLIST
// ============================================================================

/*
   Before shipping:
   [ ] Bundle size optimized (code splitting, tree shaking)
   [ ] Images optimized (lazy loading, proper formats)
   [ ] No unnecessary re-renders (React.memo, useCallback, useMemo)
   [ ] Long lists virtualized
   [ ] API calls cached (React Query/SWR)
   [ ] Debounced search inputs
   [ ] Production build tested
   [ ] Lighthouse audit passed
   
   Before committing:
   [ ] TypeScript compiles without errors
   [ ] Tests pass
   [ ] Linting passes
   [ ] No console.log left in
   [ ] Error boundaries in place
   [ ] Accessibility checked (keyboard nav, screen reader)
*/

// ============================================================================
// 8. FINAL BEST PRACTICES SUMMARY
// ============================================================================

/*
   1. Components: small, focused, single responsibility
   2. State: as local as possible, lift only when needed
   3. Hooks: custom hooks for reusable logic
   4. Performance: measure before optimizing
   5. Testing: test behavior, not implementation
   6. Accessibility: semantic HTML, keyboard nav, ARIA
   7. Error handling: error boundaries, try/catch in async
   8. TypeScript: typed props, events, and state
   9. Folder structure: feature-based organization
   10. Consistency: agree on patterns with your team
*/

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Feature-based folder structure scales well");
console.log("2. Compound components for flexible APIs");
console.log("3. Error boundaries prevent full app crashes");
console.log("4. Accessibility is not optional (semantic HTML, ARIA)");
console.log("5. Avoid prop drilling, state mutation, index-as-key");
console.log("6. Extract logic into custom hooks");
console.log("7. Handle all states: loading, success, error, empty");
console.log("=".repeat(80));

export default {};

