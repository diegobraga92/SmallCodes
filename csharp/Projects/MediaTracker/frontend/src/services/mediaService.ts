import api from './api';
import type { MediaItem, CreateMediaItem, UpdateMediaItem, MediaType } from '../types/media';

/*
 * Media service — CRUD operations for media items.
 * Each method corresponds to a backend endpoint in MediaController.
 *
 * The GetAllParams interface defines the query string parameters
 * for filtering, searching, and sorting.
 */
export interface GetAllParams {
  type?: MediaType;
  search?: string;
  sortBy?: string;
  sortOrder?: string;
}

export const mediaService = {
  /*
   * GET /api/media?type=...&search=...&sortBy=...&sortOrder=...
   * Axios automatically serializes the params object into query string parameters.
   */
  async getAll(params?: GetAllParams): Promise<MediaItem[]> {
    const response = await api.get<MediaItem[]>('/media', { params });
    return response.data;
  },

  async getById(id: string): Promise<MediaItem> {
    const response = await api.get<MediaItem>(`/media/${id}`);
    return response.data;
  },

  async create(data: CreateMediaItem): Promise<MediaItem> {
    const response = await api.post<MediaItem>('/media', data);
    return response.data;
  },

  async update(id: string, data: UpdateMediaItem): Promise<MediaItem> {
    const response = await api.put<MediaItem>(`/media/${id}`, data);
    return response.data;
  },

  /*
   * DELETE returns 204 No Content, so there's no response body to parse.
   * We return void (undefined) to indicate success.
   */
  async delete(id: string): Promise<void> {
    await api.delete(`/media/${id}`);
  },
};
