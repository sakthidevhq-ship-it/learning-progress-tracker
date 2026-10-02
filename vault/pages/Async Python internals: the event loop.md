title:: Async Python internals: the event loop
type:: article
state:: collected
ingested:: [[2026-10-03]]
domain:: [[Programming/Python]]
topic:: [[Concurrency]]
complexity:: intermediate
size:: medium
concepts:: [[Python]], [[Concurrency Basics]]
prerequisites:: [[Python]]

## Summary
How asyncio works underneath: coroutines as generators, the event loop's ready queue and selector, futures and tasks, and how await hands control back to the loop.
