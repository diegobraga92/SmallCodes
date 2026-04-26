/**
 * REACT ROUTER
 * =============
 * React Router DOM v6: routing, navigation, parameters, nested routes, guards
 */

import React from 'react';

console.log("=".repeat(80));
console.log("REACT ROUTER");
console.log("=".repeat(80));

// ============================================================================
// 1. BASIC SETUP
// ============================================================================

/*
   React Router v6 is the standard routing library for React apps.
   
   // install: npm install react-router-dom
   
   import {
       BrowserRouter,
       Routes,
       Route,
       Link,
       NavLink,
       useParams,
       useNavigate,
       useSearchParams,
       Outlet
   } from 'react-router-dom';
*/

// --- App structure ---
// function App() {
//     return (
//         <BrowserRouter>
//             <nav>
//                 <Link to="/">Home</Link>
//                 <Link to="/about">About</Link>
//                 <Link to="/users">Users</Link>
//             </nav>
//
//             <Routes>
//                 <Route path="/" element={<Home />} />
//                 <Route path="/about" element={<About />} />
//                 <Route path="/users" element={<Users />} />
//                 <Route path="*" element={<NotFound />} />
//             </Routes>
//         </BrowserRouter>
//     );
// }

// ============================================================================
// 2. LINK vs NAVLINK
// ============================================================================

/*
   Link:       Basic navigation, no styling
   NavLink:    Navigation with active state (className, style, children callback)
*/

// function Navigation() {
//     return (
//         <nav>
//             {/* Basic link */}
//             <Link to="/">Home</Link>
//
//             {/* NavLink with active class */}
//             <NavLink
//                 to="/about"
//                 className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
//             >
//                 About
//             </NavLink>
//
//             {/* NavLink with active style */}
//             <NavLink
//                 to="/contact"
//                 style={({ isActive }) => ({
//                     fontWeight: isActive ? 'bold' : 'normal',
//                     color: isActive ? 'blue' : 'gray'
//                 })}
//             >
//                 Contact
//             </NavLink>
//
//             {/* NavLink with children callback */}
//             <NavLink to="/dashboard">
//                 {({ isActive }) => (
//                     <span className={isActive ? 'active' : ''}>
//                         {isActive ? '>' : ''} Dashboard
//                     </span>
//                 )}
//             </NavLink>
//         </nav>
//     );
// }

// ============================================================================
// 3. ROUTE PARAMETERS (useParams)
// ============================================================================

/*
   Dynamic segments in paths using :paramName syntax.
   Access values with useParams() hook.
*/

// Route: <Route path="/users/:userId" element={<UserProfile />} />

// function UserProfile() {
//     const { userId } = useParams();
//     const [user, setUser] = useState(null);
//
//     useEffect(() => {
//         fetch(`/api/users/${userId}`)
//             .then(res => res.json())
//             .then(setUser);
//     }, [userId]);
//
//     if (!user) return <div>Loading...</div>;
//
//     return (
//         <div>
//             <h2>{user.name}</h2>
//             <p>Email: {user.email}</p>
//             <Link to={`/users/${userId}/edit`}>Edit</Link>
//         </div>
//     );
// }

// Multiple params: /products/:categoryId/:productId
// function ProductDetail() {
//     const { categoryId, productId } = useParams();
//     return <div>Category: {categoryId}, Product: {productId}</div>;
// }

// ============================================================================
// 4. QUERY PARAMETERS (useSearchParams)
// ============================================================================

/*
   Read and update URL query string (?key=value&key2=value2).
   Similar to useState but synced with URL.
*/

// function SearchPage() {
//     const [searchParams, setSearchParams] = useSearchParams();
//
//     const query = searchParams.get('q') || '';
//     const page = Number(searchParams.get('page')) || 1;
//     const sort = searchParams.get('sort') || 'name';
//
//     const handleSearch = (value) => {
//         setSearchParams({ q: value, page: '1', sort });
//     };
//
//     const nextPage = () => {
//         setSearchParams({ q: query, page: String(page + 1), sort });
//     };
//
//     return (
//         <div>
//             <input
//                 value={query}
//                 onChange={(e) => handleSearch(e.target.value)}
//                 placeholder="Search..."
//             />
//             <p>Page: {page}</p>
//             <button onClick={nextPage}>Next Page</button>
//         </div>
//     );
// }

// ============================================================================
// 5. NESTED ROUTES AND OUTLET
// ============================================================================

/*
   Nested routes share a parent layout via the <Outlet /> component.
   The parent renders the Outlet, and child routes render inside it.
*/

// --- Layout component ---
// function DashboardLayout() {
//     return (
//         <div className="dashboard">
//             <aside>
//                 <nav>
//                     <NavLink to="profile">Profile</NavLink>
//                     <NavLink to="settings">Settings</NavLink>
//                     <NavLink to="analytics">Analytics</NavLink>
//                 </nav>
//             </aside>
//             <main>
//                 <Outlet /> {/* Child routes render here */}
//             </main>
//         </div>
//     );
// }

