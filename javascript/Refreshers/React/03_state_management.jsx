/**
 * REACT STATE MANAGEMENT
 * =======================
 * Lifting state up, Context API, useReducer patterns, Redux Toolkit, Zustand
 */

import React, { useState, useContext, createContext, useReducer } from 'react';

console.log("=".repeat(80));
console.log("REACT STATE MANAGEMENT");
console.log("=".repeat(80));

// ============================================================================
// 1. LIFTING STATE UP
// ============================================================================

/*
   When multiple components need to share state, lift it to their
   closest common ancestor. Pass data down via props, changes up via callbacks.
*/

function TemperatureInput({ scale, temperature, onTemperatureChange }) {
    const scaleNames = { c: 'Celsius', f: 'Fahrenheit' };

    return (
        <fieldset>
            <legend>Enter temperature in {scaleNames[scale]}:</legend>
            <input
                value={temperature}
                onChange={(e) => onTemperatureChange(e.target.value)}
                type="number"
            />
        </fieldset>
    );
}

function BoilingVerdict({ celsius }) {
    if (celsius >= 100) return <p>The water would boil.</p>;
    return <p>The water would not boil.</p>;
}

// Shared conversion logic
function toCelsius(fahrenheit) { return ((fahrenheit - 32) * 5) / 9; }
function toFahrenheit(celsius) { return (celsius * 9) / 5 + 32; }

function tryConvert(temperature, convert) {
    const input = parseFloat(temperature);
    if (Number.isNaN(input)) return '';
    const output = convert(input);
    const rounded = Math.round(output * 1000) / 1000;
    return rounded.toString();
}

// Parent component holds the shared state
function Calculator() {
    const [temperature, setTemperature] = useState('');
    const [scale, setScale] = useState('c');

    const handleCelsiusChange = (value) => {
        setTemperature(value);
        setScale('c');
    };

    const handleFahrenheitChange = (value) => {
        setTemperature(value);
        setScale('f');
    };

    const celsius = scale === 'f' ? tryConvert(temperature, toCelsius) : temperature;
    const fahrenheit = scale === 'c' ? tryConvert(temperature, toFahrenheit) : temperature;

    return (
        <div>
            <TemperatureInput
                scale="c"
                temperature={celsius}
                onTemperatureChange={handleCelsiusChange}
            />
            <TemperatureInput
                scale="f"
                temperature={fahrenheit}
                onTemperatureChange={handleFahrenheitChange}
            />
            <BoilingVerdict celsius={parseFloat(celsius)} />
        </div>
    );
}

// ============================================================================
// 2. CONTEXT API - BASIC
// ============================================================================

/*
   Context provides a way to pass data through the component tree
   without manually passing props at every level (prop drilling).
*/

// Create context with default value
const ThemeContext = createContext('light');

function ThemedButton() {
    const theme = useContext(ThemeContext);
    return <button className={`btn-${theme}`}>Themed Button ({theme})</button>;
}

function ThemedToolbar() {
    return (
        <div>
            <ThemedButton />
            <ThemedButton />
        </div>
    );
}

function ThemeApp() {
    return (
        <ThemeContext.Provider value="dark">
            <ThemedToolbar />
        </ThemeContext.Provider>
    );
}

// ============================================================================
// 3. CONTEXT + USEREDUCER (Global State Pattern)
// ============================================================================

/*
   Combine Context with useReducer for a lightweight Redux-like pattern.
   This is a common pattern for medium-sized apps.
*/

// Action types
const ACTIONS = {
    ADD_TODO: 'ADD_TODO',
    TOGGLE_TODO: 'TOGGLE_TODO',
    DELETE_TODO: 'DELETE_TODO',
    SET_FILTER: 'SET_FILTER'
};

// Reducer
function todoReducer(state, action) {
    switch (action.type) {
        case ACTIONS.ADD_TODO:
            return {
                ...state,
                todos: [
                    ...state.todos,
                    {
                        id: Date.now(),
                        text: action.payload,
                        completed: false
                    }
                ]
            };
        case ACTIONS.TOGGLE_TODO:
            return {
                ...state,
                todos: state.todos.map(todo =>
                    todo.id === action.payload
                        ? { ...todo, completed: !todo.completed }
                        : todo
                )
            };
        case ACTIONS.DELETE_TODO:
            return {
                ...state,
                todos: state.todos.filter(todo => todo.id !== action.payload)
            };
        case ACTIONS.SET_FILTER:
            return { ...state, filter: action.payload };
        default:
            return state;
    }
}

// Create context
const TodoContext = createContext(null);
const TodoDispatchContext = createContext(null);

// Provider component
function TodoProvider({ children }) {
    const [state, dispatch] = useReducer(todoReducer, {
        todos: [],
        filter: 'all'
    });

    return (
        <TodoContext.Provider value={state}>
            <TodoDispatchContext.Provider value={dispatch}>
                {children}
            </TodoDispatchContext.Provider>
        </TodoContext.Provider>
    );
}

// Custom hooks for consuming context
function useTodos() {
    const context = useContext(TodoContext);
    if (!context) throw new Error('useTodos must be used within TodoProvider');
    return context;
}

function useTodoDispatch() {
    const context = useContext(TodoDispatchContext);
    if (!context) throw new Error('useTodoDispatch must be used within TodoProvider');
    return context;
}

