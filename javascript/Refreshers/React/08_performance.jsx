/**
 * REACT PERFORMANCE
 * ==================
 * React.memo, useCallback, useMemo, code splitting, virtualization
 */

import React, { useState, useCallback, useMemo, memo, lazy, Suspense } from 'react';

console.log("=".repeat(80));
console.log("REACT PERFORMANCE");
console.log("=".repeat(80));

// ============================================================================
// 1. React.memo (Component Memoization)
// ============================================================================

/*
   React.memo prevents re-rendering if props haven't changed (shallow comparison).
   Use when a component re-renders often with the same props.
*/

const ExpensiveList = memo(function ExpensiveList({ items, onItemClick }) {
    console.log('ExpensiveList rendered');
    return (
        <ul>
            {items.map(item => (
                <li key={item.id} onClick={() => onItemClick(item.id)}>
                    {item.name}
                </li>
            ))}
        </ul>
    );
});

// Custom comparison function
const ListWithCustomCompare = memo(
    function List({ items }) {
        return <ul>{items.map(i => <li key={i.id}>{i.name}</li>)}</ul>;
    },
    (prevProps, nextProps) => {
        // Only re-render if items length changed
        return prevProps.items.length === nextProps.items.length;
    }
);

// ============================================================================
// 2. useCallback (Memoized Functions)
// ============================================================================

/*
   useCallback returns a memoized function reference.
   Prevents child components from re-rendering when callback hasn't changed.
*/

function ParentComponent() {
    const [count, setCount] = useState(0);
    const [items, setItems] = useState([
        { id: 1, name: 'Apple' },
        { id: 2, name: 'Banana' }
    ]);

    // Without useCallback: new function on every render
    // const handleClick = (id) => console.log('Clicked:', id);

    // With useCallback: same function reference if deps haven't changed
    const handleClick = useCallback((id) => {
        console.log('Clicked:', id);
    }, []);  // Empty deps = never changes

    const addItem = useCallback(() => {
        setItems(prev => [...prev, { id: Date.now(), name: 'New Item' }]);
    }, []);

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(c => c + 1)}>Increment</button>
            <button onClick={addItem}>Add Item</button>
            <ExpensiveList items={items} onItemClick={handleClick} />
        </div>
    );
}

// ============================================================================
// 3. useMemo (Memoized Values)
// ============================================================================

/*
   useMemo caches the result of an expensive calculation.
   Only recomputes when dependencies change.
*/

function AnalyticsDashboard({ transactions, users }) {
    // Expensive calculation: only recompute when transactions change
    const totals = useMemo(() => {
        console.log('Computing totals...');
        return transactions.reduce(
            (acc, t) => ({
                revenue: acc.revenue + t.amount,
                count: acc.count + 1
            }),
            { revenue: 0, count: 0 }
        );
    }, [transactions]);

    // Derived data: only recompute when users change
    const activeUsers = useMemo(() => {
        console.log('Filtering active users...');
        return users.filter(u => u.isActive);
    }, [users]);

    // Sorted data
    const sortedTransactions = useMemo(() => {
        return [...transactions].sort((a, b) => b.amount - a.amount);
    }, [transactions]);

    return (
        <div>
            <p>Revenue: ${totals.revenue}</p>
            <p>Transactions: {totals.count}</p>
            <p>Active Users: {activeUsers.length}</p>
        </div>
    );
}

// ============================================================================
// 4. CODE SPLITTING (React.lazy + Suspense)
// ============================================================================

/*
   Split your bundle into smaller chunks loaded on demand.
   Reduces initial load time for large applications.
*/

// --- Lazy load a component ---
// const HeavyComponent = lazy(() => import('./HeavyComponent'));
// const AdminPanel = lazy(() => import('./pages/AdminPanel'));
//
// function App() {
//     const [showAdmin, setShowAdmin] = useState(false);
//
//     return (
//         <div>
//             <button onClick={() => setShowAdmin(true)}>
//                 Open Admin Panel
//             </button>
//
//             <Suspense fallback={<div>Loading admin panel...</div>}>
//                 {showAdmin && <AdminPanel />}
//             </Suspense>
//         </div>
//     );
// }