// --- Route configuration ---
// <Route path="dashboard" element={<DashboardLayout />}>
//     <Route index element={<DashboardHome />} />          {/* /dashboard */}
//     <Route path="profile" element={<Profile />} />       {/* /dashboard/profile */}
//     <Route path="settings" element={<Settings />} />     {/* /dashboard/settings */}
//     <Route path="analytics" element={<Analytics />} />   {/* /dashboard/analytics */}
// </Route>

// ============================================================================
// 6. PROGRAMMATIC NAVIGATION (useNavigate)
// ============================================================================

/*
   useNavigate returns a function to navigate programmatically.
   Useful after form submissions, timeouts, or conditional redirects.
*/

// function LoginForm() {
//     const navigate = useNavigate();
//     const [error, setError] = useState(null);
//
//     const handleSubmit = async (e) => {
//         e.preventDefault();
//         try {
//             await loginUser(formData);
//             navigate('/dashboard', { replace: true }); // replace: don't add to history
//         } catch (err) {
//             setError(err.message);
//         }
//     };
//
//     return <form onSubmit={handleSubmit}>...</form>;
// }

// Navigation options:
// navigate('/path')                    // Push to history
// navigate('/path', { replace: true }) // Replace current entry
// navigate(-1)                         // Go back
// navigate(1)                          // Go forward
// navigate('../parent')                // Relative navigation

// ============================================================================
// 7. PROTECTED ROUTES (Auth Guard)
// ============================================================================

/*
   Create a wrapper component that checks auth status
   and redirects unauthenticated users.
*/

// function RequireAuth({ children }) {
//     const { user } = useAuth();
//     const location = useLocation();
//
//     if (!user) {
//         // Redirect to login, but save the location they tried to access
//         return <Navigate to="/login" state={{ from: location }} replace />;
//     }
//
//     return children;
// }

// Usage:
// <Route
//     path="/dashboard"
//     element={
//         <RequireAuth>
//             <Dashboard />
//         </RequireAuth>
//     }
// />

// After login, redirect back:
// function LoginPage() {
//     const navigate = useNavigate();
//     const location = useLocation();
//     const from = location.state?.from?.pathname || '/';
//
//     const handleLogin = () => {
//         login();
//         navigate(from, { replace: true });
//     };
//
//     return <button onClick={handleLogin}>Log in</button>;
// }

// ============================================================================
// 8. LAZY LOADING ROUTES
// ============================================================================

/*
   Code-split routes with React.lazy and Suspense.
   Reduces initial bundle size.
*/

// import { lazy, Suspense } from 'react';
//
// const Dashboard = lazy(() => import('./pages/Dashboard'));
// const Settings = lazy(() => import('./pages/Settings'));
// const Analytics = lazy(() => import('./pages/Analytics'));
//
// function App() {
//     return (
//         <BrowserRouter>
//             <Suspense fallback={<div>Loading page...</div>}>
//                 <Routes>
//                     <Route path="/dashboard" element={<Dashboard />} />
//                     <Route path="/settings" element={<Settings />} />
//                     <Route path="/analytics" element={<Analytics />} />
//                 </Routes>
//             </Suspense>
//         </BrowserRouter>
//     );
// }

// ============================================================================
// 9. 404 NOT FOUND
// ============================================================================

// <Route path="*" element={<NotFound />} />

// function NotFound() {
//     return (
//         <div>
//             <h1>404 - Page Not Found</h1>
//             <Link to="/">Go Home</Link>
//         </div>
//     );
// }

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/*
   1. Use BrowserRouter for web apps (HashRouter for static hosting)
   2. Keep routes organized in a central config or use layout routes
   3. Use NavLink for navigation menus (built-in active state)
   4. Prefer <Link> over window.location (no page reload)
   5. Use relative paths in nested routes
   6. Always handle the "no match" case (404)
   7. Lazy load routes that aren't needed immediately
   8. Use replace: true for redirects after form submission
   9. Store redirect location in state for auth flows
   10. Keep URL as the source of truth for page state
*/

console.log("\n" + "=".repeat(80));
console.log("KEY TAKEAWAYS:");
console.log("1. BrowserRouter wraps the app, Routes/Route define paths");
console.log("2. Link for navigation, NavLink for active styling");
console.log("3. useParams for dynamic segments (:id)");
console.log("4. useSearchParams for query strings (?q=search)");
console.log("5. Outlet for nested layouts");
console.log("6. useNavigate for programmatic navigation");
console.log("7. Protected routes with RequireAuth wrapper");
console.log("8. React.lazy + Suspense for code splitting");
console.log("=".repeat(80));

export default {};

