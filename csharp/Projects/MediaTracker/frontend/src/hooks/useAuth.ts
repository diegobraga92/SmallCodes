import { useState, useCallback } from 'react';
import { authService } from '../services/authService';
import type { LoginRequest, RegisterRequest } from '../types/media';

/*
 * useAuth is a custom React hook that encapsulates authentication logic.
 *
 * React hooks are functions that let you use state and other React features
 * without writing a class. Custom hooks let you extract component logic into
 * reusable functions.
 *
 * This hook manages:
 * - loading state (for showing spinners/disabled buttons)
 * - error state (for showing error messages)
 * - login/register/logout functions
 *
 * The hook returns an object with these values, which components destructure.
 * This is the "hooks" pattern — stateful logic is reusable across components.
 */
export function useAuth() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /*
   * useCallback memoizes the function — it's only recreated when dependencies change.
   * This prevents unnecessary re-renders when the function is passed as a prop
   * or used in a useEffect dependency array.
   *
   * Without useCallback, a new function would be created on every render,
   * potentially causing infinite re-render loops in useEffect.
   */
  const login = useCallback(async (data: LoginRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authService.login(data);
      /*
       * Store auth data in localStorage. This is how the app persists
       * authentication across page refreshes. The token is read by the
       * Axios interceptor (api.ts) and attached to every request.
       */
      localStorage.setItem('token', response.token);
      localStorage.setItem('userId', response.userId);
      localStorage.setItem('username', response.username);
      return true;
    } catch (err: any) {
      /*
       * Axios wraps error responses in an error object with response.data.
       * We extract the message sent by the backend (see AuthController).
       */
      setError(err.response?.data?.message || 'Login failed');
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (data: RegisterRequest) => {
    setLoading(true);
    setError(null);
    try {
      const response = await authService.register(data);
      localStorage.setItem('token', response.token);
      localStorage.setItem('userId', response.userId);
      localStorage.setItem('username', response.username);
      return true;
    } catch (err: any) {
      setError(err.response?.data?.message || 'Registration failed');
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    authService.logout();
  }, []);

  return { login, register, logout, loading, error };
}
