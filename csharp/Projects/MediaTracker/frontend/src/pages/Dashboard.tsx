import { useState, useEffect, useRef, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { useMedia } from '../hooks/useMedia';
import { statsService } from '../services/statsService';
import type { Stats } from '../services/statsService';
import { MediaType, MediaStatus } from '../types/media';

/*
 * Dashboard is the main page of the app. It displays:
 * 1. Stats cards (total items, by type, completed, avg rating)
 * 2. Search bar with debounced input
 * 3. Sort controls
 * 4. Filter tabs (All, Books, Games, Movies)
 * 5. Media item grid with cards
 *
 * This is a "page component" — it composes hooks and child components
 * to build a complete page.
 */

// Color mapping for status badges
const statusColors: Record<MediaStatus, string> = {
  [MediaStatus.NotStarted]: 'bg-gray-100 text-gray-800',
  [MediaStatus.InProgress]: 'bg-blue-100 text-blue-800',
  [MediaStatus.Completed]: 'bg-green-100 text-green-800',
  [MediaStatus.OnHold]: 'bg-yellow-100 text-yellow-800',
  [MediaStatus.Dropped]: 'bg-red-100 text-red-800',
};

// Human-readable labels for media types
const typeLabels: Record<MediaType, string> = {
  [MediaType.Book]: 'Books',
  [MediaType.Game]: 'Games',
  [MediaType.Movie]: 'Movies',
};

/*
 * useDebounce is a custom hook that delays updating a value.
 * It's used here to prevent the search from firing on every keystroke.
 * Instead, it waits 300ms after the user stops typing before sending
 * the API request.
 *
 * How it works:
 * 1. User types "ha" — debounced value is still ""
 * 2. User types "harry" — debounced value is still ""
 * 3. User stops typing for 300ms — debounced value becomes "harry"
 * 4. The API call fires with "harry"
 *
 * This prevents unnecessary API calls and improves performance.
 */
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);  // Cleanup on unmount or value change
  }, [value, delay]);

  return debouncedValue;
}

