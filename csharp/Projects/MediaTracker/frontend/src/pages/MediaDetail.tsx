import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { mediaService } from '../services/mediaService';
import type { MediaItem } from '../types/media';
import { MediaStatus, MediaType } from '../types/media';

/*
 * MediaDetail displays a single media item with all its properties.
 * It handles three states:
 * 1. Loading — show spinner while fetching
 * 2. Error/Not found — show error message with back link
 * 3. Success — show the item details
 */

const statusColors: Record<MediaStatus, string> = {
  [MediaStatus.NotStarted]: 'bg-gray-100 text-gray-800',
  [MediaStatus.InProgress]: 'bg-blue-100 text-blue-800',
  [MediaStatus.Completed]: 'bg-green-100 text-green-800',
  [MediaStatus.OnHold]: 'bg-yellow-100 text-yellow-800',
  [MediaStatus.Dropped]: 'bg-red-100 text-red-800',
};

const typeLabels: Record<MediaType, string> = {
  [MediaType.Book]: 'Book',
  [MediaType.Game]: 'Game',
  [MediaType.Movie]: 'Movie',
};

export default function MediaDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [item, setItem] = useState<MediaItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /*
   * Fetch the item when the component mounts or id changes.
   * The cleanup (return from useEffect) isn't needed here because
   * there's no subscription or timer to clean up.
   */
  useEffect(() => {
    if (!id) return;
    setLoading(true);
    mediaService
      .getById(id)
      .then(setItem)
      .catch(() => setError('Failed to load media item'))
      .finally(() => setLoading(false));
  }, [id]);

  const handleDelete = useCallback(async () => {
    if (!id || !window.confirm('Are you sure you want to delete this item?')) return;
    try {
      await mediaService.delete(id);
      navigate('/');
    } catch {
      setError('Failed to delete item');
    }
  }, [id, navigate]);

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  // Error state
  if (error || !item) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Item not found'}</p>
          <Link to="/" className="text-indigo-600 hover:text-indigo-500">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  // Success state — render the item details
  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <Link to="/" className="text-indigo-600 hover:text-indigo-500 mb-4 inline-block">
          &larr; Back to Dashboard
        </Link>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <span className="text-sm font-medium text-indigo-600 uppercase">
                {typeLabels[item.mediaType]}
              </span>
              <h1 className="text-2xl font-bold text-gray-900 mt-1">{item.title}</h1>
            </div>
            <span
              className={`text-sm px-3 py-1 rounded-full font-medium ${
                statusColors[item.status]
              }`}
            >
              {item.status}
            </span>
          </div>

          {item.genre && (
            <p className="text-gray-600 mb-2">
              <span className="font-medium">Genre:</span> {item.genre}
            </p>
          )}

          {item.rating != null && (
            <div className="flex items-center gap-1 mb-4">
              <span className="text-yellow-500 text-lg">
                {'★'.repeat(item.rating)}
              </span>
              <span className="text-gray-400 text-lg">
                {'★'.repeat(5 - item.rating)}
              </span>
              <span className="text-gray-500 text-sm ml-1">({item.rating}/5)</span>
            </div>
          )}

          {item.description && (
            <div className="mb-4">
              <h3 className="font-medium text-gray-900 mb-1">Description</h3>
              <p className="text-gray-600">{item.description}</p>
            </div>
          )}

          {/* Type-specific details — conditionally rendered */}
          {item.mediaType === MediaType.Book && (
            <div className="border-t pt-4 mt-4">
              <h3 className="font-medium text-gray-900 mb-2">Book Details</h3>
              <dl className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {item.author && <DetailField label="Author" value={item.author} />}
                {item.pages != null && <DetailField label="Pages" value={item.pages} />}
                {item.isbn && <DetailField label="ISBN" value={item.isbn} />}
              </dl>
            </div>
          )}

          {item.mediaType === MediaType.Game && (
            <div className="border-t pt-4 mt-4">
              <h3 className="font-medium text-gray-900 mb-2">Game Details</h3>
              <dl className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {item.platform && <DetailField label="Platform" value={item.platform} />}
                {item.developer && <DetailField label="Developer" value={item.developer} />}
                {item.publisher && <DetailField label="Publisher" value={item.publisher} />}
                {item.hoursPlayed != null && (
                  <DetailField label="Hours Played" value={item.hoursPlayed} />
                )}
              </dl>
            </div>
          )}

          {item.mediaType === MediaType.Movie && (
            <div className="border-t pt-4 mt-4">
              <h3 className="font-medium text-gray-900 mb-2">Movie Details</h3>
              <dl className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {item.director && <DetailField label="Director" value={item.director} />}
                {item.durationMinutes != null && (
                  <DetailField label="Duration" value={`${item.durationMinutes} min`} />
                )}
                {item.releaseYear != null && (
                  <DetailField label="Release Year" value={item.releaseYear} />
                )}
              </dl>
            </div>
          )}

          {/* Action buttons */}
          <div className="flex gap-3 mt-6 pt-4 border-t">
            <Link
              to={`/media/${item.id}/edit`}
              className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700"
            >
              Edit
            </Link>
            <button
              onClick={handleDelete}
              className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

/*
 * DetailField is a small presentational component for displaying
 * a key-value pair in a definition list (<dl>).
 */
function DetailField({ label, value }: { label: string; value: string | number }) {
  return (
    <div>
      <dt className="text-sm text-gray-500">{label}</dt>
      <dd className="text-gray-900">{value}</dd>
    </div>
  );
}
