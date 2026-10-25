title:: Garbage Collectors: Reference Counting (Python) vs Tracing (Go)
type:: article
state:: collected
ingested:: [[2026-10-25]]
note:: Python uses counting based, Go uses tracing based. How do you handle cycles etc?
domain:: [[Programming/Compilers]]
topic:: [[Language Implementation]]
complexity:: intermediate
size:: medium
concepts:: [[Garbage Collection]], [[Reference Counting]], [[Tracing Garbage Collection]], [[Cycle Detection]], [[Memory Management Concepts]]
prerequisites:: [[Memory Management Concepts]], [[Data Structures]]

## Summary
A study topic rather than a single source: compare the two main garbage-collection families. CPython frees most objects by reference counting the moment their count hits zero, and adds a generational cycle detector to reclaim reference cycles that counting alone can never free (CPython dev guide: https://devguide.python.org/internals/garbage-collector/). Go uses a concurrent, non-moving, tri-colour mark-and-sweep tracing collector with write barriers, tuned by GOGC and GOMEMLIMIT ('A Guide to the Go Garbage Collector': https://go.dev/doc/gc-guide); tracing handles cycles naturally because it only keeps what is reachable from roots.

## Key Takeaways
- Reference counting is prompt and incremental but costs on every pointer write and cannot free cycles by itself
- CPython's cycle collector finds unreachable cycles by subtracting references internal to container objects
- Tracing GC (mark from roots) handles cycles for free but needs pauses or concurrent marking with write barriers
- Go trades memory headroom for CPU via GOGC; GOMEMLIMIT caps the total heap

## Learnings
- 2026-10-25 · CPython picked reference counting in 1991 because it is simple, frees memory the moment the count hits 0 (files close immediately), keeps the C API to Py_INCREF/Py_DECREF, and avoids long pauses; Java, Go and JS use tracing collectors instead, and CPython still needs a separate cycle collector.
