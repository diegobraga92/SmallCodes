/**
 * REACT HOOKS
 * ============
 * useState, useEffect, useContext, useReducer, custom hooks
 */

import React, { useState, useEffect, useContext, useReducer, useRef, useMemo, useCallback } from 'react';

console.log("=".repeat(80));
console.log("REACT HOOKS");
console.log("=".repeat(80));

// ============================================================================
// 1. useState - STATE MANAGEMENT
// ============================================================================

/**
 * useState EXPLAINED:
 * ==================
 * 
 * const [state, setState] = useState(initialValue);
 * 
 * RETURNS:
 * - state: Current state value
 * - setState: Function to update state
 * 
 * KEY CONCEPTS:
 * 
 * 1. STATE UPDATES ARE ASYNCHRONOUS:
 *    setState doesn't immediately update state
 *    Re-render is scheduled, then state updates
 * 
 * 2. AUTOMATIC BATCHING (React 18+):
 *    Multiple setState calls in same event are batched
 *    Only triggers ONE re-render
 *    
 *    Before React 18: Only batched in event handlers
 *    React 18+: Batched everywhere (promises, timeouts, etc.)
 * 
 * 3. FUNCTIONAL UPDATES:
 *    setState(prevState => newState)
 *    USE WHEN: New state depends on previous state
 *    WHY: Ensures you work with latest state (batching-safe)
 * 
 * 4. STATE INITIALIZATION:
 *    - useState(value): Re-runs on every render
 *    - useState(() => value): Only runs once (lazy initialization)
 *    - Use function for expensive initialization
 * 
 * 5. STATE SHOULD BE IMMUTABLE:
 *    Don't mutate objects/arrays directly
 *    Create new object/array with changes
 * 
 * WHEN TO USE MULTIPLE useState vs SINGLE OBJECT:
 * - Multiple useState: Independent values that change separately
 * - Single object: Related values that change together
 */

function Counter() {
    // BASIC useState USAGE:
    // Initial value: 0
    // count: current state
    // setCount: update function
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>Count: {count}</p>
            
            {/* WRONG: setCount(count + 1) multiple times won't work */}
            {/* WHY? 'count' is stale within same render */}
            <button onClick={() => {
                // setCount(count + 1);  // count = 0, sets to 1
                // setCount(count + 1);  // count = 0, sets to 1 again!
                // Result: only increments by 1, not 2
            }}>Wrong Way</button>
            
            {/* RIGHT: Use functional update for multiple updates */}
            <button onClick={() => {
                // These are batched but use latest state
                setCount(c => c + 1);  // c = 0, sets to 1
                setCount(c => c + 1);  // c = 1, sets to 2
                // Result: increments by 2 ✓
            }}>Increment Twice</button>
            
            <button onClick={() => setCount(count + 1)}>Increment</button>
            <button onClick={() => setCount(count - 1)}>Decrement</button>
            <button onClick={() => setCount(0)}>Reset</button>
        </div>
    );
}

// Multiple state variables
function Form() {
    // SEPARATE STATE FOR INDEPENDENT VALUES:
    // Each can update independently without affecting others
    // React only re-renders when specific state changes
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [age, setAge] = useState(0);
    
    // BATCHING IN ACTION:
    // If all three setState calls happen in same event,
    // React batches them into ONE re-render (React 18+)
    const handleSubmit = () => {
        setName('Alice');
        setEmail('alice@example.com');
        setAge(30);
        // Only ONE re-render happens! (not three)
    };
    
    return (
        <form>
            <input value={name} onChange={(e) => setName(e.target.value)} />
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
            <input value={age} onChange={(e) => setAge(Number(e.target.value))} />
            <button onClick={handleSubmit}>Submit</button>
        </form>
    );
}

