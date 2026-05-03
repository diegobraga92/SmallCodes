import api from './api';
import type { AuthResponse, LoginRequest, RegisterRequest } from '../types/media';

/*
 * Auth service — encapsulates all authentication-related API calls.
 *
 * This is a "service object" pattern (not a class). It's a plain object
 * with methods, which is simpler than a class for stateless services.
 *
 * Each method:
 * 1. Calls the API via our Axios instance (which auto-attaches JWT)
 * 2. Returns the typed response data
 * 3. Lets the caller handle errors (caught in hooks/components)
 */
export const authService = {
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/login', data);
    return response.data;
  },

  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/auth/register', data);
    return response.data;
  },

  /*
   * Logout is client-side only — we just clear localStorage.
   * There's no server-side session to invalidate because JWT is stateless.
   * The token remains valid until it expires, but without it in localStorage,
   * the user can't make authenticated requests.
   *
   * Tradeoff: If someone steals the token before it expires, they can still
   * use it. This is why production apps use short-lived tokens + refresh tokens.
   */
  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  },
};
