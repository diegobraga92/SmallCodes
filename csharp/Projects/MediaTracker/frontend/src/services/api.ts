import axios from 'axios';

/*
 * Axios is an HTTP client library. We use it instead of the built-in fetch() API
 * because it provides:
 * 1. Automatic JSON parsing/stringifying
 * 2. Request/response interceptors (for JWT token injection)
 * 3. Better error handling (throws on non-2xx status codes)
 * 4. Request cancellation support
 *
 * Tradeoff: Axios adds ~14KB to the bundle. For a small app, fetch() would work
 * fine, but Axios's interceptor pattern is very convenient for JWT auth.
 */

/*
 * Create an Axios instance with default configuration.
 * baseURL: '/api' — all requests go to /api/*, which Nginx proxies to the backend.
 * In development (Vite dev server), this is proxied via vite.config.ts.
 * In production (Docker), Nginx handles the proxy (see nginx.conf).
 */
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

/*
 * REQUEST INTERCEPTOR — runs before every request.
 * This is where we attach the JWT token to the Authorization header.
 *
 * The token is stored in localStorage (see authService.ts).
 * localStorage persists across browser sessions (unlike sessionStorage).
 *
 * Security note: Storing JWTs in localStorage is common but has risks:
 * - XSS (Cross-Site Scripting) attacks can read localStorage
 * - HttpOnly cookies are more secure but require more complex setup
 * For an educational project, localStorage is acceptable.
 */
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/*
 * RESPONSE INTERCEPTOR — runs after every response.
 * This handles 401 Unauthorized responses globally.
 *
 * When the server returns 401, it means the token is invalid or expired.
 * We clear the stored auth data and redirect to the login page.
 *
 * We skip this for auth endpoints (/auth/*) to avoid redirect loops
 * (e.g., if login itself returns 401 due to invalid credentials).
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const url = error.config?.url || '';
      // Don't redirect on auth endpoints (login/register)
      if (!url.includes('/auth/')) {
        localStorage.removeItem('token');
        localStorage.removeItem('userId');
        localStorage.removeItem('username');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
