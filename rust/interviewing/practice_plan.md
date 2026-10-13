# The Day-by-Day Plan (30 Days)

Source: *Senior Engineer Interview Preparation* (Topics 3, 4, and 7), §3.

**Target:** Senior software engineering roles across systems, backend, and general
software engineering. **Market:** Remote international companies.

> Adjust the sequence based on your mock-interview results. Each *Deliverable* is
> evidence of readiness — not merely time spent studying.

---

## Week 1 — Reactivate your technical skills

### Day 1 — Baseline assessment + career inventory
- Solve one medium algorithm problem in 40 minutes using your preferred interview language.
- Implement a small function in idiomatic modern C++ or Rust, with tests.
- Record friction points: decomposition, syntax, speed, debugging, or explaining reasoning.
- Select six projects or achievements for interview preparation.

**Deliverable:** Three weakest areas and six candidate interview stories.

### Day 2 — Modern C++ refresher
- Review value categories, references, move semantics, forwarding, RAII, object lifetimes, smart pointers, exception safety, templates, concepts, type deduction, and STL containers.
- Implement an LRU cache or a small ownership-sensitive data structure.

**Deliverable:** Working code, tests, and a verbal explanation of ownership and complexity.

### Day 3 — Rust refresher
- Review ownership, borrowing, lifetimes, trait bounds, generics, Send/Sync, Arc, Mutex, RwLock, error handling, async/await, futures, trait objects, and interior mutability.
- Work through three compiler exercises involving borrowing, lifetimes, or concurrency.

**Deliverable:** Explain why three snippets compile or fail, and fix them.

### Day 4 — Algorithms I: core data structures
- Practice arrays, strings, hash maps, sets, two pointers, and sliding windows.
- Solve two medium problems under time limits; explain complexity before coding.
- Test empty input, duplicates, and boundary conditions.

**Deliverable:** Two tested solutions with clear complexity analysis.

### Day 5 — Linux, memory, and debugging
- Review virtual memory, stack vs. heap, page faults, caches, file descriptors, processes, threads, syscalls, and memory mapping.
- Practice investigating a hypothetical memory leak or unexpected CPU spike.
- Review sanitizers, debuggers, profilers, and crash dumps.

**Deliverable:** A structured investigation checklist for production performance issues.

### Day 6 — Career narrative + first mock
- Prepare a 90-second introduction and explain your contracting period and full-time goals.
- Rehearse one Axcient project and one recent contract project.
- Complete a 45-minute coding mock and review the result.

**Deliverable:** Concise introduction and two project explanations.

### Day 7 — Recovery and review
- Review errors from the first six days and revisit the two weakest technical topics.
- Keep the day light; avoid adding a large new topic.

**Deliverable:** Updated weakness list and next-week priorities.

---

## Week 2 — Systems depth and production engineering

### Day 8 — Concurrency fundamentals
- Review mutexes, condition variables, atomics, memory ordering, deadlocks, race conditions, and false sharing.
- Implement a thread-safe bounded queue in C++ or Rust.

**Deliverable:** Implementation, tests, and explanation of synchronization guarantees.

### Day 9 — Async programming and network services
- Compare threads, event loops, async tasks, and worker pools.
- Review cancellation, timeouts, backpressure, and resource limits.
- Design a concurrent job-processing service and define its overload behavior.

**Deliverable:** Concurrency model with explicit failure and overload handling.

### Day 10 — Networking and secure communication
- Review TCP/UDP, TLS, connection pooling, gRPC, Protobuf, retries, idempotency, and timeouts.
- Connect these topics to Axcient RPC/security work and your C++ monitoring platform.

**Deliverable:** Explain an RPC request end-to-end, including failures and security.

### Day 11 — Storage, indexing, and performance
- Review caching, indexes, lookup complexity, I/O bottlenecks, memory allocation, profiling, and benchmark methodology.
- Reconstruct the Axcient recovery-time improvement: baseline, change, measurement, and tradeoffs.

**Deliverable:** A 10–15 minute technical deep dive into the reported recovery-time reduction.

### Day 12 — Reliability and incident response
- Practice investigating failing backups, intermittent service failures, and missing telemetry.
- Cover reproduction, logs, metrics, tracing, root cause, mitigation, and regression tests.

**Deliverable:** Incident postmortem outline tied to your reliability experience.

### Day 13 — Algorithms II: trees and graphs
- Practice BFS, DFS, binary search, heaps, and interval problems.
- Solve two timed problems and explain tradeoffs aloud.

