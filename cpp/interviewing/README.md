# C++ Interviewing

Self-contained interview-prep hub for **senior C++ / systems / backend** roles.
Everything needed for the C++ track lives in this folder.

**Sources:** two prep PDFs — *C++ and Rust Coding Interview Exercises* (prioritised
practice guide) and *Senior Engineer Interview Preparation* (Topics 3, 4, 7).

## Files

| File | Contents |
|------|----------|
| [`exercises.md`](exercises.md) | Merged, prioritised C++ exercise catalogue (core systems, language drills, algorithms) with API sketches. |
| [`practice_plan.md`](practice_plan.md) | The day-by-day 30-day preparation plan (Weeks 1–4). |
| [`resume_deep_dives.md`](resume_deep_dives.md) | Resume anchors + the repeatable project-story structure. |
| [`readiness_scorecard.md`](readiness_scorecard.md) | Readiness checklist and status interpretation. |

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

## Exercise → existing C++ code

[`exercises.md`](exercises.md) links each exercise to the closest existing material:

| Area | Where it lives |
|------|----------------|
| Ownership, smart pointers, RAII | [`Refreshers/13_smart_pointers.cpp`](../Refreshers/13_smart_pointers.cpp), [`Examples/ptr_wrapper.cpp`](../Examples/ptr_wrapper.cpp) |
| Move semantics, value categories | [`Refreshers/09_move_and_copyelision.cpp`](../Refreshers/09_move_and_copyelision.cpp), [`Refreshers/07_value_categories.cpp`](../Refreshers/07_value_categories.cpp) |
| Threads, concurrency, atomics | [`Refreshers/14_threads.cpp`](../Refreshers/14_threads.cpp), [`Refreshers/31_advanced_concurrency.cpp`](../Refreshers/31_advanced_concurrency.cpp) |
| Thread pool / queues | [`Examples/thread_pool.cpp`](../Examples/thread_pool.cpp), [`Examples/thread_queue.cpp`](../Examples/thread_queue.cpp) |
| Allocators & memory | [`Refreshers/33_allocators_memory.cpp`](../Refreshers/33_allocators_memory.cpp) |
| Templates, type traits, SFINAE | [`Refreshers/23_advanced_templates.cpp`](../Refreshers/23_advanced_templates.cpp), [`Examples/template_sfinae.cpp`](../Examples/template_sfinae.cpp) |
| Parsing, protocols, IPC | [`Examples/bin_parser.cpp`](../Examples/bin_parser.cpp), [`Examples/packet_receiver.cpp`](../Examples/packet_receiver.cpp) |
| Patterns (observer, factory, plugin) | [`Examples/observer.cpp`](../Examples/observer.cpp), [`Refreshers/26_design_patterns.cpp`](../Refreshers/26_design_patterns.cpp) |
| SOLID / refactoring | [`Refreshers/18_solid.cpp`](../Refreshers/18_solid.cpp) |
| Algorithms practice | [`../Algorithms/`](../Algorithms/README.md) |
