# VaultFolio – Personal Finance & Investment Command Center

## Overview
A self‑hosted financial cockpit that aggregates bank transactions, tracks budgets, monitors investment portfolios, and runs advanced analytics—all on private infrastructure. The system is designed to replace dependence on third‑party apps like Mint or spreadsheets, while deliberately deepening my skills in **Python (FastAPI) as an orchestrator**, **Rust for performance‑critical compute**, **cloud‑native architecture**, **streaming data pipelines (Kafka/Redpanda)**, **Kubernetes operations**, and **distributed tracing (OpenTelemetry)**.

**Core principle:** local control with cloud mirroring; all sensitive financial data stays in my hands, with optional remote access and automated backups.

## Learning Objectives (Gaps Filled)
- **Python Backend (Solidification)**: Build a production‑grade FastAPI service with async workers, scheduled jobs, and a rule engine.
- **Rust Backend (Solidification)**: Implement a compute microservice (Axum) for heavy financial models (Monte Carlo, XIRR, portfolio rebalancing).
- **Backend Systems**: Event‑driven architecture, message brokers (Kafka/Redpanda, SQS), exactly‑once processing, schema registries.
- **Cloud Engineering**:
  - Advanced Terraform: multi‑service deployment, queues, object storage, IAM, monitoring.
  - AWS managed services: S3, EventBridge, DynamoDB, RDS (PostgreSQL), ElastiCache (Redis optional), MSK or self‑hosted Kafka.
  - **Kubernetes**: deploy the full stack on EKS with Helm, HPA, and pod disruption budgets.
- **Streaming & Messaging**: Deep dive into Kafka/Redpanda (partitions, consumers, offsets, schema evolution) and optionally SQS/FIFO.
- **Observability**: OpenTelemetry distributed tracing across Python → Kafka → Rust, metrics with Prometheus/Grafana.
- **Security**: OAuth2 integration with financial APIs, KMS encryption, threat‑modeling the data pipeline.

## Core Features (MVP)
1. **Bank Transaction Aggregation**
   - Connect to financial APIs (Plaid/Salt Edge or manual CSV import).
   - Periodic scheduled fetches (EventBridge + workers).
   - Automatic categorization with rule engine.
2. **Budgeting & Cash Flow**
   - Monthly budget targets per category.
   - Real‑time spending dashboards, alerts for overspending.
3. **Investment Portfolio Tracker**
   - Manual entries or API sync (stocks, crypto, funds).
   - Performance metrics: XIRR, time‑weighted returns, drawdowns.
   - What‑if scenarios (Monte Carlo simulation) using the Rust microservice.
4. **Custom Reporting**
   - Net worth over time, income vs expenses.
   - Tax‑relevant summaries.
5. **Savings Goals & Alerts**
   - Goal tracking with projected completion dates.
   - Alerts via email or push notification (SNS).

## Tech Stack
### Backend – Control Plane (Python)
- **Framework:** FastAPI (async) with Uvicorn.
- **Database Integration:** SQLAlchemy async + Alembic for migrations.
- **Scheduled Jobs:** Celery with Redis broker or APScheduler + custom worker processes.
- **Rule Engine:** Simple Python‑based rule matching for transaction categorization (configurable via YAML/DB).
- **API:** REST with OpenAPI auto‑generation.

### Backend – Compute Microservice (Rust)
- **Framework:** Axum (async Rust).
- **Mathematical Libraries:** `statrs` or `ndarray` for simulations, `rust_decimal` for precise money math.
- **Communication:** Protobuf/gRPC or REST endpoints called by the Python orchestrator.

### Messaging & Streaming
- **Primary:** Apache Kafka (or Redpanda) for transaction ingestion pipeline.
- **Alternative:** AWS SQS + SNS for simpler queuing of background jobs.
- **Local dev:** Redpanda container (single node) or Kafka in KRaft mode.

### Databases & Storage
- **Primary:** PostgreSQL (RDS) for structured data.
- **Cache:** Redis (ElastiCache) for rate limiting, session, or Celery task queue.
- **Time Series / Analytics:** Optional DuckDB for local analytics or parquet files on S3.
- **Object Storage:** AWS S3 for raw statement backups and parquet archives.

### Cloud & Infrastructure
- **Compute:** AWS ECS Fargate (or EC2) for API and workers; Lambda for lightweight triggers.
- **Kubernetes:** Primary deployment target on EKS (or local k3s) with Terraform Helm provider.
- **Orchestration:** Terraform for all resources (state in S3, DynamoDB lock).
- **CI/CD:** GitHub Actions → Docker build → ECR → deploy to ECS/K8s.
- **Monitoring:** OpenTelemetry tracing (OTLP) → Honeycomb/Jaeger; Prometheus metrics, CloudWatch Logs.

### Local Development
- Docker Compose with: Python API, Rust worker, Redpanda, PostgreSQL, Redis.
- `docker-compose up` gives a fully functional local system.

