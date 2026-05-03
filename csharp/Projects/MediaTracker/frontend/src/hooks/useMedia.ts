import { useState, useEffect, useCallback } from 'react';
import { mediaService } from '../services/mediaService';
import type { MediaItem, CreateMediaItem, UpdateMediaItem, MediaType } from '../types/media';
import type { GetAllParams } from '../services/mediaService';

/*
 * useMedia is a custom hook for managing media items.
 * It handles:
 * - Fetching items with optional filters (type, search, sort)
 * - Creating, updating, and deleting items
 * - Loading and error states
 *
 * The hook takes filter parameters and automatically re-fetches when they change
 * (via the useEffect dependency on fetchItems, which depends on the filter params).
 */
export function useMedia(type?: MediaType, search?: string, sortBy?: string, sortOrder?: string) {
  const [items, setItems] = useState<MediaItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /*
   * fetchItems is memoized with useCallback because it's used in useEffect.
   * Without useCallback, it would be a new function on every render, causing
   * the effect to run on every render (infinite loop).
   *
   * The dependencies are the filter parameters — when any of them change,
   * a new fetchItems is created, triggering the useEffect to re-fetch.
   */
  const fetchItems = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params: GetAllParams = {};
      if (type) params.type = type;
      if (search) params.search = search;
      if (sortBy) params.sortBy = sortBy;
      if (sortOrder) params.sortOrder = sortOrder;
      const data = await mediaService.getAll(params);
      setItems(data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch media items');
    } finally {
      setLoading(false);
    }
  }, [type, search, sortBy, sortOrder]);

  /*
   * useEffect runs fetchItems when the component mounts and when
   * fetchItems changes (which happens when filter params change).
   *
   * This is the React way of handling side effects (data fetching).
   * In a class component, this would be componentDidMount + componentDidUpdate.
   */
  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  /*
   * Optimistic updates: create/update/remove modify the local state immediately
   * after the API call succeeds. This keeps the UI in sync without re-fetching
   * the entire list.
   *
   * Tradeoff: If another user modifies the same data, we won't see it until
   * the next fetch. For a single-user app like this, it's fine.
   */
  const create = useCallback(async (data: CreateMediaItem) => {
    const item = await mediaService.create(data);
    setItems((prev) => [item, ...prev]);  // Add new item to the beginning
    return item;
  }, []);

  const update = useCallback(async (id: string, data: UpdateMediaItem) => {
    const updated = await mediaService.update(id, data);
    setItems((prev) => prev.map((item) => (item.id === id ? updated : item)));
    return updated;
  }, []);

  const remove = useCallback(async (id: string) => {
    await mediaService.delete(id);
    setItems((prev) => prev.filter((item) => item.id !== id));
  }, []);

  return { items, loading, error, fetchItems, create, update, remove };
}
