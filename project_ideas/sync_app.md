# SafeSync – Personal Backup & Sync Agent

## Overview
A cross‑platform (Linux, macOS, Windows) backup agent and coordination server that provides deduplicated, encrypted, versioned backups of my most important files to cloud object storage. The system is designed to replace commercial backup tools, giving me full control over data security and retention policies while serving as a deep learning sandbox for **Rust backend engineering**, **advanced cloud storage infrastructure (Terraform)**, **sync protocol design**, and **reliability engineering**.

**Core principle:** local agent syncs changes to a Rust coordination server, which handles versioning, conflict resolution, and secure cloud uploads. The entire cloud footprint is managed as code.

## Learning Objectives (Gaps Filled)
- **Rust Backend (Solidification):** Build a highly‑available coordination server in Rust (Axum) that manages device authentication, sync state, version history, and restore APIs.
- **Cloud Engineering (Deep Dive):** 
  - Terraform for object storage infrastructure (S3/Backblaze B2), IAM, KMS encryption, lifecycle policies, cost alerting.
  - Cloud‑native storage patterns: versioning, object locking, replication, multipart uploads.
- **Backend Systems:** Design a sync protocol with conflict resolution, compare‑and‑swap semantics, and point‑in‑time snapshot restores.
- **Reliability & Observability:** Crash‑fault tolerance in the agent, graceful degradation, structured logging, and monitoring.

## Core Features (MVP)
1. **Cross‑Platform Agent (Rust)**
   - Real‑time file watching (inotify/FSEvents/ReadDirectoryChangesW).
   - Chunk‑based deduplication (content‑defined chunking, hash indexing).
   - Client‑side encryption (AES‑256‑GCM or ChaCha20‑Poly1305) before upload.
   - Fault‑tolerant: resumes interrupted backups, handles network loss.
2. **Coordination Server (Rust)**
   - Device registration and authentication (API keys or mTLS).
   - Version tree management for each file path.
   - Conflict detection and resolution (last‑write‑wins or interactive merge).
   - Snapshot creation and point‑in‑time restore.
3. **Cloud Storage Backend**
   - Primary: AWS S3 (or Backblaze B2 for cost efficiency).
   - Objects encrypted at rest (KMS) and optionally with Object Lock for immutability.
   - Lifecycle policies to transition old versions to cheaper tiers (Glacier).
   - Multipart uploads for large files.
4. **Web Dashboard**
   - View device status, recent backups, storage usage.
   - Browse file versions and trigger restores.
   - Simple shell script/CLI for command‑line restore.

## Tech Stack
### Agent (Rust)
- **Core libraries:** `notify` for file watching, `blake3` for hashing, `fastcdc` for chunking, `ring` or `aws-lc-rs` for encryption.
- **Networking:** `reqwest` (HTTP) + `tonic` (gRPC) for communication with the server.

### Coordination Server (Rust)
- **Framework:** Axum (async, high‑performance HTTP).
- **Database:** PostgreSQL (via `sqlx`) for metadata (file versions, snapshots, devices).
- **Authentication:** API keys stored hashed in DB, optional mTLS.
- **Blob Storage Abstraction:** Trait to support S3, B2, local disk.

### Cloud & Infrastructure
- **Object Storage:** AWS S3 with cross‑region replication (optional).
- **Compute:** AWS EC2 (single instance) or ECS Fargate for the coordination server.
- **Queue (Optional):** SQS for processing large sync jobs asynchronously.
- **IaC:** Terraform with modules for S3 buckets, IAM roles, KMS keys, EC2/ECS, and CloudWatch alarms.

### Local Development
- **LocalStack** to emulate S3 locally.
- Docker Compose with: coordination server, PostgreSQL, LocalStack.
- Agent runs natively on the host for real file system access.

## Architecture Diagram (Logical)
[Agent (Laptop)] [Agent (Desktop)]
│ │
▼ ▼
[Coordination Server (Rust/Axum)]
│
├────────[PostgreSQL] (metadata)
│
▼
[AWS S3 / Backblaze B2]
│
[Lifecycle → Glacier]


## Data Models (Key Entities)
- **Device:** id, name, platform, auth_key_hash, last_seen.
- **BackupObject:** hash, size, chunk_list, encryption_key_id.
- **FileVersion:** path, device_id, object_hash, timestamp, size, state (active, deleted).
- **Snapshot:** id, timestamp, set of FileVersion IDs, total_size.
- **Chunk:** chunk_hash, object_hash (the compressed/encrypted chunk stored in S3), offset.
- **User:** for dashboard access, JWT tokens.

## Implementation Phases
### Phase 1: Agent Skeleton & Local‑Only Backup (Weeks 1‑4)
- Implement file watcher and chunking engine (Rust).
- Compute content hashes, build local index (SQLite for speed).
- Encrypt chunks and store locally (simulate cloud target).
- Design CLI: `safesync init`, `safesync backup /path`.

### Phase 2: Coordination Server & Cloud Upload (Weeks 5‑8)
- Build Axum server with device registration and auth.
- Implement API to receive index metadata, allocate new objects.
- Integrate S3 upload directly from agent (pre‑signed URLs) or via server proxy.
- PostgreSQL schema and migrations (sqlx).
- Terraform: S3 bucket with versioning, encryption, lifecycle; IAM roles.

### Phase 3: Sync Protocol & Conflict Resolution (Weeks 9‑12)
- Define version tree logic: each file path has a history.
- On backup, agent sends delta (list of modified chunks + new file version info).
- Server detects conflicts (concurrent modifications from two devices), stores both.
- Implement simple restore API (download latest version or specific snapshot).
- Add snapshot creation and pruning.

### Phase 4: Dashboard & Hardening (Weeks 13‑16)
- Simple web UI (Vue/React) for status monitoring and restore operations.
- Automated recovery tests (restore random snapshots and verify integrity).
- Observability: structured logs, metrics (prometheus endpoint), alerting on failed backups.
- Hardening: handle edge cases (disk full, network timeouts, corrupted chunks).
- Write thorough documentation and a demo video.

## Gap‑Filling Deep Dives
### Rust Backend (Solidify)
- **Async Rust:** deep dive into Axum, Tokio, and SQLx.
- **Error Handling:** `thiserror`, `anyhow`, structured error responses.
- **Testing:** unit tests for chunking/crypto, integration tests with `reqwest` against a test server.

### Cloud Storage Infrastructure
- **Terraform Modules:** build reusable S3 module with versioning, encryption, lifecycle, object lock, public block.
- **IAM:** minimal‑privilege roles for agent upload, server operations, and dashboard access.
- **Cost Optimization:** lifecycle rules to move older versions to Standard‑IA or Glacier Deep Archive; set up billing alerts.

### Sync Protocol & Reliability
- **Deduplication efficiency:** measure reduction ratio over time.
- **Conflict scenarios:** simulate concurrent writes, verify resolution.
- **Recovery time objective (RTO):** benchmark restore from cloud to a clean directory.

## Non‑Goals (for this project)
- No Golang – Go is only for the Productivity App.
- No Python backend – Python lives in the Finance and Drone projects.
- No embedded real‑time – this is pure software infrastructure.

## Why I’ll Actually Use This
- Protects my personal projects, documents, and memories with encryption only I control.
- No monthly subscription for a backup service; I own the stack.
- Demonstrates exactly the backup/recovery domain expertise from my Ancient experience, but in my own open‑source portfolio.

---

**Author:** Diego Braga  
**Status:** Planning phase – to be built after VaultFolio reaches MVP.