## Architecture Diagram (Logical)
[Web Dashboard (React/Vue)]
│
▼
[FastAPI API]───────────[Redis Cache]
│
┌────┴─────────────┐
[PostgreSQL] [Kafka/Redpanda]
│
┌───┴────┐
[Python Consumer] [Rust Compute Worker]
│ │
[Processes txn] [Monte Carlo, XIRR]
│ │
[Writes to DB] [Returns via gRPC]
(all services report OTel traces)


## Data Models (Key Entities)
- **Account**: bank name, type (checking, savings, credit, investment).
- **Transaction**: date, amount, description, category, account_id, raw_data.
- **Category**: name, parent, rule_set.
- **Budget**: category_id, month, amount.
- **InvestmentHolding**: ticker, shares, cost_basis.
- **PortfolioSnapshot**: date, total_value, breakdown.
- **Goal**: name, target_amount, deadline, current_amount.
- **Rule**: for categorization (e.g., if description contains "AMAZON" → Shopping).

## Implementation Phases
### Phase 1: Core Infrastructure & Data Ingestion (Weeks 1‑4)
- Scaffold Python FastAPI project with clean architecture.
- Set up PostgreSQL schema, run migrations (Alembic).
- Build manual transaction CRUD + CSV import endpoint.
- Implement basic bank‑API integration (Plaid sandbox).
- Deploy a single EC2/ECS service via Terraform.
- CI pipeline (lint, test, build, deploy).

### Phase 2: Streaming Pipeline & Categorization (Weeks 5‑8)
- Introduce Redpanda/Kafka: publish raw transactions to a topic.
- Build Python consumer that categorizes and persists.
- Implement rule engine with configurable rules.
- Deploy Redpanda cluster (or AWS MSK Serverless) via Terraform.
- Add dead‑letter queues and retry logic.

### Phase 3: Budgets, Reporting, Rust Compute (Weeks 9‑12)
- Budget module: set targets, view spending over time.
- Investment tracker: manual holdings, regular valuation updates.
- Build Rust microservice for XIRR and Monte Carlo simulation.
- Expose gRPC endpoint; Python API calls it for portfolio analysis.
- Dockerize and add to Terraform deployment.

### Phase 4: Frontend & Advanced Features (Weeks 13‑16)
- Build web dashboard (React/Vue) consuming the API.
- Add alerts and notifications (SNS/SES).
- Auto‑fetch from institutions on schedule using EventBridge.
- Optional: DynamoDB for user preferences.

### Phase 5: Kubernetes & Observability (Weeks 17‑20)
- Migrate deployment to Kubernetes (EKS). Create Helm charts for API, workers, Kafka consumers.
- Configure HPA for the Rust compute worker based on queue depth.
- Add OpenTelemetry auto‑instrumentation to Python and manual instrumentation to Rust.
- Deploy Jaeger or sign up for Grafana Cloud; visualize traces across message boundaries.
- Set up Prometheus/Grafana for custom business metrics.

### Phase 6: Security Hardening & Advanced Features
- Implement OAuth2 flow for financial data providers.
- Use KMS for field‑level encryption of sensitive data in DB.
- Conduct a threat model exercise and document it in the repo.
- (Optional) Replace local SQLite analytics with an embedded Rust KV store for high‑frequency portfolio snapshots.

## Gap‑Filling Deep Dives
### Python Backend (Solidify)
- **Async patterns:** efficient I/O for multiple bank providers concurrently.
- **Testing:** `pytest`, `httpx` for API tests, `testcontainers` for integration with Kafka/DB.
- **Observability:** OpenTelemetry propagation, custom spans, trace‑aware logging.

### Rust Backend (Solidify)
- **Performance:** memory‑safe simulation of thousands of Monte Carlo iterations.
- **gRPC:** use `tonic` to define service and handle message serialization.
- **Interoperability:** decoupled service that can be scaled independently (K8s HPA).

### Kafka/Streaming
- **Partitioning strategy:** by account_id for ordered transaction events.
- **Consumer groups:** separate ingestion from analytics.
- **Schema Registry:** optional Avro schema for events.
- **Offset management:** handle reprocessing and consumer failures.
- **Comparison:** optionally also implement a SQS version to compare trade‑offs.

### Kubernetes (New Gap)
- **Helm charts:** packaging the whole application.
- **Health probes:** liveness/readiness checks, graceful shutdown.
- **HPA:** scale Rust workers based on Kafka consumer lag.
- **Pod disruption budgets:** ensure zero‑downtime deployments.

### Advanced Cloud
- **Terraform modules:** reusable modules for Kafka cluster, RDS, ECS.
- **Security:** IAM roles for service ecsTaskRole, KMS for sensitive data.
- **Cost management:** set up AWS Budget alerts; design architecture to stay within free tier for low traffic.

## Non‑Goals (for this project)
- No embedded or real‑time hardware.
- No Golang – Go is solely for the Productivity App.
- No file sync/backup logic – that’s the SafeSync project.

## Why I’ll Actually Use This
- Complete control over my financial data, no sharing with third‑party aggregators.
- Custom reports and alerts that match my exact needs.
- A permanent lab for exploring streaming, distributed systems, Kubernetes, and analytics.
- Saves money on premium finance apps while teaching skills that directly boost my career.

---

**Author:** Diego Braga  
**Status:** Planning phase – ready to start after FocusFlow core is stable.