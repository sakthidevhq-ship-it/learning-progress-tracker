title:: The Python GIL
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
my-priority:: now

## Summary
What the Global Interpreter Lock protects, how CPython hands it between threads, why it limits CPU-bound threading, and where free-threaded (no-GIL) CPython stands.

## Checklist
- [ ] Why was it created?
- [ ] What do other language like Go use as alternatives?
- [ ] Re-implement?
- [ ] How to circumvent the downsides of GIL in python
- [ ] Upsides of GIL?
- [ ] subinterpreters
- [ ] What have people done in 3.14 on this

## Time
- 2026-10-04 · 30m
- 2026-10-25 · 30m

## Notes
Learnt what Cpython does. How it differs from JIT and complier. 
Where GIL prevents. 
