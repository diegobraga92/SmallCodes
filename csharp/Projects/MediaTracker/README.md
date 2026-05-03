# MediaTracker

A full-stack media tracking application for tracking books, games, and movies. Built with **.NET 10** (Web API) and **React + TypeScript** (Vite).

## Features

- **User Authentication** - Register and login with JWT-based authentication
- **Media Management** - Create, read, update, and delete media items
- **Media Types** - Books, Games, and Movies with type-specific fields
- **Status Tracking** - Track progress: Not Started, In Progress, Completed, On Hold, Dropped
- **Rating System** - Rate items on a 1-5 scale
- **Filtering** - Filter media by type
- **Search** - Search by title, description, or genre
- **Sorting** - Sort by title, rating, status, date added, or last updated
- **Statistics Dashboard** - Overview cards showing totals, completed items, and average rating
- **Responsive Design** - Mobile-first UI with Tailwind CSS
- **Docker Support** - Run the entire stack with a single command

## Tech Stack

### Backend
- **.NET 10** Web API
- **Entity Framework Core 10** with PostgreSQL (Npgsql)
- **ASP.NET Core Identity** for user management
- **JWT Bearer Authentication**
- **Table Per Hierarchy (TPH)** inheritance for media types

### Frontend
- **React 18** with TypeScript
- **Vite** build tool
- **React Router v6** for routing
- **Axios** for HTTP requests with JWT interceptor
- **Tailwind CSS 3** for styling

### Infrastructure
- **PostgreSQL 16** (via Docker Compose)
- **Docker** - Containerized backend (.NET) and frontend (Nginx)

## Project Structure

```
MediaTracker/
├── backend/
│   └── MediaTracker.Api/
│       ├── Controllers/
│       │   ├── AuthController.cs      # Register/Login endpoints
│       │   ├── MediaController.cs     # CRUD endpoints for media
│       │   └── StatsController.cs     # Statistics endpoint
│       ├── Models/
│       │   ├── MediaItem.cs           # Base abstract class
│       │   ├── Book.cs                # Book-specific properties
│       │   ├── Game.cs                # Game-specific properties
│       │   └── Movie.cs               # Movie-specific properties
│       ├── Data/
│       │   └── AppDbContext.cs        # EF Core DbContext with TPH config
│       ├── Migrations/                # EF Core migrations
│       ├── DTOs/
│       │   ├── AuthDtos.cs            # Login/Register/Response DTOs
│       │   ├── MediaItemDtos.cs       # Create/Update/Response DTOs
│       │   └── StatsDtos.cs           # Statistics response DTO
│       ├── Services/
│       │   ├── IAuthService.cs        # Auth service interface
│       │   ├── AuthService.cs         # JWT token generation & auth logic
│       │   ├── IMediaService.cs       # Media service interface
│       │   ├── MediaService.cs        # Media CRUD + search/sort logic
│       │   ├── IStatsService.cs       # Stats service interface
│       │   └── StatsService.cs        # Statistics calculation logic
│       ├── Program.cs                 # App configuration & startup
│       ├── appsettings.json           # Configuration (DB, JWT)
│       └── Dockerfile                 # .NET Docker image
├── frontend/
│   ├── src/
│   │   ├── components/                # Reusable UI components
│   │   ├── pages/
│   │   │   ├── Login.tsx              # Login page
│   │   │   ├── Register.tsx           # Registration page
│   │   │   ├── Dashboard.tsx          # Main media list with search, sort, stats
│   │   │   ├── MediaForm.tsx          # Create/Edit media form
│   │   │   └── MediaDetail.tsx        # Media item detail view
│   │   ├── services/
│   │   │   ├── api.ts                 # Axios instance with JWT interceptor
│   │   │   ├── authService.ts         # Auth API calls
│   │   │   ├── mediaService.ts        # Media API calls
│   │   │   └── statsService.ts        # Stats API calls
│   │   ├── types/
│   │   │   └── media.ts               # TypeScript interfaces & enums
│   │   ├── hooks/
│   │   │   ├── useAuth.ts             # Auth state management hook
│   │   │   └── useMedia.ts            # Media state management hook
│   │   ├── App.tsx                    # Router configuration
│   │   └── main.tsx                   # App entry point
│   ├── Dockerfile                     # Nginx Docker image
│   ├── nginx.conf                     # Nginx SPA routing config
│   └── package.json
├── docker-compose.yml                 # PostgreSQL + API + Frontend
└── README.md
```

## Getting Started

### Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download)
- [Node.js 18+](https://nodejs.org/)
- [Docker](https://docker.com/) (for PostgreSQL)

### Option A: Run with Docker (Full Stack)

```bash
# Start everything (PostgreSQL, API, Frontend)
docker compose up -d

# The app will be available at http://localhost:5173
```

### Option B: Run Locally (Development)

#### 1. Start PostgreSQL

```bash
docker compose up -d postgres
```

This starts a PostgreSQL 16 container on port `5432` with:
- Database: `mediatracker`
- Username: `mediatracker`
- Password: `mediatracker123`

#### 2. Run the Backend

```bash
cd backend/MediaTracker.Api
dotnet run
```

The API will start on `http://localhost:5000`.

The database will be automatically migrated on startup (tables created via EF Core migrations).

#### 3. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will start on `http://localhost:5173`.

#### 4. Open the App

Navigate to [http://localhost:5173](http://localhost:5173) in your browser.

1. **Register** a new account
2. **Login** with your credentials
3. **Add media** items (books, games, or movies)
4. **Track** your progress and rate your media

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and get JWT token |

### Media Items (requires JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/media` | Get all media items (see query params below) |
| GET | `/api/media/{id}` | Get a specific media item |
| POST | `/api/media` | Create a new media item |
| PUT | `/api/media/{id}` | Update a media item |
| DELETE | `/api/media/{id}` | Delete a media item |

**Media Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | `Book\|Game\|Movie` | Filter by media type |
| `search` | string | Search by title, description, or genre |
| `sortBy` | `title\|rating\|status\|createdAt\|updatedAt` | Sort field (default: `updatedAt`) |
| `sortOrder` | `asc\|desc` | Sort direction (default: `desc`) |

### Statistics (requires JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats` | Get user statistics (totals, counts by type/status, avg rating) |

## Database Schema

The application uses **Table Per Hierarchy (TPH)** inheritance with a single `MediaItems` table and a discriminator column (`MediaType`).

```
MediaItems
├── Id (Guid, PK)
├── Title (string, required)
├── Description (string, optional)
├── Genre (string, optional)
├── Status (enum: NotStarted, InProgress, Completed, OnHold, Dropped)
├── Rating (int 1-5, optional)
├── MediaType (discriminator: Book, Game, Movie)
├── UserId (string, FK to AspNetUsers)
├── CreatedAt (DateTime)
├── UpdatedAt (DateTime)
├── Author (string, Book only)
├── Pages (int, Book only)
├── Isbn (string, Book only)
├── Platform (string, Game only)
├── Developer (string, Game only)
├── Publisher (string, Game only)
├── HoursPlayed (int, Game only)
├── Director (string, Movie only)
├── DurationMinutes (int, Movie only)
└── ReleaseYear (int, Movie only)
```

## Future Enhancements

- **More Media Types** - TV Series, Podcasts, Comics, Music Albums
- **Lists & Collections** - Custom curated lists
- **Import/Export** - CSV/JSON import and export
- **Image Upload** - Cover art for media items
- **Social Features** - Share lists, follow users
- **Activity Feed** - Timeline of recent activity
- **Mobile App** - Wrap with Capacitor or React Native

## License

MIT