// State with objects
function UserForm() {
    // SINGLE STATE FOR RELATED VALUES:
    // All user fields are related, update together
    const [user, setUser] = useState({ name: '', email: '', age: 0 });
    
    const handleChange = (field, value) => {
        // IMPORTANT: Spread previous state to preserve other fields
        // React does SHALLOW comparison - must create new object
        setUser(prev => ({ ...prev, [field]: value }));
        
        // WRONG: Mutating state directly
        // user[field] = value;  // ✗ React won't detect change
        // setUser(user);        // ✗ Same reference, no re-render
    };
    
    // LAZY INITIALIZATION EXAMPLE:
    // const [expensive] = useState(() => {
    //     // This function only runs ONCE on mount
    //     // Not on every re-render
    //     return computeExpensiveValue();
    // });
    
    return (
        <form>
            <input 
                value={user.name} 
                onChange={(e) => handleChange('name', e.target.value)} 
            />
            <input 
                value={user.email} 
                onChange={(e) => handleChange('email', e.target.value)} 
            />
        </form>
    );
}

/**
 * useState COMMON PITFALLS:
 * 
 * 1. STALE CLOSURE:
 *    setTimeout(() => setCount(count + 1), 1000);
 *    // 'count' is captured at setTimeout call time
 *    // Use functional update: setCount(c => c + 1)
 * 
 * 2. UNNECESSARY RE-RENDERS:
 *    setUser({ ...user });  // New object but same values
 *    // React still re-renders (shallow comparison)
 *    // Only call setState when value actually changes
 * 
 * 3. OBJECT MUTATION:
 *    const newUser = user;
 *    newUser.name = 'Alice';
 *    setUser(newUser);  // Same reference, no re-render!
 *    // Must create new object: setUser({ ...user, name: 'Alice' })
 */

// ============================================================================
// 2. useEffect - SIDE EFFECTS
// ============================================================================

/**
 * useEffect EXPLAINED:
 * ===================
 * 
 * useEffect(effectFunction, dependencyArray);
 * 
 * PURPOSE:
 * Run side effects (API calls, subscriptions, DOM manipulation)
 * after render commits to screen
 * 
 * EXECUTION TIMING:
 * 1. Component renders
 * 2. React updates DOM
 * 3. Browser paints screen
 * 4. useEffect runs (AFTER paint, non-blocking)
 * 
 * DEPENDENCY ARRAY BEHAVIOR:
 * 
 * - No array: useEffect(() => {})
 *   Runs after EVERY render (usually wrong!)
 * 
 * - Empty array: useEffect(() => {}, [])
 *   Runs ONCE on mount only
 * 
 * - With deps: useEffect(() => {}, [a, b])
 *   Runs on mount + when a or b changes
 *   Comparison uses Object.is (like ===)
 * 
 * CLEANUP FUNCTION:
 * - Return function from effect
 * - Runs BEFORE next effect
 * - Runs on unmount
 * - Critical for: timers, subscriptions, event listeners
 * 
 * EXECUTION ORDER:
 * 1. Cleanup from previous effect (if exists)
 * 2. New effect runs
 * 3. On unmount: Final cleanup
 * 
 * COMMON PITFALLS:
 * 1. Missing dependencies (ESLint exhaustive-deps)
 * 2. Object/array deps cause infinite loops
 * 3. Forgetting cleanup (memory leaks)
 * 4. Effect depends on stale closure
 */

// Run on every render (RARE - usually a mistake!)
function EveryRender() {
    useEffect(() => {
        // NO DEPENDENCY ARRAY = runs after every render
        // Usually wrong! Causes performance issues
        // Only use when you truly need to sync with every render
        console.log('Component rendered');
    });
    // WARNING: If this effect calls setState, infinite loop!
    return <div>Check console</div>;
}

// Run only on mount (COMMON - initialization)
function OnMount() {
    useEffect(() => {
        // EMPTY ARRAY [] = runs once on mount
        // Perfect for: API calls, subscriptions, one-time setup
        console.log('Component mounted');
        
        // Cleanup runs on unmount
        return () => {
            console.log('Component unmounted');
            // Clean up: cancel subscriptions, remove listeners, etc.
        };
    }, []);  // Empty deps = mount/unmount only
    
    return <div>Mounted</div>;
}

// Run when dependencies change (MOST COMMON)
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    
    useEffect(() => {
        // Runs when userId changes
        // Effect body should ONLY use values from deps array
        
        // DEPENDENCY COMPARISON:
        // React uses Object.is(prevUserId, newUserId)
        // For primitives (string, number): works perfectly
        // For objects/arrays: compares REFERENCE, not contents
        
        fetch(`/api/users/${userId}`)
            .then(res => res.json())
            .then(data => setUser(data));
            
        // RACE CONDITION WARNING:
        // If userId changes rapidly, responses may arrive out of order
        // Fix: Use cleanup with AbortController (see advanced patterns)
    }, [userId]);  // Re-run when userId changes
    
    // IMPORTANT: userId MUST be in dependency array
    // If omitted, effect uses stale userId
    // ESLint rule 'exhaustive-deps' catches this
    
    return user ? <div>{user.name}</div> : <div>Loading...</div>;
}

