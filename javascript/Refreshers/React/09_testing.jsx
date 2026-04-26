/**
 * REACT TESTING
 * ==============
 * Jest, React Testing Library, component tests, hooks, mocking
 */

import React from 'react';

console.log("=".repeat(80));
console.log("REACT TESTING");
console.log("=".repeat(80));

// ============================================================================
// 1. SETUP
// ============================================================================

/*
   Testing stack:
   - Jest: test runner and assertions
   - React Testing Library (RTL): render components, query DOM
   - user-event: simulate user interactions
   
   // install: npm install --save-dev jest @testing-library/react @testing-library/jest-dom @testing-library/user-event
   
   // setupTests.js (runs before each test)
   // import '@testing-library/jest-dom';
*/

// ============================================================================
// 2. RENDERING AND QUERYING
// ============================================================================

/*
   RTL queries by priority:
   1. getByRole (most accessible)
   2. getByLabelText (form inputs)
   3. getByPlaceholderText
   4. getByText (non-interactive elements)
   5. getByDisplayValue (form values)
   6. getByAltText (images)
   7. getByTitle
   8. getByTestId (last resort)
*/

// --- Component to test ---
function Greeting({ name, onLogout }) {
    return (
        <div>
            <h1>Hello, {name}!</h1>
            <button onClick={onLogout}>Logout</button>
        </div>
    );
}

// --- Test ---
// import { render, screen } from '@testing-library/react';
// import userEvent from '@testing-library/user-event';
//
// test('renders greeting with name', () => {
//     render(<Greeting name="Alice" onLogout={() => {}} />);
//
//     expect(screen.getByRole('heading')).toHaveTextContent('Hello, Alice!');
//     expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument();
// });
//
// test('calls onLogout when button clicked', async () => {
//     const handleLogout = jest.fn();
//     const user = userEvent.setup();
//
//     render(<Greeting name="Bob" onLogout={handleLogout} />);
//
//     await user.click(screen.getByRole('button', { name: /logout/i }));
//     expect(handleLogout).toHaveBeenCalledTimes(1);
// });

// ============================================================================
// 3. TESTING FORMS
// ============================================================================

// --- Component ---
function LoginForm({ onSubmit }) {
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ email, password });
    };

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="email">Email</label>
            <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <label htmlFor="password">Password</label>
            <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <button type="submit">Login</button>
        </form>
    );
}

// --- Test ---
// test('submits form with email and password', async () => {
//     const handleSubmit = jest.fn();
//     const user = userEvent.setup();
//
//     render(<LoginForm onSubmit={handleSubmit} />);
//
//     await user.type(screen.getByLabelText(/email/i), 'alice@example.com');
//     await user.type(screen.getByLabelText(/password/i), 'mypassword');
//     await user.click(screen.getByRole('button', { name: /login/i }));
//
//     expect(handleSubmit).toHaveBeenCalledWith({
//         email: 'alice@example.com',
//         password: 'mypassword'
//     });
// });

// ============================================================================
// 4. TESTING ASYNC OPERATIONS
// ============================================================================

// --- Component ---
function UserProfile({ userId }) {
    const [user, setUser] = React.useState(null);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        fetch(`/api/users/${userId}`)
            .then(res => res.json())
            .then(data => {
                setUser(data);
                setLoading(false);
            });
    }, [userId]);

    if (loading) return <div>Loading...</div>;
    return <h1>{user.name}</h1>;
}

// --- Test with async ---
// import { waitFor } from '@testing-library/react';
//
// test('loads and displays user', async () => {
//     // Mock fetch
//     global.fetch = jest.fn(() =>
//         Promise.resolve({
//             ok: true,
//             json: () => Promise.resolve({ id: 1, name: 'Alice' })
//         })
//     );
//
//     render(<UserProfile userId={1} />);
//
//     // Initially shows loading
//     expect(screen.getByText('Loading...')).toBeInTheDocument();
//
//     // Wait for data to load
//     await waitFor(() => {
//         expect(screen.getByText('Alice')).toBeInTheDocument();
//     });
//
//     // Cleanup
//     global.fetch.mockRestore();
// });

