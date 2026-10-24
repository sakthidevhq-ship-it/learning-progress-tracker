title:: How Go implements async: goroutines and the scheduler
type:: article
state:: picked
ingested:: [[2026-10-03]]
note:: Compare with Python's event loop and GIL.
domain:: [[Systems]]
topic:: [[Concurrency]]
complexity:: intermediate
size:: medium
concepts:: [[Concurrency Basics]]
prerequisites:: [[Concurrency Basics]]
picked:: [[2026-10-03]]
planned:: 2026-10

## Summary
Go's answer to async: cheap goroutines on a work-stealing M:N scheduler (G, M, P), the netpoller that turns blocking I/O into parking, and channels. No async/await colouring.

## Checklist
- [ ] Start 100k goroutines vs 100k asyncio tasks vs threads: compare memory and startup time
- [ ] Read the G/M/P overview in runtime/proc.go and draw it
- [ ] Run a CPU-bound program with GODEBUG=schedtrace=1000 and watch work stealing
- [ ] TCP echo server: see the netpoller park goroutines in go tool trace
- [ ] Worker pool and pipeline with channels, select and context cancellation
- [ ] One-page comparison: Go scheduler vs asyncio vs the GIL
