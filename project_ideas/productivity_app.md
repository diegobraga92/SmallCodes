# FocusFlow – Personal Productivity Platform

## Overview
A private, self‑hosted productivity suite that consolidates task management, habit tracking, focus timers, white noise, meal planning, and book tracking into a single, clean web and phone interface. Built primarily to deepen my **Golang**, **Cloud (AWS/Terraform)**, and **backend system design** skills while creating a tool I will actually use every day.

**Core principle:** local‑first, cloud‑mirrored so it works offline and respects privacy, with optional sync and backups.

## Learning Objectives (Gaps Filled)
- **Golang**: Production‑grade backend with concurrency (goroutines, timers, workers), REST/gRPC APIs, robust testing, and profiling.
- **Backend Architecture**: Scheduled tasks (cron‑like), idempotent reminders, flexible habit engine, pomodoro state machine.
- **Cloud & DevOps**:
  - Infrastructure as Code with Terraform (AWS EC2 + S3 + SQS + SES).
  - CI/CD pipeline (GitHub Actions) to build, test, and deploy.
  - Message queues for async jobs (RabbitMQ or SQS).
  - Observability: structured logging, metrics, and alerting.
- **Solidification**: Keeps frontend (React/Vue) and React Native/Expo skills sharp, plus Rust for a small utility (optional).

## Core Features (MVP)
1. **Todo & Daily Tasks**
   - Create lists, set priorities, due dates, recurring tasks.
   - Drag‑and‑drop reordering, tags, quick capture inbox.
2. **Habit Formation**
   - Define daily/weekly habits with streaks and completion calendar.
   - Flexible scheduling (e.g., “3 times per week”, “every weekday”).
3. **Pomodoro Timer**
   - Configurable work/break intervals, auto‑start next session.
   - Track focus hours, daily goals, and interruption log.
4. **White Noise Generator**
   - Combines sounds (rain, fan, café) with custom mix curves.
   - Timer to fade out after pomodoro ends.
5. **Meal Planning**
   - Weekly meal calendar with drag‑and‑drop recipes.
   - Shopping list auto‑generated from recipes.
6. **Book Tracking**
   - Search/add books by ISBN or title (Open Library API).
   - Track reading status, notes, and personal rating.

## Tech Stack
### Backend (Golang)
- **Web framework:** `chi` or `gin` for HTTP routing.
- **Database:** PostgreSQL (primary), Redis (caching/sessions).
- **Scheduling:** Custom task scheduler with `robfig/cron` or a job queue pattern.
- **Real‑time:** WebSockets via `gorilla/websocket` for timer sync, live updates.
- **API:** REST (with optional gRPC for internal services later).
- **Testing:** Table‑driven tests, `testify`, integration tests with `testcontainers-go`.

### Frontend & Mobile
- **Web:** React + TypeScript (or Vue 3) with Tailwind CSS.
- **Mobile:** React Native (Expo) or PWA for cross‑platform simplicity.

### Cloud & Infrastructure
- **Compute:** AWS EC2 (single instance, t3.micro for start) or ECS Fargate.
- **Storage:** S3 for backups, RDS PostgreSQL, ElastiCache (Redis optional).
- **Messaging:** RabbitMQ (self‑managed on EC2 or Amazon MQ) or SQS for reminder dispatching.
- **IaC:** Terraform for all resources, remote state in S3.
- **CI/CD:** GitHub Actions → Docker build → push to ECR → deploy to ECS/Fargate.

### Local Development
- Docker Compose with all services: Go app, PostgreSQL, Redis, RabbitMQ.
- Hot‑reload with `air` or similar.

## Architecture Diagram (Logical)
[React Web / React Native]
│
REST + WS
│
[Go API Server]────[Redis Cache]
│
┌────┴────────────┐
[PostgreSQL DB] [Message Queue (RabbitMQ/SQS)]
│
[Background Workers] ──> [Email/SMS via SES]


## Data Models (Key Entities)
- **User**: auth, settings, premium flags.
- **Task**: title, description, due date, recurrence rule, list, order, completed.
- **Habit**: name, frequency config, current streak, longest streak, log entries.
- **PomodoroSession**: start time, end time, type (work/break), interruption count, completed.
- **SoundMix**: name, track volumes (rain, thunder, etc.).
- **MealPlan**: day, meal type, recipe reference.
- **Recipe**: name, ingredients, instructions, servings.
- **Book**: title, author, isbn, status, rating, notes.

## Implementation Phases
### Phase 1: Backend Core & Infrastructure (Weeks 1‑4)
- Scaffold Go project structure (clean architecture: handlers, services, repositories).
- Setup Docker Compose with PostgreSQL + RabbitMQ.
- Implement user auth (JWT) and basic user management.
- Design DB schema and run migrations.
- Write Terraform configs for AWS environment (EC2, RDS, S3, IAM).
- CI pipeline that runs linters, tests, builds Docker image.
- Deploy “Hello World” API to AWS.

### Phase 2: Task, Habit, Pomodoro (Weeks 5‑8)
- Task CRUD with reordering and recurrence logic.
- Habit engine: calculate streaks, compute next due date.
- Pomodoro timer state machine with WebSocket push.
- Implement first background worker: send daily habit reminder email via queue.
- Integrate RabbitMQ/SQS for reminder delivery.

### Phase 3: White Noise, Meal Plan, Books (Weeks 9‑12)
- White noise: store mixes, stream audio files (static or generated).
- Meal planning: recipe management, drag‑and‑drop weekly grid, shopping list aggregation.
- Book tracker: search via Open Library API, log status and notes.
- All features backed by proper REST endpoints and tests.

### Phase 4: Mobile & Polish (Weeks 13‑16)
- Build React Native app (or PWA) with full offline support (local storage synced to API).
- Push notifications via Firebase Cloud Messaging or Expo Notifications.
- End‑to‑end tests and performance profiling (pprof).
- Write comprehensive documentation and a demo video.

## Gap‑Filling Deep Dives
### Golang
- **Concurrency patterns:** goroutine pools for background jobs, channels for timer broadcast.
- **Profiling:** use `pprof` to optimize habit recalculation queries.
- **Testing:** integration tests with real DB in Docker, mocking external APIs.

### Cloud
- **Terraform:** multi‑environment (dev/prod) with workspaces, modules for SQS, RDS, EC2.
- **Cost control:** setup budget alerts and `terraform destroy` schedule for unused resources.
- **Monitoring:** CloudWatch dashboards for API latency, queue depth, error rates.

### RabbitMQ/SQS (Optional Deep Dive)
- **Exchange types:** direct exchanges for reminder routing.
- **Dead‑letter queues:** handle failed habit reminders gracefully.
- **Idempotency:** prevent duplicate email sends using message IDs.

## Non‑Goals (for this project)
- No embedded/hardware component – to focus on pure Go/cloud.
- No AI/ML – leave that for the Finance project later.
- No Rust microservices – Solidify Rust separately in SafeSync & Finance.

## Why I’ll Actually Use This
- Consolidates five apps I currently juggle into one private, self‑hosted tool.
- Works offline when I travel, syncs later when connected.
- Gives me total control over data – no ads, no subscriptions, no privacy leaks.

---

**Author:** Diego Braga  
**Status:** Planning phase – ready to start scaffolding.