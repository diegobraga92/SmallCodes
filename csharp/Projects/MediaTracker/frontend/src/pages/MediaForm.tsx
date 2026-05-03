import { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { mediaService } from '../services/mediaService';
import { MediaType, MediaStatus } from '../types/media';
import type { CreateMediaItem, UpdateMediaItem } from '../types/media';

/*
 * MediaForm handles both creating and editing media items.
 * It uses the same form for both operations — the isEdit flag
 * (derived from whether an :id param exists) determines the mode.
 *
 * This is called a "dual-purpose component" — it handles two related
 * use cases with shared UI. The alternative is separate Create and Edit
 * components, which would duplicate a lot of code.
 */

// Initial form state — all fields empty/default
const INITIAL_FORM_DATA: CreateMediaItem = {
  title: '',
  description: '',
  genre: '',
  status: MediaStatus.NotStarted,
  rating: undefined,
  mediaType: MediaType.Book,
  author: '',
  pages: undefined,
  isbn: '',
  platform: '',
  developer: '',
  publisher: '',
  hoursPlayed: undefined,
  director: '',
  durationMinutes: undefined,
  releaseYear: undefined,
};

export default function MediaForm() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEdit = !!id;

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<CreateMediaItem>(INITIAL_FORM_DATA);

  /*
   * If editing, fetch the existing item and populate the form.
   * The effect runs once when the component mounts (or when id changes).
   */
  useEffect(() => {
    if (isEdit && id) {
      setLoading(true);
      mediaService
        .getById(id)
        .then((item) => {
          setFormData({
            title: item.title,
            description: item.description || '',
            genre: item.genre || '',
            status: item.status,
            rating: item.rating,
            mediaType: item.mediaType,
            author: item.author || '',
            pages: item.pages,
            isbn: item.isbn || '',
            platform: item.platform || '',
            developer: item.developer || '',
            publisher: item.publisher || '',
            hoursPlayed: item.hoursPlayed,
            director: item.director || '',
            durationMinutes: item.durationMinutes,
            releaseYear: item.releaseYear,
          });
        })
        .catch(() => setError('Failed to load media item'))
        .finally(() => setLoading(false));
    }
  }, [id, isEdit]);

  /*
   * Generic change handler for text inputs and selects.
   * Uses the input's "name" attribute to determine which field to update.
   * This avoids having a separate handler for each field.
   *
   * If the value is empty string, we set it to undefined (so the backend
   * treats it as "no value" rather than "empty string").
   */
  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
      const { name, value } = e.target;
      setFormData((prev) => ({
        ...prev,
        [name]: value === '' ? undefined : value,
      }));
    },
    []
  );

  /*
   * Separate handler for number inputs (parseInt instead of string).
   */
  const handleNumberChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value === '' ? undefined : parseInt(value, 10),
    }));
  }, []);

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      setLoading(true);
      setError(null);

      try {
        if (isEdit && id) {
          /*
           * For updates, exclude mediaType (it's immutable — you can't change
           * a Book into a Movie). The backend doesn't accept mediaType in updates.
           */
          const { mediaType: _type, ...rest } = formData;
          const updateData: UpdateMediaItem = rest;
          await mediaService.update(id, updateData);
        } else {
          await mediaService.create(formData);
        }
        navigate('/');
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to save media item');
      } finally {
        setLoading(false);
      }
    },
    [id, isEdit, formData, navigate]
  );

  // Loading spinner while fetching existing item for edit
  if (loading && isEdit) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">
          {isEdit ? 'Edit Media Item' : 'Add New Media'}
        </h1>

        {error && (
          <div className="bg-red-50 text-red-700 p-3 rounded-md text-sm mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-sm">
          {/* Media Type — disabled when editing because it's immutable */}
          <FormField label="Media Type" name="mediaType">
            <select
              name="mediaType"
              value={formData.mediaType}
              onChange={handleChange}
              disabled={isEdit}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-100"
            >
              {Object.values(MediaType).map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </FormField>

          {/* Common fields */}
          <FormField label="Title *" name="title">
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              maxLength={200}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </FormField>

          <FormField label="Description" name="description">
            <textarea
              name="description"
              value={formData.description || ''}
              onChange={handleChange}
              rows={3}
              maxLength={2000}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </FormField>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <FormField label="Genre" name="genre">
              <input
                type="text"
                name="genre"
                value={formData.genre || ''}
                onChange={handleChange}
                maxLength={100}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </FormField>
            <FormField label="Status" name="status">
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              >
                {Object.values(MediaStatus).map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </FormField>
          </div>

          <FormField label="Rating (1-5)" name="rating">
            <input
              type="number"
              name="rating"
              min={1}
              max={5}
              value={formData.rating ?? ''}
              onChange={handleNumberChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            />
          </FormField>

          {/* Type-specific fields — conditionally rendered based on selected mediaType */}
          {formData.mediaType === MediaType.Book && (
            <div className="border-t pt-4 space-y-4">
              <h3 className="font-medium text-gray-900">Book Details</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <FormField label="Author" name="author">
                  <input
                    type="text"
                    name="author"
                    value={formData.author || ''}
                    onChange={handleChange}
                    maxLength={200}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </FormField>
                <FormField label="Pages" name="pages">
                  <input
                    type="number"
                    name="pages"
                    value={formData.pages ?? ''}
                    onChange={handleNumberChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </FormField>
              </div>
              <FormField label="ISBN" name="isbn">
                <input
                  type="text"
                  name="isbn"
                  value={formData.isbn || ''}
                  onChange={handleChange}
                  maxLength={20}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </FormField>
            </div>
          )}

          {formData.mediaType === MediaType.Game && (
            <div className="border-t pt-4 space-y-4">
              <h3 className="font-medium text-gray-900">Game Details</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <FormField label="Platform" name="platform">
                  <input
                    type="text"
                    name="platform"
                    value={formData.platform || ''}
                    onChange={handleChange}
                    maxLength={100}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </FormField>
                <FormField label="Developer" name="developer">
                  <input
                    type="text"
                    name="developer"
                    value={formData.developer || ''}
                    onChange={handleChange}
                    maxLength={200}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </FormField>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <FormField label="Publisher" name="publisher">
                  <input
                    type="text"
                    name="publisher"
                    value={formData.publisher || ''}
                    onChange={handleChange}
                    maxLength={200}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </FormField>
                <FormField label="Hours Played" name="hoursPlayed">
                  <input
                    type="number"
                    name="hoursPlayed"
                    value={formData.hoursPlayed ?? ''}
                    onChange={handleNumberChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </FormField>
              </div>
            </div>
          )}

          {formData.mediaType === MediaType.Movie && (
            <div className="border-t pt-4 space-y-4">
              <h3 className="font-medium text-gray-900">Movie Details</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <FormField label="Director" name="director">
                  <input
                    type="text"
                    name="director"
                    value={formData.director || ''}
                    onChange={handleChange}
                    maxLength={200}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </FormField>
                <FormField label="Duration (minutes)" name="durationMinutes">
                  <input
                    type="number"
                    name="durationMinutes"
                    value={formData.durationMinutes ?? ''}
                    onChange={handleNumberChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </FormField>
              </div>
              <FormField label="Release Year" name="releaseYear">
                <input
                  type="number"
                  name="releaseYear"
                  value={formData.releaseYear ?? ''}
                  onChange={handleNumberChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </FormField>
            </div>
          )}

          {/* Submit buttons */}
          <div className="flex gap-3">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {loading ? 'Saving...' : isEdit ? 'Update' : 'Create'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/')}
              className="flex-1 bg-gray-200 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

/*
 * FormField is a small presentational component that wraps a form field
 * with a label. It reduces repetition in the form — instead of writing
 * the label div + children pattern for every field, we just use <FormField>.
 */
function FormField({
  label,
  name,
  children,
}: {
  label: string;
  name: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      {children}
    </div>
  );
}
