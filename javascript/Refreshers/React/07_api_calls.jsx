/**
 * REACT API CALLS
 * ================
 * Fetch, Axios, React Query, SWR, error handling, loading states
 */

import React, { useState, useEffect, useCallback } from 'react';

console.log("=".repeat(80));
console.log("REACT API CALLS");
console.log("=".repeat(80));

// ============================================================================
// 1. FETCH API (Built-in)
// ============================================================================

/*
   The Fetch API is built into modern browsers.
   It returns Promises and works with async/await.
*/

function FetchExample() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('https://api.example.com/users')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setData(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    return <div>{JSON.stringify(data)}</div>;
}

// --- POST request with fetch ---
async function createUser(userData) {
    const response = await fetch('https://api.example.com/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer token123'
        },
        body: JSON.stringify(userData)
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
}

// ============================================================================
// 2. AXIOS
// ============================================================================

/*
   Axios is a popular HTTP client with a cleaner API than fetch.
   Features: request/response interceptors, automatic JSON parsing, timeout.
   
   // install: npm install axios
   
   import axios from 'axios';
*/

// --- Basic usage ---
// function AxiosExample() {
//     const [users, setUsers] = useState([]);
//     const [loading, setLoading] = useState(true);
//
//     useEffect(() => {
//         axios.get('https://api.example.com/users')
//             .then(response => {
//                 setUsers(response.data);  // Axios auto-parses JSON
//                 setLoading(false);
//             })
//             .catch(error => {
//                 console.error('Error:', error.response?.data || error.message);
//                 setLoading(false);
//             });
//     }, []);
//
//     if (loading) return <div>Loading...</div>;
//     return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
// }

// --- Axios instance with base config ---
// const api = axios.create({
//     baseURL: 'https://api.example.com',
//     timeout: 5000,
//     headers: { 'Content-Type': 'application/json' }
// });

// --- Interceptors ---
// api.interceptors.request.use(config => {
//     const token = localStorage.getItem('token');
//     if (token) {
//         config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
// });
//
// api.interceptors.response.use(
//     response => response,
//     error => {
//         if (error.response?.status === 401) {
//             // Redirect to login
//         }
//         return Promise.reject(error);
//     }
// );

// ============================================================================
// 3. CUSTOM useFetch HOOK
// ============================================================================

/*
   Encapsulate fetch logic in a reusable custom hook.
   Handles loading, error, and data states consistently.
*/

function useFetch(url, options = {}) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let cancelled = false;

        const fetchData = async () => {
            setLoading(true);
            setError(null);

            try {
                const response = await fetch(url, options);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                const result = await response.json();
                if (!cancelled) {
                    setData(result);
                }
            } catch (err) {
                if (!cancelled) {
                    setError(err.message);
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        };

        fetchData();

        return () => {
            cancelled = true;
        };
    }, [url]);  // Re-fetch when URL changes

    return { data, loading, error };
}

// Usage:
// function UsersList() {
//     const { data: users, loading, error } = useFetch('/api/users');
//
//     if (loading) return <Spinner />;
//     if (error) return <ErrorMessage message={error} />;
//     return <UserTable users={users} />;
// }

// ============================================================================
// 4. REACT QUERY / TANSTACK QUERY
// ============================================================================

/*
   TanStack Query (formerly React Query) manages server state.
   Features: caching, background refetching, pagination, optimistic updates.
   
   // install: npm install @tanstack/react-query
   
   import { QueryClient, QueryClientProvider, useQuery, useMutation } from '@tanstack/react-query';
*/

// --- Setup ---
// const queryClient = new QueryClient({
//     defaultOptions: {
//         queries: {
//             staleTime: 5 * 60 * 1000,  // 5 minutes
//             retry: 2,
//             refetchOnWindowFocus: true
//         }
//     }
// });
//
// function App() {
//     return (
//         <QueryClientProvider client={queryClient}>
//             <UsersPage />
//         </QueryClientProvider>
//     );
// }

// --- useQuery (fetching) ---
// function UsersPage() {
//     const { data, isLoading, error, refetch } = useQuery({
//         queryKey: ['users'],
//         queryFn: () => fetch('/api/users').then(res => res.json()),
//         select: (data) => data.filter(user => user.isActive)  // transform data
//     });
//
//     if (isLoading) return <Spinner />;
//     if (error) return <Error error={error} />;
//     return <UserList users={data} onRefresh={refetch} />;
// }