**Deliverable:** Two tested solutions without relying on memorized templates.

### Day 14 — Technical mock interview
- Run a 60-minute session: 35 minutes coding, 15 minutes technical follow-ups, and 10 minutes feedback.

**Deliverable:** Three specific changes for the following week.

---

## Week 3 — Backend design and interview execution

### Day 15 — System design I: event-driven job processing
- Design a job-processing platform with queues, retries, dead-letter queues, idempotency, circuit breakers, and observability.
- Draw on your FastAPI/Celery contract work.

**Deliverable:** Architecture diagram and discussion of failure modes.

### Day 16 — System design II: high-throughput ingestion
- Design a service that validates, processes, and stores data asynchronously.
- Cover Kafka/RabbitMQ, partitioning, ordering, delivery guarantees, and backpressure.

**Deliverable:** Design that handles traffic spikes and partial failures.

### Day 17 — System design III: distributed monitoring
- Design monitoring agents, ingestion, time-series storage, alerting, authentication, and Linux/Windows deployment.
- Justify component choices, scalability, and security tradeoffs.

**Deliverable:** End-to-end design with failure and security considerations.

### Day 18 — Algorithms III: harder patterns
- Practice dynamic programming, heaps, graph traversal, and multi-structure problems.
- Substitute a weak topic from Week 1 if these are already strong.

**Deliverable:** Two timed problems and an error analysis.

### Day 19 — Resume deep dive: Axcient
- Rehearse the backup agent, storage/cache optimization, cross-platform reliability, and production debugging.
- For each, explain baseline, personal contribution, alternatives, validation, tradeoffs, and results.

**Deliverable:** Three project narratives with anticipated follow-up questions.

### Day 20 — Behavioral and leadership interview
- Prepare stories about technical disagreement, an incident, ambiguous requirements, mentoring, a failed approach, and a difficult tradeoff.

**Deliverable:** Six concise STAR-style stories with clear personal contribution and outcomes.

### Day 21 — Full mock: coding + system design
- Simulate two interview rounds with a break between them.
- Review clarity, pacing, assumptions, testing, and response to hints.

**Deliverable:** Ranked list of the five most important remaining weaknesses.

---

## Week 4 — Interview readiness and applications

### Day 22 — Fix the biggest technical weakness
- Choose one topic based on mock results rather than preference.
- Retest the original problem after focused review.

**Deliverable:** Evidence that the original weakness has improved.

### Day 23 — Modern language and tooling updates
- Review relevant C++20/23 and Rust ecosystem developments, Cargo/CMake, testing, sanitizers, profiling, and build tooling.
- Focus on job-relevant changes, not exhaustive release notes.

**Deliverable:** Explain five modern practices and when to use them.

### Day 24 — General backend interview
- Practice API design, SQL/indexing, transactions, caching, queues, REST vs. gRPC, authentication, and observability.

**Deliverable:** A 45-minute backend design or debugging session.

### Day 25 — Remote international interview preparation
- Practice concise English technical communication.
- Prepare availability, time zone, notice period, and preferred employment/contract arrangement.
- Prepare questions about team structure, on-call, ownership, and interview stages.
- Shortlist roles and tailor your resume where needed.

**Deliverable:** Recruiter-screen script and target-job shortlist.

### Day 26 — Mock coding interview
- Complete a realistic 45–60-minute coding session.
- Speak while solving, test edge cases, and finish with complexity analysis.

**Deliverable:** Complete solution within the time limit, with no major untested assumptions.

### Day 27 — Mock system design + project deep dive
- Design a system, defend the architecture, then answer follow-up questions about an actual project.

**Deliverable:** Move confidently between high-level architecture and implementation detail.

### Day 28 — Full interview loop
- Simulate coding, systems, system design, and behavioral rounds with realistic breaks.
- If possible, have another engineer act as interviewer.

**Deliverable:** Final scorecard and last-mile improvements.

### Day 29 — Targeted review + applications
- Review mistakes, refine project stories, and apply to selected roles.
- Start recruiter conversations rather than waiting for perfect readiness.

**Deliverable:** Final review sheet and active applications.

### Day 30 — Readiness check + sustainable routine
- Do a light coding warm-up, review your introduction and project stories, and check your application pipeline.
- Avoid cramming a new advanced topic.

**Deliverable:** Readiness assessment and a sustainable ongoing routine.