// ============================================================================
// 5. TESTING CUSTOM HOOKS
// ============================================================================

/*
   Use renderHook from @testing-library/react to test hooks in isolation.
   
   // import { renderHook, act } from '@testing-library/react';
*/

// --- Hook ---
function useCounter(initialValue = 0) {
    const [count, setCount] = React.useState(initialValue);
    const increment = () => setCount(c => c + 1);
    const decrement = () => setCount(c => c - 1);
    const reset = () => setCount(initialValue);
    return { count, increment, decrement, reset };
}

// --- Test ---
// test('useCounter increments and decrements', () => {
//     const { result } = renderHook(() => useCounter(5));
//
//     expect(result.current.count).toBe(5);
//
//     act(() => result.current.increment());
//     expect(result.current.count).toBe(6);
//
//     act(() => result.current.decrement());
//     expect(result.current.count).toBe(5);
//
//     act(() => result.current.reset());
//     expect(result.current.count).toBe(5);
// });

// ============================================================================
// 6. MOCKING API CALLS (MSW)
// ============================================================================

/*
   MSW (Mock Service Worker) intercepts network requests at the service worker level.
   More realistic than mocking fetch directly.
   
   // install: npm install --save-dev msw
*/

// --- Setup ---
// import { http, HttpResponse } from 'msw';
// import { setupServer } from 'msw/node';
//
// const server = setupServer(
//     http.get('/api/users', () => {
//         return HttpResponse.json([
//             { id: 1, name: 'Alice' },
//             { id: 2, name: 'Bob' }
//         ]);
//     }),
//     http.post('/api/users', async ({ request }) => {
//         const body = await request.json();
//         return HttpResponse.json({ id: 3, ...body }, { status: 201 });
//     })
// );
//
// beforeAll(() => server.listen());
// afterEach(() => server.resetHandlers());
// afterAll(() => server.close());

// ============================================================================
// 7. SNAPSHOT TESTING
// ============================================================================

/*
   Snapshot tests capture the rendered output and compare on subsequent runs.
   Useful for detecting unintended changes.
*/

// test('matches snapshot', () => {
//     const { container } = render(<Greeting name="Alice" onLogout={() => {}} />);
//     expect(container).toMatchSnapshot();
// });

// ============================================================================
// 8. TESTING ERROR STATES
// ============================================================================

// --- Component ---
function ErrorBoundaryFallback({ error }) {
    return <div role="alert">Error: {error.message}</div>;
}

// --- Test ---
// test('displays error message', () => {
//     render(<ErrorBoundaryFallback error={new Error('Something went wrong')} />);
//     expect(screen.getByRole('alert')).toHaveTextContent('Something went wrong');
// });

// ============================================================================
// 9. BEST PRACTICES
// ============================================================================

/*
   1. Test behavior, not implementation (don't test internal state)
   2. Use accessible queries (getByRole, getByLabelText) over test IDs
   3. Use user-event over fireEvent (more realistic)
   4. Mock at the network level (MSW) not at the module level
   5. Test loading, success, error, and empty states
   6. Keep tests simple and focused (one assertion per test)
   7. Use describe blocks to organize related tests
   8. Avoid testing implementation details (don't test setState calls)
   9. Run tests in CI and block merges on failures
   10. Use code coverage as a guide, not a target
*/

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. React Testing Library: test how users interact");
console.log("2. Query by accessibility (getByRole, getByLabelText)");
console.log("3. user-event for realistic interactions");
console.log("4. MSW for network-level mocking");
console.log("5. renderHook for testing custom hooks");
console.log("6. Test loading, success, error, and empty states");
console.log("7. Test behavior, not implementation details");
console.log("=".repeat(80));

export default {};

