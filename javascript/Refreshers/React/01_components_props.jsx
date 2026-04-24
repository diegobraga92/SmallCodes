/**
 * REACT COMPONENTS AND PROPS
 * ===========================
 * Functional components, props, prop destructuring, children
 */

import React from 'react';

console.log("=".repeat(80));
console.log("REACT COMPONENTS AND PROPS");
console.log("=".repeat(80));

// ============================================================================
// 1. FUNCTIONAL COMPONENTS
// ============================================================================

// Simple functional component
function Welcome() {
    return <h1>Hello, World!</h1>;
}

// Component with props
function Greeting(props) {
    return <h1>Hello, {props.name}!</h1>;
}

// Usage:
// <Greeting name="Alice" />

// ============================================================================
// 2. PROPS
// ============================================================================

// Multiple props
function UserCard(props) {
    return (
        <div className="user-card">
            <h2>{props.name}</h2>
            <p>Email: {props.email}</p>
            <p>Age: {props.age}</p>
        </div>
    );
}

// Usage:
// <UserCard name="Alice" email="alice@example.com" age={30} />

// ============================================================================
// 3. PROP DESTRUCTURING
// ============================================================================

// Destructure props for cleaner code
function UserProfile({ name, email, age }) {
    return (
        <div className="profile">
            <h2>{name}</h2>
            <p>{email}</p>
            <p>Age: {age}</p>
        </div>
    );
}

// With default values
function Button({ text = "Click me", onClick = () => {} }) {
    return <button onClick={onClick}>{text}</button>;
}

// ============================================================================
// 4. CHILDREN PROP
// ============================================================================

// Children = content between opening and closing tags
function Card({ children, title }) {
    return (
        <div className="card">
            <h3>{title}</h3>
            <div className="card-content">
                {children}
            </div>
        </div>
    );
}

// Usage:
// <Card title="My Card">
//     <p>This is the content</p>
//     <button>Action</button>
// </Card>

// ============================================================================
// 5. PROP TYPES (Runtime validation)
// ============================================================================

import PropTypes from 'prop-types';

function Product({ name, price, inStock }) {
    return (
        <div>
            <h3>{name}</h3>
            <p>${price.toFixed(2)}</p>
            {inStock && <span>In Stock</span>}
        </div>
    );
}

Product.propTypes = {
    name: PropTypes.string.isRequired,
    price: PropTypes.number.isRequired,
    inStock: PropTypes.bool
};

Product.defaultProps = {
    inStock: true
};

// ============================================================================
// 6. CONDITIONAL RENDERING WITH PROPS
// ============================================================================

function Alert({ type, message }) {
    const alertClass = type === 'error' ? 'alert-error' : 'alert-info';
    
    return (
        <div className={alertClass}>
            {message}
        </div>
    );
}

// Conditional rendering based on props
function UserStatus({ isLoggedIn, username }) {
    if (isLoggedIn) {
        return <p>Welcome back, {username}!</p>;
    }
    return <p>Please log in</p>;
}

// ============================================================================
// 7. RENDERING LISTS WITH PROPS
// ============================================================================

function TodoList({ items }) {
    return (
        <ul>
            {items.map((item, index) => (
                <li key={index}>{item}</li>
            ))}
        </ul>
    );
}

// Usage:
// <TodoList items={['Task 1', 'Task 2', 'Task 3']} />

// ============================================================================
// 8. CALLBACK PROPS (PASSING FUNCTIONS)
// ============================================================================

function TodoItem({ text, onDelete, onToggle }) {
    return (
        <li>
            <input type="checkbox" onChange={onToggle} />
            <span>{text}</span>
            <button onClick={onDelete}>Delete</button>
        </li>
    );
}

// ============================================================================
// 9. COMPOSITION
// ============================================================================

function Layout({ header, sidebar, content }) {
    return (
        <div className="layout">
            <header>{header}</header>
            <aside>{sidebar}</aside>
            <main>{content}</main>
        </div>
    );
}

// Usage:
// <Layout
//     header={<Header />}
//     sidebar={<Sidebar />}
//     content={<MainContent />}
// />

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/**
 * COMPONENT & PROPS BEST PRACTICES:
 * 
 * 1. DESTRUCTURE PROPS
 *    function MyComponent({ name, age }) { }
 * 
 * 2. USE PROP-TYPES OR TYPESCRIPT
 *    Add validation for props
 * 
 * 3. DEFAULT PROPS
 *    Provide sensible defaults
 * 
 * 4. KEEP COMPONENTS SMALL
 *    Single responsibility
 * 
 * 5. USE COMPOSITION
 *    Compose complex UIs from simple components
 * 
 * 6. IMMUTABLE PROPS
 *    Never modify props directly
 * 
 * 7. KEYS IN LISTS
 *    Use stable, unique keys
 * 
 * 8. CALLBACK NAMING
 *    onEventName for props, handleEventName for handlers
 */

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Functional components are the modern standard");
console.log("2. Props pass data from parent to child");
console.log("3. Destructure props for cleaner code");
console.log("4. children prop for component composition");
console.log("5. PropTypes for runtime validation");
console.log("6. Never mutate props");
console.log("7. Use unique keys when rendering lists");
console.log("8. Callback props for parent-child communication");
console.log("=".repeat(80));

export default Welcome;
