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
