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

function Counter() {
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>Increment</button>
            <button onClick={() => setCount(count - 1)}>Decrement</button>
            <button onClick={() => setCount(0)}>Reset</button>
        </div>
    );
}

// Multiple state variables
function Form() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [age, setAge] = useState(0);
    
    return (
        <form>
            <input value={name} onChange={(e) => setName(e.target.value)} />
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
            <input value={age} onChange={(e) => setAge(Number(e.target.value))} />
        </form>
    );
}

// State with objects
function UserForm() {
    const [user, setUser] = useState({ name: '', email: '', age: 0 });
    
    const handleChange = (field, value) => {
        setUser(prev => ({ ...prev, [field]: value }));
    };
    
    return (
        <form>
            <input 
                value={user.name} 
                onChange={(e) => handleChange('name', e.target.value)} 
            />
        </form>
    );
}

// ============================================================================
// 2. useEffect - SIDE EFFECTS
// ============================================================================

// Run on every render
function EveryRender() {
    useEffect(() => {
        console.log('Component rendered');
    });
    return <div>Check console</div>;
}

// Run only on mount
function OnMount() {
    useEffect(() => {
        console.log('Component mounted');
        return () => console.log('Component unmounted');
    }, []);
    return <div>Mounted</div>;
}

// Run when dependencies change
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    
    useEffect(() => {
        fetch(`/api/users/${userId}`)
            .then(res => res.json())
            .then(data => setUser(data));
    }, [userId]);  // Re-run when userId changes
    
    return user ? <div>{user.name}</div> : <div>Loading...</div>;
}

// Cleanup function
function Timer() {
    const [seconds, setSeconds] = useState(0);
    
    useEffect(() => {
        const interval = setInterval(() => {
            setSeconds(s => s + 1);
        }, 1000);
        
        // Cleanup
        return () => clearInterval(interval);
    }, []);
    
    return <div>Seconds: {seconds}</div>;
}

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