// Components using the context
function TodoList() {
    const { todos, filter } = useTodos();
    const dispatch = useTodoDispatch();

    const filteredTodos = todos.filter(todo => {
        if (filter === 'active') return !todo.completed;
        if (filter === 'completed') return todo.completed;
        return true;
    });

    return (
        <ul>
            {filteredTodos.map(todo => (
                <li key={todo.id}>
                    <span
                        style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}
                        onClick={() => dispatch({ type: ACTIONS.TOGGLE_TODO, payload: todo.id })}
                    >
                        {todo.text}
                    </span>
                    <button onClick={() => dispatch({ type: ACTIONS.DELETE_TODO, payload: todo.id })}>
                        Delete
                    </button>
                </li>
            ))}
        </ul>
    );
}

function AddTodo() {
    const dispatch = useTodoDispatch();
    const [text, setText] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!text.trim()) return;
        dispatch({ type: ACTIONS.ADD_TODO, payload: text });
        setText('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <input value={text} onChange={(e) => setText(e.target.value)} />
            <button type="submit">Add Todo</button>
        </form>
    );
}

function FilterButtons() {
    const dispatch = useTodoDispatch();
    return (
        <div>
            <button onClick={() => dispatch({ type: ACTIONS.SET_FILTER, payload: 'all' })}>All</button>
            <button onClick={() => dispatch({ type: ACTIONS.SET_FILTER, payload: 'active' })}>Active</button>
            <button onClick={() => dispatch({ type: ACTIONS.SET_FILTER, payload: 'completed' })}>Completed</button>
        </div>
    );
}

function TodoApp() {
    return (
        <TodoProvider>
            <h2>Todo App (Context + useReducer)</h2>
            <AddTodo />
            <FilterButtons />
            <TodoList />
        </TodoProvider>
    );
}

// ============================================================================
// 4. REDUX TOOLKIT PATTERN
// ============================================================================

/*
   Redux Toolkit (RTK) is the modern way to write Redux.
   It reduces boilerplate significantly compared to vanilla Redux.
   
   // install: npm install @reduxjs/toolkit react-redux
   
   import { createSlice, configureStore } from '@reduxjs/toolkit';
   import { Provider, useSelector, useDispatch } from 'react-redux';
*/

// --- Slice (reducer + actions together) ---
// const counterSlice = createSlice({
//     name: 'counter',
//     initialState: { value: 0 },
//     reducers: {
//         increment: (state) => { state.value += 1; },
//         decrement: (state) => { state.value -= 1; },
//         incrementByAmount: (state, action) => { state.value += action.payload; }
//     }
// });

// --- Store ---
// const store = configureStore({
//     reducer: {
//         counter: counterSlice.reducer
//     }
// });

// --- Usage in components ---
// function Counter() {
//     const count = useSelector((state) => state.counter.value);
//     const dispatch = useDispatch();
//
//     return (
//         <div>
//             <span>{count}</span>
//             <button onClick={() => dispatch(counterSlice.actions.increment())}>+</button>
//             <button onClick={() => dispatch(counterSlice.actions.decrement())}>-</button>
//         </div>
//     );
// }

// --- App wrapper ---
// function App() {
//     return (
//         <Provider store={store}>
//             <Counter />
//         </Provider>
//     );
// }

// ============================================================================
// 5. ZUSTAND (Lightweight State Management)
// ============================================================================

/*
   Zustand is a minimal state management library.
   No providers, no boilerplate, just a hook.
   
   // install: npm install zustand
   
   import { create } from 'zustand';
*/

// --- Store definition ---
// const useStore = create((set) => ({
//     count: 0,
//     increment: () => set((state) => ({ count: state.count + 1 })),
//     decrement: () => set((state) => ({ count: state.count - 1 })),
//     reset: () => set({ count: 0 })
// }));

// --- Usage ---
// function Counter() {
//     const count = useStore((state) => state.count);
//     const increment = useStore((state) => state.increment);
//     const decrement = useStore((state) => state.decrement);
//
//     return (
//         <div>
//             <span>{count}</span>
//             <button onClick={increment}>+</button>
//             <button onClick={decrement}>-</button>
//         </div>
//     );
// }

// ============================================================================
// 6. WHEN TO USE WHAT
// ============================================================================

/*
   Approach           | Best For                          | When to Avoid
   -------------------|-----------------------------------|---------------------------
   useState           | Local component state             | Shared state between far components
   Lifting state up   | Sibling communication             | Deep prop drilling (>3 levels)
   Context + useReducer| Medium app, global UI state      | High-frequency updates (perf)
   Redux Toolkit      | Large apps, complex state, team   | Simple apps (overkill)
   Zustand            | Simple global state, small-medium | Complex middleware needs
   React Query/SWR    | Server state (API data)           | Client-only state
*/

// ============================================================================
// 7. BEST PRACTICES
// ============================================================================

/*
   1. Keep state as local as possible (start with useState)
   2. Lift state up only when truly needed
   3. Split contexts to avoid unnecessary re-renders
   4. Use useReducer for complex state logic (multiple sub-values)
   5. Keep reducers pure (no side effects)
   6. Use selectors to minimize re-renders
   7. Normalize nested state (like a database)
   8. Consider server state vs client state separately
   9. Avoid putting derived state in state (compute it)
   10. Use TypeScript for better state management DX
*/

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Lift state to common ancestor for sibling sharing");
console.log("2. Context avoids prop drilling but watch re-renders");
console.log("3. Context + useReducer = lightweight Redux alternative");
console.log("4. Redux Toolkit for complex apps with devtools");
console.log("5. Zustand for simple, no-boilerplate global state");
console.log("6. React Query for server state (caching, refetching)");
console.log("7. Start simple, add complexity only when needed");
console.log("=".repeat(80));

export default Calculator;

