/*
 * These TypeScript types mirror the C# DTOs from the backend.
 * They define the contract between frontend and backend.
 *
 * Why define types separately instead of auto-generating from the API?
 * Auto-generation tools (like OpenAPI generators) exist, but manual types give us:
 * 1. Full control over the type definitions
 * 2. No build-time dependency on the API being running
 * 3. Ability to add frontend-specific types (like AuthResponse, LoginRequest)
 *
 * Tradeoff: Types can drift from the backend if not kept in sync.
 */

/*
 * Enums in TypeScript work differently than in C#.
 * In C#, enums are numeric by default (NotStarted = 0, InProgress = 1, etc.).
 * In TypeScript, we use string enums to match the JSON serialization
 * (JsonStringEnumConverter on the backend converts enums to strings).
 *
 * If the backend used numeric enum values, we'd need to map them here.
 */
export enum MediaStatus {
  NotStarted = 'NotStarted',
  InProgress = 'InProgress',
  Completed = 'Completed',
  OnHold = 'OnHold',
  Dropped = 'Dropped',
}

export enum MediaType {
  Book = 'Book',
  Game = 'Game',
  Movie = 'Movie',
}

/*
 * MediaItem interface — matches MediaItemDto from the backend.
 * All type-specific fields are optional (?) because they only apply
 * to certain media types. The frontend checks mediaType to know
 * which fields to display.
 *
 * This "flattened" approach means the frontend has one type to handle
 * instead of three (BookItem, GameItem, MovieItem). The tradeoff is
 * that TypeScript can't enforce "author is required for books" at
 * the type level — that logic must be in the UI code.
 */
export interface MediaItem {
  id: string;
  title: string;
  description?: string;
  genre?: string;
  status: MediaStatus;
  rating?: number;
  mediaType: MediaType;
  createdAt: string;
  updatedAt: string;

  // Book-specific
  author?: string;
  pages?: number;
  isbn?: string;

  // Game-specific
  platform?: string;
  developer?: string;
  publisher?: string;
  hoursPlayed?: number;

  // Movie-specific
  director?: string;
  durationMinutes?: number;
  releaseYear?: number;
}

/*
 * CreateMediaItem — matches CreateMediaItemDto from the backend.
 * Note: No userId field here either! The backend extracts it from the JWT.
 */
export interface CreateMediaItem {
  title: string;
  description?: string;
  genre?: string;
  status?: MediaStatus;
  rating?: number;
  mediaType: MediaType;

  author?: string;
  pages?: number;
  isbn?: string;
  platform?: string;
  developer?: string;
  publisher?: string;
  hoursPlayed?: number;
  director?: string;
  durationMinutes?: number;
  releaseYear?: number;
}

/*
 * UpdateMediaItem — matches UpdateMediaItemDto from the backend.
 * All fields are optional for partial updates.
 */
export interface UpdateMediaItem {
  title?: string;
  description?: string;
  genre?: string;
  status?: MediaStatus;
  rating?: number;
  author?: string;
  pages?: number;
  isbn?: string;
  platform?: string;
  developer?: string;
  publisher?: string;
  hoursPlayed?: number;
  director?: string;
  durationMinutes?: number;
  releaseYear?: number;
}

/*
 * Auth types — these are frontend-specific and don't directly map to
 * backend DTOs. AuthResponse matches AuthResponseDto from the backend.
 * LoginRequest and RegisterRequest are sent to the API.
 */
export interface AuthResponse {
  token: string;
  userId: string;
  email: string;
  username: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  username: string;
}
