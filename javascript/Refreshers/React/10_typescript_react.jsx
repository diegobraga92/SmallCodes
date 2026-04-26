/**
 * REACT WITH TYPESCRIPT
 * ======================
 * Typed components, hooks, events, patterns, generics
 * 
 * NOTE: This file uses .jsx extension but demonstrates TypeScript patterns.
 * In practice, use .tsx extension for TypeScript React files.
 */

import React from 'react';

console.log("=".repeat(80));
console.log("REACT WITH TYPESCRIPT");
console.log("=".repeat(80));

// ============================================================================
// 1. TYPING COMPONENT PROPS
// ============================================================================

/*
   Define props interface/type for each component.
   Use interface for public APIs, type for unions/utility types.
*/

// --- Basic props ---
// interface GreetingProps {
//     name: string;
//     age?: number;  // Optional prop
//     onGreet: (name: string) => void;
// }
//
// function Greeting({ name, age, onGreet }: GreetingProps) {
//     return (
//         <div>
//             <h1>Hello, {name}!</h1>
//             {age && <p>Age: {age}</p>}
//             <button onClick={() => onGreet(name)}>Greet</button>
//         </div>
//     );
// }

// --- With children ---
// interface CardProps {
//     title: string;
//     children: React.ReactNode;  // Any renderable content
// }
//
// function Card({ title, children }: CardProps) {
//     return (
//         <div className="card">
//             <h2>{title}</h2>
//             {children}
//         </div>
//     );
// }

// --- With specific children type ---
// interface ListProps {
//     items: string[];
//     renderItem: (item: string, index: number) => React.ReactNode;
// }

// ============================================================================
// 2. TYPING EVENT HANDLERS
// ============================================================================

// interface FormProps {
//     onSubmit: (data: { email: string; password: string }) => void;
// }
//
// function LoginForm({ onSubmit }: FormProps) {
//     const [email, setEmail] = React.useState('');
//     const [password, setPassword] = React.useState('');
//
//     const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
//         e.preventDefault();
//         onSubmit({ email, password });
//     };
//
//     const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//         setEmail(e.target.value);
//     };
//
//     const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
//         if (e.key === 'Enter') {
//             console.log('Enter pressed');
//         }
//     };
//
//     return (
//         <form onSubmit={handleSubmit}>
//             <input
//                 type="email"
//                 value={email}
//                 onChange={handleEmailChange}
//                 onKeyDown={handleKeyDown}
//             />
//             <input
//                 type="password"
//                 value={password}
//                 onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
//                     setPassword(e.target.value)
//                 }
//             />
//             <button type="submit">Login</button>
//         </form>
//     );
// }

// ============================================================================
// 3. TYPING HOOKS
// ============================================================================

// --- useState ---
// const [count, setCount] = React.useState<number>(0);
// const [user, setUser] = React.useState<User | null>(null);
// const [items, setItems] = React.useState<string[]>([]);

// --- useRef ---
// const inputRef = React.useRef<HTMLInputElement>(null);
// const intervalRef = React.useRef<ReturnType<typeof setInterval> | null>(null);

// --- useReducer ---
// interface TodoState {
//     todos: Todo[];
//     filter: 'all' | 'active' | 'completed';
// }
//
// type TodoAction =
//     | { type: 'ADD_TODO'; payload: string }
//     | { type: 'TOGGLE_TODO'; payload: number }
//     | { type: 'DELETE_TODO'; payload: number };
//
// function todoReducer(state: TodoState, action: TodoAction): TodoState {
//     switch (action.type) {
//         case 'ADD_TODO':
//             return { ...state, todos: [...state.todos, { id: Date.now(), text: action.payload, completed: false }] };
//         case 'TOGGLE_TODO':
//             return { ...state, todos: state.todos.map(t => t.id === action.payload ? { ...t, completed: !t.completed } : t) };
//         case 'DELETE_TODO':
//             return { ...state, todos: state.todos.filter(t => t.id !== action.payload) };
//         default:
//             return state;
//     }
// }

// ============================================================================
// 4. GENERIC COMPONENTS
// ============================================================================

/*
   Generic components work with different data types while maintaining type safety.
*/

// interface ListProps<T> {
//     items: T[];
//     renderItem: (item: T, index: number) => React.ReactNode;
//     keyExtractor: (item: T) => string | number;
// }
//
// function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
//     return (
//         <ul>
//             {items.map((item, index) => (
//                 <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
//             ))}
//         </ul>
//     );
// }
//
// // Usage with type inference:
// // <List
// //     items={users}
// //     renderItem={(user) => <span>{user.name}</span>}
// //     keyExtractor={(user) => user.id}
// // />

// ============================================================================
// 5. TYPED CONTEXT
// ============================================================================

// interface AuthContextType {
//     user: User | null;
//     login: (email: string, password: string) => Promise<void>;
//     logout: () => void;
//     isLoading: boolean;
// }
//
// const AuthContext = React.createContext<AuthContextType | undefined>(undefined);
//
// function useAuth(): AuthContextType {
//     const context = React.useContext(AuthContext);
//     if (!context) {
//         throw new Error('useAuth must be used within AuthProvider');
//     }
//     return context;
// }

// ============================================================================
// 6. EXTENDING HTML ELEMENTS
// ============================================================================

/*
   Create components that accept all native HTML attributes plus custom props.
*/

// interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
//     variant?: 'primary' | 'secondary' | 'danger';
//     isLoading?: boolean;
// }
//
// function Button({ variant = 'primary', isLoading, children, ...props }: ButtonProps) {
//     return (
//         <button
//             className={`btn btn-${variant}`}
//             disabled={isLoading || props.disabled}
//             {...props}
//         >
//             {isLoading ? 'Loading...' : children}
//         </button>
//     );
// }

// --- With forwardRef ---
// const FancyInput = React.forwardRef<HTMLInputElement, { label: string }>(
//     ({ label, ...props }, ref) => (
//         <div>
//             <label>{label}</label>
//             <input ref={ref} {...props} />
//         </div>
//     )
// );

// ============================================================================
// 7. COMMON UTILITY TYPES
// ============================================================================

/*
   // Pick specific props
   type UserName = Pick<User, 'firstName' | 'lastName'>;
   
   // Omit specific props
   type UserWithoutPassword = Omit<User, 'password'>;
   
   // Make all props optional
   type PartialUser = Partial<User>;
   
   // Make all props required
   type RequiredUser = Required<PartialUser>;
   
   // Record type for dictionaries
   type UserMap = Record<string, User>;
   
   // Union of string literals
   type Status = 'active' | 'inactive' | 'pending';
*/

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
   1. Use interface for public component props (extends, declaration merging)
   2. Use type for unions, intersections, and utility types
   3. Prefer React.ReactNode over JSX.Element (more flexible)
   4. Type event handlers explicitly (React.ChangeEvent, React.MouseEvent)
   5. Use discriminated unions for reducer actions
   6. Use generic components for reusable data-display components
   7. Always provide a default value or undefined check for context
   8. Use satisfies operator for stricter type checking (TS 4.9+)
   9. Avoid using any - prefer unknown if type is truly unknown
   10. Use as const for literal types and readonly arrays
*/

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Define props with interface or type");
console.log("2. Type event handlers with React.Event types");
console.log("3. Type hooks explicitly (useState<T>, useRef<T>)");
console.log("4. Use generic components for reusable patterns");
console.log("5. Extend HTML element interfaces for custom components");
console.log("6. Use discriminated unions for reducer actions");
console.log("7. Prefer React.ReactNode for children prop");
console.log("=".repeat(80));

export default {};

