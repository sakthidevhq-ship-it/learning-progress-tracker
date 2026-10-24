title:: Async Python internals: the event loop
type:: article
state:: picked
ingested:: [[2026-10-03]]
domain:: [[Programming/Python]]
topic:: [[Concurrency]]
complexity:: intermediate
size:: medium
concepts:: [[Python]], [[Concurrency Basics]]
prerequisites:: [[Python]]
picked:: [[2026-10-03]]
planned:: 2026-10

## Summary
How asyncio works underneath: coroutines as generators, the event loop's ready queue and selector, futures and tasks, and how await hands control back to the loop.

## Checklist
- [ ] Write a generator-based round-robin scheduler (no asyncio)
- [ ] Add sleep() and non-blocking sockets with selectors; serve many echo clients
- [ ] Implement a minimal Future with __await__ and done callbacks
- [ ] Trace one iteration of asyncio's BaseEventLoop._run_once
- [ ] Block the loop with a sync call, measure loop lag, fix with asyncio.to_thread
- [ ] Benchmark the echo server: asyncio vs uvloop
