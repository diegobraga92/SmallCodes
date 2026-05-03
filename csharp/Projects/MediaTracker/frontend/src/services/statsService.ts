import api from './api';

/*
 * Stats interface — matches StatsDto from the backend.
 * Defined here rather than in types/media.ts because it's specific
 * to this service. In a larger project, you'd have a dedicated types
 * directory structure.
 */
export interface Stats {
  totalItems: number;
  totalBooks: number;
  totalGames: number;
  totalMovies: number;
  notStarted: number;
  inProgress: number;
  completed: number;
  onHold: number;
  dropped: number;
  averageRating: number | null;
}

export const statsService = {
  /*
   * GET /api/stats
   * Returns aggregate statistics for the authenticated user.
   * The userId is extracted from the JWT on the backend.
   */
  async get(): Promise<Stats> {
    const response = await api.get<Stats>('/stats');
    return response.data;
  },
};
