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
- [x] Why was it created?
- [ ] What do other language like Go use as alternatives?
- [ ] Re-implement?
- [x] How to circumvent the downsides of GIL in python
- [x] Upsides of GIL?
- [x] subinterpreters
- [x] What have people done in 3.14 on this
- [ ] Python JIT (pypy).
- [ ] Hypervisor, VMs, Emulators
- [ ] Garbage collector

## Time
- 2026-10-04 · 30m
- 2026-10-25 · 2h

## Notes
Learnt what Cpython does. How it differs from JIT and complier. 
Where GIL prevents. 

## Learnings
- 2026-10-25 · CPython never turns my code into machine code: it compiles each file to bytecode before running (imports get cached as .pyc) and a precompiled C loop in ceval.c acts out each instruction. A JIT like PyPy also interprets at first, but compiles hot loops to machine code once and then runs that directly.
- 2026-10-25 · Every Python object keeps its refcount (ob_refcnt) on the shared heap, and even x = my_list writes to it, so two threads incrementing it without a lock can lose an update and free a live object. The GIL's upside is one rarely-taken lock instead of a lock or atomic op on every object, which keeps single-threaded code fast.
- 2026-10-25 · The GIL switches threads between bytecodes, so stats.count += 1 (several bytecodes) can still lose updates across threads and needs a threading.Lock; asyncio only switches at await, so the same line is safe there.
- 2026-10-25 · Subinterpreters are several interpreters inside one process, each with its own GIL and objects, on separate OS threads: isolated, parallel only if there are free cores, and they talk by message passing (queues, memoryview buffers) rather than shared references. They're basically cheaper processes; on my 1-vCPU voice worker they wouldn't cut jitter, and on multi-core gunicorn processes stay the better default.
- 2026-10-25 · Python 3.14 made the free-threaded build (python3.14t, no GIL) officially supported, and its single-threaded cost dropped from ~40% in 3.13t to ~5-10% because the specialising interpreter was made thread-safe again. That's the pick when I need shared memory plus real parallelism, Go-style, as long as my C extensions support it.