export default function Dashboard() {
  const [activeType, setActiveType] = useState<MediaType | undefined>(undefined);
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState('updatedAt');
  const [sortOrder, setSortOrder] = useState('desc');
  const [stats, setStats] = useState<Stats | null>(null);
  const statsFetched = useRef(false);  // Prevents double-fetch in StrictMode

  const debouncedSearch = useDebounce(search, 300);

  /*
   * useMedia hook — fetches items whenever filters change.
   * The debounced search value is passed, so the API call only
   * fires after the user stops typing.
   */
  const { items, loading, remove } = useMedia(activeType, debouncedSearch, sortBy, sortOrder);

  const username = localStorage.getItem('username') || 'User';

  /*
   * Fetch stats only once on mount.
   * useRef(false) creates a mutable ref that persists across renders.
   * We set it to true after the first fetch to prevent double-fetching
   * in React StrictMode (which runs effects twice in development).
   *
   * Alternative: We could use a useEffect with empty deps, but StrictMode
   * would fire it twice. The useRef pattern is a workaround.
   */
  useEffect(() => {
    if (!statsFetched.current) {
      statsFetched.current = true;
      statsService.get().then(setStats).catch(() => {});
    }
  }, []);

  const handleDelete = useCallback(async (id: string) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      await remove(id);
    }
  }, [remove]);

  const handleLogout = useCallback(() => {
    localStorage.clear();
    window.location.href = '/login';
  }, []);

  const toggleSortOrder = useCallback(() => {
    setSortOrder((prev) => (prev === 'asc' ? 'desc' : 'asc'));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">MediaTracker</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">Welcome, {username}</span>
            <Link
              to="/media/new"
              className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
            >
              + Add Media
            </Link>
            <button
              onClick={handleLogout}
              className="text-gray-500 hover:text-gray-700 text-sm"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats cards */}
        {stats && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
            <StatCard label="Total Items" value={stats.totalItems} color="indigo" />
            <StatCard label="Books" value={stats.totalBooks} color="blue" />
            <StatCard label="Games" value={stats.totalGames} color="green" />
            <StatCard label="Movies" value={stats.totalMovies} color="purple" />
            <StatCard label="Completed" value={stats.completed} color="yellow" />
            <StatCard
              label="Avg Rating"
              value={stats.averageRating ? stats.averageRating.toFixed(1) : '—'}
              color="orange"
            />
          </div>
        )}

        {/* Search & Sort bar */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search by title, description, or genre..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>
          <div className="flex gap-2">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            >
              <option value="updatedAt">Last Updated</option>
              <option value="createdAt">Date Added</option>
              <option value="title">Title</option>
              <option value="rating">Rating</option>
              <option value="status">Status</option>
            </select>
            <button
              onClick={toggleSortOrder}
              className="px-3 py-2 border border-gray-300 rounded-md bg-white text-sm hover:bg-gray-50"
              title={sortOrder === 'asc' ? 'Ascending' : 'Descending'}
            >
              {sortOrder === 'asc' ? '↑ Asc' : '↓ Desc'}
            </button>
          </div>
        </div>

        {/* Filter tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto">
          <button
            onClick={() => setActiveType(undefined)}
            className={`px-4 py-2 rounded-md text-sm font-medium whitespace-nowrap ${
              !activeType
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            All
          </button>
          {Object.values(MediaType).map((type) => (
            <button
              key={type}
              onClick={() => setActiveType(type)}
              className={`px-4 py-2 rounded-md text-sm font-medium whitespace-nowrap ${
                activeType === type
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {typeLabels[type]}
            </button>
          ))}
        </div>

        {/* Loading state */}
        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
            <p className="mt-2 text-gray-500">Loading...</p>
          </div>
        )}

        {/* Empty state */}
        {!loading && items.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              {search ? 'No items match your search.' : 'No media items yet.'}
            </p>
            {!search && (
              <Link
                to="/media/new"
                className="mt-2 inline-block text-indigo-600 hover:text-indigo-500"
              >
                Add your first item
              </Link>
            )}
          </div>
        )}

        {/* Media grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-2">
                <span className="text-xs font-medium text-indigo-600 uppercase">
                  {typeLabels[item.mediaType]}
                </span>
                <span
                  className={`text-xs px-2 py-1 rounded-full font-medium ${
                    statusColors[item.status]
                  }`}
                >
                  {item.status}
                </span>
              </div>

              <h3 className="font-semibold text-gray-900 mb-1">{item.title}</h3>

              {item.genre && (
                <p className="text-sm text-gray-500 mb-2">{item.genre}</p>
              )}

              {item.rating && (
                <div className="flex items-center gap-1 mb-2">
                  <span className="text-yellow-500">{'★'.repeat(item.rating)}</span>
                  <span className="text-gray-400">{'★'.repeat(5 - item.rating)}</span>
                </div>
              )}

              <div className="flex gap-2 mt-3">
                <Link
                  to={`/media/${item.id}`}
                  className="text-sm text-indigo-600 hover:text-indigo-500"
                >
                  View
                </Link>
                <Link
                  to={`/media/${item.id}/edit`}
                  className="text-sm text-gray-600 hover:text-gray-500"
                >
                  Edit
                </Link>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="text-sm text-red-600 hover:text-red-500"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

/*
 * StatCard is a presentational component — it only handles rendering.
 * It receives data via props and has no state or side effects.
 * This is a "dumb component" or "pure component."
 */
function StatCard({ label, value, color }: { label: string; value: string | number; color: string }) {
  const colorClasses: Record<string, string> = {
    indigo: 'text-indigo-600',
    blue: 'text-blue-600',
    green: 'text-green-600',
    purple: 'text-purple-600',
    yellow: 'text-yellow-600',
    orange: 'text-orange-600',
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 text-center">
      <p className={`text-2xl font-bold ${colorClasses[color] || 'text-gray-600'}`}>{value}</p>
      <p className="text-xs text-gray-500 mt-1">{label}</p>
    </div>
  );
}