// Cleanup function (CRITICAL for memory leaks)
function Timer() {
    const [seconds, setSeconds] = useState(0);
    
    useEffect(() => {
        // Setup: Create interval
        const interval = setInterval(() => {
            // Use functional update to avoid stale closure
            // setSeconds(seconds + 1) would be WRONG (stale)
            setSeconds(s => s + 1);  // Always uses latest state ✓
        }, 1000);
        
        // Cleanup: Clear interval
        return () => {
            clearInterval(interval);
            // WHY CLEANUP?
            // Without cleanup:
            // 1. Component unmounts
            // 2. Interval keeps running (memory leak!)
            // 3. Calls setState on unmounted component (error/warning)
            
            // Cleanup runs:
            // - Before next effect (if deps changed)
            // - On component unmount
        };
    }, []);  // Empty deps = interval never recreated
    
    return <div>Seconds: {seconds}</div>;
}

/**
 * useEffect ADVANCED PATTERNS:
 * 
 * 1. PREVENTING RACE CONDITIONS:
 *    useEffect(() => {
 *        let cancelled = false;
 *        fetchUser(userId).then(user => {
 *            if (!cancelled) setUser(user);
 *        });
 *        return () => { cancelled = true; };
 *    }, [userId]);
 * 
 * 2. ABORT CONTROLLER (Modern):
 *    useEffect(() => {
 *        const controller = new AbortController();
 *        fetch(url, { signal: controller.signal })
 *            .then(...)
 *            .catch(err => {
 *                if (err.name !== 'AbortError') throw err;
 *            });
 *        return () => controller.abort();
 *    }, [url]);
 * 
 * 3. AVOIDING OBJECT/ARRAY DEPS:
 *    // BAD: Object changes every render
 *    const config = { userId, type };
 *    useEffect(() => {...}, [config]);  // Infinite loop!
 *    
 *    // GOOD: Use primitive deps
 *    useEffect(() => {...}, [userId, type]);
 * 
 * 4. MULTIPLE EFFECTS:
 *    Separate concerns into different useEffect calls
 *    Better for readability and cleanup management
 */

// ============================================================================
// 3. useContext - GLOBAL STATE
// ============================================================================

const ThemeContext = React.createContext('light');

function ThemedButton() {
    const theme = useContext(ThemeContext);
    return <button className={theme}>Themed Button</button>;
}

function App() {
    return (
        <ThemeContext.Provider value="dark">
            <ThemedButton />
        </ThemeContext.Provider>
    );
}

// ============================================================================
// 4. useReducer - COMPLEX STATE
// ============================================================================

const initialState = { count: 0 };

function reducer(state, action) {
    switch (action.type) {
        case 'increment':
            return { count: state.count + 1 };
        case 'decrement':
            return { count: state.count - 1 };
        case 'reset':
            return initialState;
        default:
            throw new Error();
    }
}

function CounterWithReducer() {
    const [state, dispatch] = useReducer(reducer, initialState);
    
    return (
        <div>
            <p>Count: {state.count}</p>
            <button onClick={() => dispatch({ type: 'increment' })}>+</button>
            <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
            <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
        </div>
    );
}

// ============================================================================
// 5. useRef - DOM REFERENCES AND MUTABLE VALUES
// ============================================================================

function FocusInput() {
    const inputRef = useRef(null);
    
    const handleClick = () => {
        inputRef.current.focus();
    };
    
    return (
        <div>
            <input ref={inputRef} />
            <button onClick={handleClick}>Focus Input</button>
        </div>
    );
}

// Storing mutable value without re-render
function TimerWithRef() {
    const [count, setCount] = useState(0);
    const intervalRef = useRef(null);
    
    const start = () => {
        intervalRef.current = setInterval(() => {
            setCount(c => c + 1);
        }, 1000);
    };
    
    const stop = () => {
        clearInterval(intervalRef.current);
    };
    
    return (
        <div>
            <p>{count}</p>
            <button onClick={start}>Start</button>
            <button onClick={stop}>Stop</button>
        </div>
    );
}

