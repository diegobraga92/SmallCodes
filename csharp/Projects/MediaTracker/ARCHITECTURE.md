# Architecture

This document explains the architectural decisions, reasoning, and tradeoffs behind MediaTracker. It is intended for educational purposes — to understand *why* things are built the way they are, not just *what* was built.

---

## Table of Contents

1. [High-Level Architecture](#1-high-level-architecture)
2. [Backend Architecture](#2-backend-architecture)
3. [Domain Model & Inheritance Strategy (TPH)](#3-domain-model--inheritance-strategy-tph)
4. [Authentication & Authorization](#4-authentication--authorization)
5. [Frontend Architecture](#5-frontend-architecture)
6. [Data Flow](#6-data-flow)
7. [Configuration & Environment](#7-configuration--environment)
8. [Database Schema Design](#8-database-schema-design)
9. [Containerization Decisions](#9-containerization-decisions)
10. [Educational Value & Design Tradeoffs Summary](#10-educational-value--design-tradeoffs-summary)

---

## 1. High-Level Architecture

MediaTracker follows a classic **three-tier architecture**:

```
┌──────────────┐     ┌──────────────────┐     ┌────────────┐
│  React SPA   │────▶│  .NET 10 Web API │────▶│ PostgreSQL │
│  (Vite)      │     │  (Controllers →  │     │    16      │
│              │◀────│   Services →     │◀────│            │
│  Nginx       │     │   EF Core)       │     │            │
└──────────────┘     └──────────────────┘     └────────────┘
```

**Why three tiers?** Separation of concerns. The frontend only handles UI and user interaction. The backend encapsulates business logic and data access. The database stores data. Each layer can be developed, tested, and scaled independently.

**Docker Compose** orchestrates three containers:
- `postgres` — PostgreSQL 16 database
- `api` — .NET 10 Web API
- `frontend` — Nginx serving the built React SPA

**Communication flow:**
1. The browser loads the SPA from Nginx (port 5173)
2. API requests (`/api/*`) are **reverse-proxied** by Nginx to the .NET backend (port 8080 internal)
3. The backend communicates with PostgreSQL (port 5432)

This means the browser only ever talks to one origin — no CORS issues in production. The `AllowAnyOrigin` CORS policy in the backend is only needed for local development when running the frontend dev server separately.

---

## 2. Backend Architecture

### Layered Pattern

```
Controllers  ──▶  Services  ──▶  EF Core DbContext  ──▶  PostgreSQL
   │                  │
   ▼                  ▼
  DTOs              Models
```

**Controllers** handle HTTP concerns: routing, request validation, response formatting. They are thin — no business logic.

**Services** contain business logic. They are injected into controllers via constructor injection.

**EF Core DbContext** handles data access. The service layer never touches the database directly.

**Why this layering?**
- **Testability**: Services can be unit-tested with mocked DbContexts. Controllers can be integration-tested.
- **Separation of concerns**: If the data access strategy changes (e.g., moving to Dapper or a different ORM), only the service layer changes.
- **Consistency**: All database queries go through the same DbContext configuration (TPH mapping, constraints, etc.).

### Dependency Injection

Services are registered with **scoped lifetime** in `Program.cs`:

```csharp
builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IMediaService, MediaService>();
builder.Services.AddScoped<IStatsService, StatsService>();
```

**Why scoped?** A new service instance is created per HTTP request. This aligns with the DbContext (also scoped), ensuring each request gets a fresh unit of work. Singleton would cause stale data and thread-safety issues. Transient would waste resources creating new instances for no benefit.

### DTO Pattern

The API uses **Data Transfer Objects (DTOs)** separate from the domain models (`MediaItem`, `Book`, etc.).

**Why not expose domain models directly?**
- **Security**: The `UserId` field is never sent from the client. It is extracted from the JWT token server-side. If we exposed the `MediaItem` entity directly, a client could set `UserId` to another user's ID.
- **API contract stability**: DTOs can evolve independently of the domain model. You can add fields to the domain model without breaking the API.
- **Flattening**: The DTO flattens the TPH hierarchy into a single object with all type-specific fields nullable. This is simpler for the frontend to consume than a discriminated union.

**Tradeoff**: The DTOs duplicate field definitions (three DTOs + the base model + three subtypes). This is boilerplate but intentional — it's the "safe" approach for API contracts.

---

## 3. Domain Model & Inheritance Strategy (TPH)

### Decision: Table Per Hierarchy

```csharp
public abstract class MediaItem { /* common fields */ }
public class Book : MediaItem { /* Author, Pages, Isbn */ }
public class Game : MediaItem { /* Platform, Developer, Publisher, HoursPlayed */ }
public class Movie : MediaItem { /* Director, DurationMinutes, ReleaseYear */ }
```

EF Core maps this to a **single table** `MediaItems` with a **discriminator column** `MediaType`:

```
MediaItems
├── Id (Guid, PK)
├── Title, Description, Genre, Status, Rating, MediaType (discriminator)
├── UserId, CreatedAt, UpdatedAt
├── Author (Book only, nullable)
├── Pages (Book only, nullable)
├── Isbn (Book only, nullable)
├── Platform (Game only, nullable)
├── Developer (Game only, nullable)
├── Publisher (Game only, nullable)
├── HoursPlayed (Game only, nullable)
├── Director (Movie only, nullable)
├── DurationMinutes (Movie only, nullable)
└── ReleaseYear (Movie only, nullable)
```

### Why TPH over other strategies?

| Strategy | Description | Why not chosen |
|----------|-------------|----------------|
| **TPH** (Table Per Hierarchy) | Single table with discriminator | ✅ Chosen — simplest for this scope |
| **TPT** (Table Per Type) | One table per class, joined | ❌ Complex queries, slower joins, more tables |
| **TPC** (Table Per Concrete) | One table per subclass, no shared table | ❌ Duplicate columns, hard to query across types |

### Reasoning

- **Simplicity**: One table, one query, no joins. The `GetAllAsync` method with filtering, searching, and sorting is a single LINQ query.
- **Query performance**: Filtering by `MediaType` is a simple `WHERE` clause on the discriminator column.
- **EF Core support**: TPH is the default and most mature inheritance mapping strategy in EF Core.

### Tradeoffs

- **Nullable columns**: All type-specific columns must be nullable. You cannot enforce `Author IS NOT NULL` at the database level for books. This must be enforced in application code.
- **Wasted space**: For a `Movie` row, the `Author`, `Pages`, `Isbn`, `Platform`, `Developer`, `Publisher`, and `HoursPlayed` columns are all `NULL`. With PostgreSQL's storage engine, nulls are cheap (1 bit per column in a null bitmap), but it's still conceptually wasteful.
- **Schema rigidity**: Adding a new media type (e.g., `TvSeries`) adds more nullable columns to the same table. At scale (dozens of types), the table becomes wide and sparse.
- **No foreign key constraints**: You cannot have a separate `Authors` table with a FK from `Book` rows, because the column exists for all rows.

**When would TPT or TPC be better?** If the project had many media types with very different fields, or if type-specific fields needed NOT NULL constraints or foreign keys, TPT would be more appropriate despite the query complexity.

---

## 4. Authentication & Authorization

### Decision: JWT Bearer Tokens + ASP.NET Core Identity

**Why JWT?**
- **Stateless**: The server does not need to store session state. The token contains all the information needed to authenticate the user.
- **SPA-friendly**: The frontend stores the token in `localStorage` and sends it with every request via an Axios interceptor.
- **Self-contained**: The token includes the user ID, email, username, and roles. No database lookup needed on each request.

**Why ASP.NET Core Identity?**
- **Batteries included**: User management, password hashing, role management, and EF Core integration out of the box.
- **Proven**: Battle-tested, well-documented, and actively maintained by Microsoft.

### Token Flow

1. User registers or logs in → backend validates credentials → generates JWT → returns it
2. Frontend stores token in `localStorage`
3. Axios interceptor attaches `Authorization: Bearer <token>` to every request
4. Backend validates the token on every request via the `[Authorize]` attribute
5. Controllers extract the user ID from `ClaimTypes.NameIdentifier`

### Tradeoffs

- **Token revocation**: JWTs are valid until they expire (default: 7 days). There is no way to revoke a token before expiry without maintaining a blacklist (which defeats the stateless purpose). For an educational project this is fine, but a production app would need refresh tokens or short-lived tokens.
- **localStorage storage**: Storing the JWT in `localStorage` makes it accessible to any JavaScript running on the same origin. This is **vulnerable to XSS attacks**. A more secure approach would be HTTP-only cookies, but that requires CSRF protection and more complex frontend logic. For an educational project, `localStorage` is simpler and sufficient.
- **Password validation**: The `RegisterDto` only requires `MinLength(6)` for passwords. ASP.NET Identity's default password policy is more strict (requires special chars, uppercase, etc.), but the DTO validation doesn't enforce this — the error comes from Identity's `CreateAsync` result. This could be confusing to users.

---

## 5. Frontend Architecture

### Component Tree

```
App.tsx (BrowserRouter)
├── /login          → Login.tsx
├── /register       → Register.tsx
├── /               → Dashboard.tsx (PrivateRoute)
├── /media/new      → MediaForm.tsx (PrivateRoute)
├── /media/:id      → MediaDetail.tsx (PrivateRoute)
└── /media/:id/edit → MediaForm.tsx (PrivateRoute)
```

### State Management Decision: No Global State Library

**Why not Redux, Zustand, or Context API?**
- **Scope**: The app has two main data domains — auth and media. Both are simple enough to manage with custom hooks + `localStorage`.
- **Simplicity**: Adding a state management library adds boilerplate (actions, reducers, stores) that isn't justified for this app's complexity.
- **Educational value**: Custom hooks demonstrate React patterns without abstraction overhead.

**Tradeoff**: If the app grew (e.g., real-time updates, complex caching, cross-page state), a library like Zustand or TanStack Query would become beneficial.

### Custom Hooks

**`useAuth`** — encapsulates login, register, logout, loading, and error state. Auth state (token, userId, username) is persisted in `localStorage` and read directly by components.

**`useMedia`** — encapsulates fetching, creating, updating, and deleting media items. It accepts filter/sort parameters and re-fetches when they change via `useEffect`.

**Why hooks instead of putting logic in components?**
- **Reusability**: `useMedia` could be used by multiple pages (Dashboard, a future "Favorites" page, etc.)
- **Separation**: Components focus on rendering; hooks focus on state and side effects.
- **Testability**: Hooks can be tested with `renderHook` from React Testing Library.

### Axios Interceptor Pattern

The Axios instance in `api.ts` has two interceptors:

1. **Request interceptor**: Attaches the JWT token from `localStorage` to every request.
2. **Response interceptor**: On 401 responses, clears auth state and redirects to `/login` — but **skips this for auth endpoints** to avoid redirect loops during login/register.

This is a common pattern that keeps individual service files clean — they don't need to worry about auth headers or error handling.

### Debounce Pattern

The search input on the Dashboard uses a custom `useDebounce` hook with a 300ms delay. This prevents sending an API request on every keystroke. The debounced value is passed to `useMedia`, which triggers a re-fetch when it changes.

**Tradeoff**: The debounce adds a slight UI delay (300ms) before results update. This is a good tradeoff — it reduces API calls significantly while feeling instant to the user.

---

## 6. Data Flow

Here's the full lifecycle of a typical request (e.g., creating a new book):

```
1. User fills form in MediaForm.tsx
2. Form submit calls mediaService.create(data)
3. Axios request interceptor attaches JWT token
4. HTTP POST /api/media with JSON body
5. Nginx proxies to .NET backend at http://api:8080
6. [Authorize] attribute validates JWT
7. MediaController.Create() extracts UserId from claims
8. MediaService.CreateAsync() creates Book entity
9. EF Core adds to DbSet and calls SaveChangesAsync()
10. PostgreSQL inserts row into MediaItems table
11. Response flows back: Book → MediaItemDto → JSON → HTTP → Axios → hook → component re-render
```

**Why this matters**: Each layer has a specific responsibility. If something breaks, you know exactly where to look. The JWT is validated at the controller level (step 6), so the service can trust `userId` without re-validating.

---

## 7. Configuration & Environment

### Configuration Sources

| Setting | Source | Example |
|---------|--------|---------|
| Database connection | `appsettings.json` or env var | `Host=localhost;Database=mediatracker;...` |
| JWT key | `appsettings.json` or env var | `MediaTrackerSuperSecretKey...` |
| JWT issuer/audience | `appsettings.json` or env var | `MediaTracker.Api` / `MediaTracker.Frontend` |

In Docker Compose, these are set as **environment variables** using the `__` separator convention for nested config (e.g., `ConnectionStrings__DefaultConnection`).

### Security Consideration

The JWT secret key is hardcoded in `docker-compose.yml` and `appsettings.Development.json`. This is fine for local development but **must** be moved to a secure store (e.g., Docker secrets, Azure Key Vault, environment variables in CI/CD) for any non-development deployment.

### CORS Policy

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});
```

**Why `AllowAnyOrigin`?** In development, the frontend runs on `localhost:5173` (Vite dev server) while the backend runs on `localhost:5000`. This is a cross-origin scenario. In production (Docker Compose), Nginx proxies all requests, so CORS isn't needed — but the policy remains permissive for flexibility.

**Tradeoff**: `AllowAnyOrigin` is not suitable for production. A production deployment would restrict origins to the actual frontend domain.

---

## 8. Database Schema Design

### EF Core Migrations

The database is **auto-migrated on startup** in `Program.cs`:

```csharp
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.Migrate();
}
```

**Why auto-migrate?** Convenience for development. No need to run `dotnet ef database update` manually. The database schema is always up-to-date with the code.

**Tradeoff**: Auto-migrating in production is dangerous. If a migration fails or has destructive changes (e.g., dropping a column), the app won't start. Production deployments should use controlled migration scripts with rollback plans.

### ASP.NET Identity Tables

In addition to `MediaItems`, EF Core Identity creates these tables:
- `AspNetUsers` — user accounts
- `AspNetRoles` — roles
- `AspNetUserRoles` — user-role assignments
- `AspNetUserClaims`, `AspNetUserLogins`, `AspNetUserTokens` — Identity infrastructure

The `UserId` column in `MediaItems` is a foreign key to `AspNetUsers.Id` (though not explicitly configured as a FK constraint in the current code — this is a potential improvement).

### Why Guid for Primary Keys?

`MediaItem.Id` uses `Guid.NewGuid()` (client-side generated). This avoids round-trips to the database for ID generation and makes it safe to create entities before persisting them. The tradeoff is that GUIDs are larger than auto-increment integers (16 bytes vs. 4-8 bytes) and can cause index fragmentation in some databases. PostgreSQL handles UUIDs reasonably well.

---

## 9. Containerization Decisions

### Why Separate Containers?

Each service runs in its own container:
- **PostgreSQL**: Database
- **API**: .NET application
- **Frontend**: Nginx serving static files

**Benefits:**
- **Independent scaling**: You could run multiple API instances behind a load balancer
- **Independent lifecycle**: Update the frontend without touching the backend
- **Clear boundaries**: Each container has a single responsibility

**Tradeoff**: More complexity than a monolith. You need Docker Compose (or Kubernetes) to orchestrate them. For a simple app, a single container running both the API and serving the frontend would be simpler.

### Nginx as Reverse Proxy

The frontend container runs Nginx, which:
1. Serves the built React SPA (static files)
2. Proxies `/api/*` requests to the backend container
3. Handles SPA routing (`try_files $uri /index.html`) — so refreshing `/media/123` works
4. Caches static assets with immutable cache headers

**Why Nginx instead of serving with Vite/Node?** Nginx is production-grade, lightweight, and handles static file serving and reverse proxying efficiently. The Vite dev server is only for development.

### Health Checks

PostgreSQL has a health check that waits for `pg_isready` before the API container starts. This prevents the API from crashing on startup because the database isn't ready yet.

**Tradeoff**: Docker Compose's `depends_on` with `condition: service_healthy` only waits for the database to be ready at the container level. The API's auto-migration could still fail if the database accepts connections but isn't fully initialized. A retry pattern in the application code would be more robust.

---

## 10. Educational Value & Design Tradeoffs Summary

### What Makes This a Good Teaching Project

- **Full-stack**: Covers frontend, backend, database, and infrastructure
- **Realistic patterns**: Dependency injection, DTOs, JWT auth, repository pattern (via services), TPH inheritance
- **Modern tech**: .NET 10, React 18, TypeScript, Vite, Tailwind CSS, Docker
- **Simple but not trivial**: Multiple media types with inheritance, search/sort/filter, auth, stats — enough complexity to demonstrate important patterns without being overwhelming

### Honest Tradeoff Assessment

| Decision | Tradeoff | When to Revisit |
|----------|----------|-----------------|
| TPH inheritance | Nullable columns, no FK constraints on subtype fields | Adding 5+ media types with distinct fields |
| JWT in localStorage | XSS vulnerability | Before any production deployment |
| Auto-migrate on startup | Dangerous for production | Before deploying to production |
| AllowAnyOrigin CORS | Insecure for production | When deploying with a known frontend domain |
| No global state library | Manual prop drilling if app grows | When adding cross-page state or caching |
| Flat DTO with all fields | Boilerplate, no type safety per media type | When adding many media types with very different fields |
| Hardcoded JWT secret in docker-compose.yml | Security risk | Before sharing the repo publicly or deploying |
| No refresh tokens | Can't revoke tokens, long expiry | When user sessions need fine-grained control |
| No explicit FK from MediaItems.UserId to AspNetUsers | Referential integrity not enforced at DB level | When data integrity is critical |

---

*This document is a living artifact. As the project evolves, update this document to reflect new decisions and tradeoffs.*