// ============================================================================
// 5. VIRTUALIZATION (react-window)
// ============================================================================

/*
   Virtualization only renders visible items in a long list.
   Essential for lists with thousands of items.
   
   // install: npm install react-window
   
   import { FixedSizeList, VariableSizeList } from 'react-window';
*/

// --- Fixed size list ---
// const items = Array.from({ length: 10000 }, (_, i) => `Item ${i}`);
//
// function VirtualList() {
//     const Row = ({ index, style }) => (
//         <div style={style}>
//             {items[index]}
//         </div>
//     );
//
//     return (
//         <FixedSizeList
//             height={400}
//             itemCount={items.length}
//             itemSize={35}
//             width={300}
//         >
//             {Row}
//         </FixedSizeList>
//     );
// }

// ============================================================================
// 6. AVOIDING UNNECESSARY RE-RENDERS
// ============================================================================

/*
   Common causes of unnecessary re-renders and how to fix them.
*/

// --- Problem 1: Inline objects/arrays create new references ---
// BAD: <User style={{ color: 'red' }} />  // New object every render
// GOOD: const style = useMemo(() => ({ color: 'red' }), []);
//       <User style={style} />

// --- Problem 2: Inline functions ---
// BAD: <button onClick={() => handleClick(id)} />
// GOOD: const handleClick = useCallback(() => ..., []);
//       <button onClick={handleClick} />

// --- Problem 3: Lifting state too high ---
// BAD: State in parent causes all children to re-render
// GOOD: Keep state as close to where it's used as possible

// --- Problem 4: Context causing wide re-renders ---
// BAD: Single context with all state
// GOOD: Split contexts by concern (ThemeContext, UserContext, etc.)

// ============================================================================
// 7. PROFILING
// ============================================================================

/*
   React DevTools Profiler helps identify performance bottlenecks.
   
   // In browser DevTools > React > Profiler
   // Record interactions and inspect component render times
   
   // Programmatic profiling:
   // import { unstable_trace as trace } from 'scheduler/tracing';
   //
   // trace('Button click', performance.now(), () => {
   //     setCount(c => c + 1);
   // });
*/

// ============================================================================
// 8. DEBOUNCING AND THROTTLING
// ============================================================================

/*
   Debounce: delay execution until after a pause (search input)
   Throttle: limit execution rate (scroll handler, resize)
*/

// Debounce hook
function useDebounce(value, delay = 300) {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const timeout = setTimeout(() => setDebouncedValue(value), delay);
        return () => clearTimeout(timeout);
    }, [value, delay]);

    return debouncedValue;
}

// Usage:
// function SearchInput() {
//     const [query, setQuery] = useState('');
//     const debouncedQuery = useDebounce(query, 500);
//
//     useEffect(() => {
//         if (debouncedQuery) {
//             fetchResults(debouncedQuery);
//         }
//     }, [debouncedQuery]);
//
//     return <input value={query} onChange={e => setQuery(e.target.value)} />;
// }

// ============================================================================
// 9. PERFORMANCE CHECKLIST
// ============================================================================

/*
   Before optimizing, measure first!
   
   1. Identify slow renders with React DevTools Profiler
   2. Check for unnecessary re-renders (Why Did You Render? library)
   3. Apply React.memo to pure presentational components
   4. Memoize callbacks with useCallback
   5. Memoize expensive computations with useMemo
   6. Lazy load routes and heavy components
   7. Virtualize long lists
   8. Debounce search inputs and expensive handlers
   9. Split context to avoid wide re-renders
   10. Use production build for performance testing
*/

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. React.memo prevents re-renders when props haven't changed");
console.log("2. useCallback memoizes function references");
console.log("3. useMemo caches expensive calculations");
console.log("4. React.lazy + Suspense for code splitting");
console.log("5. Virtualization for long lists (react-window)");
console.log("6. Avoid inline objects/functions in render");
console.log("7. Profile before optimizing (measure, don't guess)");
console.log("=".repeat(80));

export default ParentComponent;

