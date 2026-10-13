# Rust Interviewing

Self-contained interview-prep hub for **senior Rust / backend** roles. Everything for the
Rust track lives in this folder, alongside the exercise crates.

**Sources:** *C++ and Rust Coding Interview Exercises* (§1 core, §3 Rust drills, §4 order)
and the original `ideas.txt` (40 senior-scoped Rust challenges).

## Files

| File | Contents |
|------|----------|
| [`exercises.md`](exercises.md) | Merged, prioritised Rust exercise catalogue (core systems, language & async drills, algorithms) with API sketches. |
| [`practice_plan.md`](practice_plan.md) | The day-by-day 30-day preparation plan (Weeks 1–4). |
| [`resume_deep_dives.md`](resume_deep_dives.md) | Resume anchors + the repeatable project-story structure. |
| [`readiness_scorecard.md`](readiness_scorecard.md) | Readiness checklist and status interpretation. |

## Exercise crates in this folder

Several catalogue exercises already exist here as runnable crates:

| Exercise | Crate |
|----------|-------|
| LRU cache | [`mini_lru`](mini_lru) |
| Token bucket rate limiter | [`rate_limiter`](rate_limiter) |
| Thread pool | [`mini_thread_pool`](mini_thread_pool) |
| TTL key-value store | [`inmem_kv_store`](inmem_kv_store) |
| Streaming median | [`stream_median`](stream_median) |
| Custom iterator | [`custom_iter`](custom_iter) |
| Binary search tree | [`bin_search_tree`](bin_search_tree) |
| Domain type via `TryFrom` | [`tryfrom`](tryfrom) |
| Config loader | [`config_loader`](config_loader) |
| Thread-safe counter | [`threadsafe_counter`](threadsafe_counter) |
| Simple logger | [`simple_logger`](simple_logger) |
| HTTP router (Axum / Actix) | [`simple_router_axum`](simple_router_axum), [`simple_router_actix`](simple_router_actix) |
| Warm-ups | [`two_sum`](two_sum), [`fizzbuzz`](fizzbuzz), [`fibonacci`](fibonacci), [`palindrome_check`](palindrome_check), [`prime_check`](prime_check), [`reverse_string`](reverse_string), [`max_val`](max_val), [`vowel_counter`](vowel_counter), [`hello_rust`](hello_rust) |

Larger reference projects live in [`../Projects/`](../Projects) (`jwt-auth`, `axum-webserver`,
`taskflow`, `kafka-event-processor`, `rust-payment-engine`) and refreshers in
[`../Refreshers/`](../Refreshers).

## How to use

- Start with [`exercises.md`](exercises.md) §D ("Suggested first pass"), then work §A/B/C by priority.
- Follow [`practice_plan.md`](practice_plan.md) as a sequence, but adjust based on mock-interview results.
- Treat each deliverable as **evidence of readiness** — not merely time spent studying.
- For project stories, distinguish your personal contribution from team outcomes and
  **never invent metrics or implementation details**.

## Priority legend

| Priority | Meaning |
|----------|---------|
| **P0** | Practice first — highest signal for senior loops. |
| **P1** | Important next. |
| **P2** | Specialized / advanced. |
| **P3** | Defer unless the target role demands it. |