// --- useMutation (writing) ---
// function AddUserForm() {
//     const queryClient = useQueryClient();
//
//     const mutation = useMutation({
//         mutationFn: (newUser) => fetch('/api/users', {
//             method: 'POST',
//             body: JSON.stringify(newUser)
//         }),
//         onSuccess: () => {
//             // Invalidate and refetch users list
//             queryClient.invalidateQueries({ queryKey: ['users'] });
//         }
//     });
//
//     return (
//         <button
//             onClick={() => mutation.mutate({ name: 'New User' })}
//             disabled={mutation.isPending}
//         >
//             {mutation.isPending ? 'Adding...' : 'Add User'}
//         </button>
//     );
// }

// ============================================================================
// 5. SWR (Stale-While-Revalidate)
// ============================================================================

/*
   SWR is a lightweight alternative to React Query by Vercel.
   
   // install: npm install swr
   
   import useSWR from 'swr';
*/

// const fetcher = (...args) => fetch(...args).then(res => res.json());
//
// function Profile() {
//     const { data, error, isLoading, mutate } = useSWR('/api/user', fetcher, {
//         refreshInterval: 30000,  // Poll every 30 seconds
//         revalidateOnFocus: true
//     });
//
//     if (isLoading) return <div>Loading...</div>;
//     if (error) return <div>Failed to load</div>;
//     return <div>Hello {data.name}</div>;
// }

// ============================================================================
// 6. REQUEST CANCELLATION (AbortController)
// ============================================================================

/*
   Cancel in-flight requests when component unmounts or dependencies change.
   Prevents memory leaks and race conditions.
*/

function SearchComponent() {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!query) {
            setResults([]);
            return;
        }

        const controller = new AbortController();

        const search = async () => {
            setLoading(true);
            try {
                const response = await fetch(`/api/search?q=${query}`, {
                    signal: controller.signal
                });
                const data = await response.json();
                setResults(data);
            } catch (err) {
                if (err.name !== 'AbortError') {
                    console.error('Search failed:', err);
                }
            } finally {
                setLoading(false);
            }
        };

        // Debounce: wait 300ms before searching
        const timeout = setTimeout(search, 300);

        return () => {
            clearTimeout(timeout);
            controller.abort();  // Cancel in-flight request
        };
    }, [query]);

    return (
        <div>
            <input value={query} onChange={(e) => setQuery(e.target.value)} />
            {loading && <div>Searching...</div>}
            <ul>{results.map(r => <li key={r.id}>{r.name}</li>)}</ul>
        </div>
    );
}

// ============================================================================
// 7. OPTIMISTIC UPDATES
// ============================================================================

/*
   Update the UI immediately before the server confirms.
   Roll back if the server request fails.
*/

// function ToggleTodo({ todo }) {
//     const queryClient = useQueryClient();
//
//     const mutation = useMutation({
//         mutationFn: () => fetch(`/api/todos/${todo.id}`, {
//             method: 'PATCH',
//             body: JSON.stringify({ completed: !todo.completed })
//         }),
//         // Optimistic update
//         onMutate: async () => {
//             await queryClient.cancelQueries({ queryKey: ['todos'] });
//             const previousTodos = queryClient.getQueryData(['todos']);
//
//             queryClient.setQueryData(['todos'], (old) =>
//                 old.map(t =>
//                     t.id === todo.id ? { ...t, completed: !t.completed } : t
//                 )
//             );
//
//             return { previousTodos };
//         },
//         // Rollback on error
//         onError: (err, newTodo, context) => {
//             queryClient.setQueryData(['todos'], context.previousTodos);
//         },
//         onSettled: () => {
//             queryClient.invalidateQueries({ queryKey: ['todos'] });
//         }
//     });
//
//     return (
//         <input
//             type="checkbox"
//             checked={todo.completed}
//             onChange={() => mutation.mutate()}
//         />
//     );
// }

// ============================================================================
// 8. BEST PRACTICES
// ============================================================================

/*
   1. Use React Query or SWR for server state (caching, refetching)
   2. Always handle loading, error, and empty states
   3. Cancel requests on unmount to prevent memory leaks
   4. Use AbortController for search/autocomplete
   5. Implement retry logic for transient failures
   6. Use optimistic updates for better UX
   7. Centralize API configuration (base URL, auth headers)
   8. Use TypeScript for typed API responses
   9. Separate API layer from UI components
   10. Handle token refresh and 401 redirects globally
*/

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. Fetch is built-in, Axios has better DX (interceptors)");
console.log("2. Custom useFetch hook for reusable fetch logic");
console.log("3. React Query: caching, background refetch, mutations");
console.log("4. SWR: lightweight alternative by Vercel");
console.log("5. AbortController for request cancellation");
console.log("6. Optimistic updates for instant UI feedback");
console.log("7. Always handle loading, error, and empty states");
console.log("=".repeat(80));

export default FetchExample;

