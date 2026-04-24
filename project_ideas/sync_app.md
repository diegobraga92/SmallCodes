# SafeSync – Personal Backup & Sync Agent

## Overview
A cross‑platform (Linux, macOS, Windows) backup agent and coordination server that provides deduplicated, encrypted, versioned backups of my most important files to cloud object storage. The system is designed to replace commercial backup tools, giving me full control over data security and retention policies while serving as a deep learning sandbox for **Rust backend engineering**, **advanced cloud storage infrastructure (Terraform)**, **distributed consensus (Raft)**, **Kubernetes operators**, and **security engineering (mTLS, remote attestation)**.

**Core principle:** local agent syncs changes to a Rust coordination server, which handles versioning, conflict resolution, and secure cloud uploads. The server can be deployed as a highly‑available cluster using Raft. A Kubernetes operator (Go) will be built to manage backup schedules for containerised workloads.

## Learning Objectives (Gaps Filled)
- **Rust Backend (Solidification):** Build a highly‑available coordination server in Rust (Axum) that manages device authentication, sync state, version history, and restore APIs. Evolve it into a clustered, consensus‑driven service.
- **Cloud Engineering (Deep Dive):** 
  - Terraform for object storage infrastructure (S3/Backblaze B2), IAM, KMS encryption, lifecycle policies, cost alerting.
  - Cloud‑native storage patterns: versioning, object locking, replication, multipart uploads.
- **Backend Systems:** Design a sync protocol with conflict resolution, compare‑and‑swap semantics, and point‑in‑time snapshot restores.
- **Distributed Consensus:** Implement Raft consensus within the coordination server, enabling leader election and log replication for high availability.
- **Kubernetes Operator (Golang):** Build an operator that schedules SafeSync backups for PersistentVolumeClaims in a K8s cluster.
- **Security:** Mutual TLS (mTLS) between agents and server, remote attestation of agent integrity, KMS‑based encryption.
- **Reliability & Observability:** Crash‑fault tolerance in the agent, graceful degradation, structured logging, and monitoring.

## Core Features (MVP)
1. **Cross‑Platform Agent (Rust)**
   - Real‑time file watching (inotify/FSEvents/ReadDirectoryChangesW).
   - Chunk‑based deduplication (content‑defined chunking, hash indexing).
   - Client‑side encryption (AES‑256‑GCM or ChaCha20‑Poly1305) before upload.
   - Fault‑tolerant: resumes interrupted backups, handles network loss.
2. **Coordination Server (Rust)**
   - Device registration and authentication (API keys initially, then mTLS).
   - Version tree management for each file path.
   - Conflict detection and resolution (last‑write‑wins or interactive merge).
   - Snapshot creation and point‑in‑time restore.
   - **Cluster mode:** Raft consensus for HA, leader handles writes, followers serve reads.
3. **Cloud Storage Backend**
   - Primary: AWS S3 (or Backblaze B2 for cost efficiency).
   - Objects encrypted at rest (KMS) and optionally with Object Lock for immutability.
   - Lifecycle policies to transition old versions to cheaper tiers (Glacier).
   - Multipart uploads for large files.
4. **Web Dashboard**
   - View device status, recent backups, storage usage.
   - Browse file versions and trigger restores.
   - Simple shell script/CLI for command‑line restore.
5. **Kubernetes Operator (Go)**
   - Custom Resource `BackupSchedule`: target PVC, schedule, retention.
   - Operator creates a sidecar agent that syncs data to SafeSync server.

## Tech Stack
### Agent (Rust)
- **Core libraries:** `notify` for file watching, `blake3` for hashing, `fastcdc` for chunking, `ring` or `aws-lc-rs` for encryption.
- **Networking:** `reqwest` (HTTP) + `tonic` (gRPC) for communication with the server.

### Coordination Server (Rust)
- **Framework:** Axum (async, high‑performance HTTP).
- **Database:** PostgreSQL (via `sqlx`) for metadata, or an **embedded KV store** (e.g., a custom LSM‑tree in Rust) for version metadata – a stretch goal to deepen DB internals.
- **Consensus:** `raft-rs` (with etcd’s Raft implementation or `openraft`) for clustering.
- **Authentication:** API keys initially, then upgraded to mTLS using `rustls`.
- **Blob Storage Abstraction:** Trait to support S3, B2, local disk.

### Cloud & Infrastructure
- **Object Storage:** AWS S3 with cross‑region replication (optional).
- **Compute:** AWS EC2 (single instance initially, then a small cluster) or ECS Fargate.
- **Kubernetes Operator:** Written in **Go** using `controller-runtime` and `client-go`.
- **IaC:** Terraform with modules for S3 buckets, IAM roles, KMS keys, EC2/ECS, and CloudWatch alarms.

### Local Development
- **LocalStack** to emulate S3 locally.
- Docker Compose with: coordination server, PostgreSQL, LocalStack.
- Agent runs natively on the host for real file system access.

## Architecture Diagram (Logical)
[Agent (Laptop)] [Agent (Desktop)]
│ (mTLS) │ (mTLS)
▼ ▼
[SafeSync Cluster (Raft)]
│
├────────[PostgreSQL / KV store] (metadata)
│
▼
[AWS S3 / Backblaze B2]
│
[Lifecycle → Glacier]


## Data Models (Key Entities)
- **Device:** id, name, platform, certificate_fingerprint, last_seen.
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

### Phase 5: High Availability with Raft (Weeks 17‑20)
- Add `raft-rs` to the coordination server. Bootstrap a 3‑node cluster.
- Metadata writes (new file versions) go through Raft log; reads can be eventually consistent.
- Leader failover testing, network partition tests.
- This directly demonstrates distributed consensus experience.

### Phase 6: Kubernetes Operator (Weeks 21‑24)
- Write a Go operator using `kubebuilder` that watches `BackupSchedule` CRDs.
- For each schedule, it creates a sidecar container running SafeSync agent that backs up the PVC.
- Register backups in the coordination server and show status in the dashboard.

### Phase 7: Advanced Security (ongoing)
- Migrate from API keys to mTLS for agent‑server communication.
- Implement a simple remote attestation mechanism (agent sends hash of its binary; server verifies).
- Encrypt metadata at rest using KMS.

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

### Distributed Consensus (New Gap)
- **Raft implementation:** log replication, snapshots, cluster membership changes.
- **Testing consensus:** chaos engineering – kill nodes, partition network, verify safety.
- **Trade‑offs:** when to use leader‑based vs leaderless designs.

### Kubernetes Operator (New Gap)
- **Go client-go:** interacting with the Kubernetes API.
- **Controller pattern:** reconciling desired state with actual.
- **Operator SDK:** kubebuilder to scaffold and manage CRDs.

### Security Engineering
- **mTLS:** certificate provisioning and rotation.
- **Remote attestation:** ensuring agent binaries haven’t been tampered.
- **KMS integration:** envelope encryption for chunks.

## Non‑Goals (for this project)
- No Golang – Go is solely for the Productivity App, except for the K8s operator (which is a deliberate small Go component).
- No Python backend – Python lives in the Finance and Drone projects.
- No embedded real‑time – this is pure software infrastructure.

## Why I’ll Actually Use This
- Protects my personal projects, documents, and memories with encryption only I control.
- No monthly subscription for a backup service; I own the stack.
- Demonstrates exactly the backup/recovery domain expertise from my Ancient experience, but in my own open‑source portfolio.
- The Raft cluster and Kubernetes operator make it a standout project for senior systems/infrastructure roles.

---

**Author:** Diego Braga  
**Status:** Planning phase – to be built after VaultFolio MVP.