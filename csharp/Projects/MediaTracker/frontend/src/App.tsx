import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import MediaForm from './pages/MediaForm';
import MediaDetail from './pages/MediaDetail';

/*
 * PrivateRoute is a wrapper component that checks authentication.
 * If the user has a token in localStorage, render the children.
 * Otherwise, redirect to /login.
 *
 * This is a "Higher-Order Component" pattern — a component that wraps
 * another component to add behavior. In this case, it adds auth checking.
 *
 * Alternative: We could use a route guard library like react-router's
 * loader functions, but this simple approach is clear and educational.
 */
function PrivateRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('token');
  return token ? <>{children}</> : <Navigate to="/login" replace />;
}

/*
 * App component defines the routing structure.
 * React Router v6 uses a declarative route configuration:
 * - BrowserRouter: HTML5 history API for clean URLs
 * - Routes: container for all Route definitions
 * - Route: maps a URL path to a component
 *
 * Route order matters — more specific routes should come before
 * less specific ones. React Router v6 is "best match" based, so
 * order is less critical than v5, but it's still good practice.
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes — no authentication required */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected routes — wrapped in PrivateRoute */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/media/new"
          element={
            <PrivateRoute>
              <MediaForm />
            </PrivateRoute>
          }
        />
        <Route
          path="/media/:id"
          element={
            <PrivateRoute>
              <MediaDetail />
            </PrivateRoute>
          }
        />
        <Route
          path="/media/:id/edit"
          element={
            <PrivateRoute>
              <MediaForm />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