// ============================================================================
// 6. useMemo - MEMOIZATION
// ============================================================================

function ExpensiveComponent({ items }) {
    const expensiveCalculation = useMemo(() => {
        console.log('Computing...');
        return items.reduce((acc, item) => acc + item, 0);
    }, [items]);  // Only recompute when items change
    
    return <div>Sum: {expensiveCalculation}</div>;
}

// ============================================================================
// 7. useCallback - MEMOIZED CALLBACKS
// ============================================================================

function ParentComponent() {
    const [count, setCount] = useState(0);
    
    // Memoized callback
    const handleClick = useCallback(() => {
        console.log('Button clicked');
    }, []);  // Never changes
    
    return (
        <div>
            <ChildComponent onClick={handleClick} />
            <button onClick={() => setCount(count + 1)}>
                Parent Count: {count}
            </button>
        </div>
    );
}

const ChildComponent = React.memo(({ onClick }) => {
    console.log('Child rendered');
    return <button onClick={onClick}>Click me</button>;
});

// ============================================================================
// 8. CUSTOM HOOKS
// ============================================================================

// Custom hook for fetching data
function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        setLoading(true);
        fetch(url)
            .then(res => res.json())
            .then(data => {
                setData(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err);
                setLoading(false);
            });
    }, [url]);
    
    return { data, loading, error };
}

// Usage
function UserList() {
    const { data, loading, error } = useFetch('/api/users');
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;
    return <ul>{data.map(user => <li key={user.id}>{user.name}</li>)}</ul>;
}

// Custom hook for local storage
function useLocalStorage(key, initialValue) {
    const [value, setValue] = useState(() => {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : initialValue;
    });
    
    const setStoredValue = (newValue) => {
        setValue(newValue);
        localStorage.setItem(key, JSON.stringify(newValue));
    };
    
    return [value, setStoredValue];
}

// ============================================================================
// 9. HOOKS RULES
// ============================================================================

/**
 * RULES OF HOOKS:
 * 
 * 1. ONLY CALL AT TOP LEVEL
 *    - Don't call in loops, conditions, or nested functions
 *    ✗ if (condition) { useState(0); }
 *    ✓ useState(0);
 * 
 * 2. ONLY CALL FROM REACT FUNCTIONS
 *    - Call from functional components
 *    - Call from custom hooks
 *    ✗ Regular JavaScript functions
 * 
 * 3. CUSTOM HOOKS START WITH "use"
 *    ✓ useCustomHook
 *    ✗ customHook
 */

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/**
 * HOOKS BEST PRACTICES:
 * 
 * 1. DEPENDENCY ARRAYS
 *    - Include all dependencies in useEffect
 *    - Use ESLint plugin (eslint-plugin-react-hooks)
 * 
 * 2. STATE UPDATES
 *    - Use functional updates when depending on previous state
 *    setCount(c => c + 1) instead of setCount(count + 1)
 * 
 * 3. SPLIT STATE
 *    - Multiple useState for unrelated state
 *    - useReducer for complex related state
 * 
 * 4. CUSTOM HOOKS
 *    - Extract reusable logic
 *    - Follow naming convention (useXxx)
 * 
 * 5. MEMOIZATION
 *    - useMemo for expensive calculations
 *    - useCallback for callback stability
 *    - Don't overuse (premature optimization)
 * 
 * 6. CLEANUP
 *    - Return cleanup function from useEffect
 *    - Cancel subscriptions, clear timers
 * 
 * 7. AVOID STALE CLOSURES
 *    - Be careful with closure over state in callbacks
 *    - Use functional updates or include in dependencies
 */

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. useState for component state");
console.log("2. useEffect for side effects and lifecycle");
console.log("3. useContext for global state");
console.log("4. useReducer for complex state logic");
console.log("5. useRef for DOM refs and mutable values");
console.log("6. useMemo/useCallback for optimization");
console.log("7. Custom hooks for reusable logic");
console.log("8. Follow hooks rules (top-level, React functions)");
console.log("=".repeat(80));

export default Counter;
