title:: Before GPU Engineering
type:: article
state:: picked
source:: https://before-gpu-engineering.github.io/BEFORE-GPU-ENGINEERING/toc.html
ingested:: [[2026-11-17]]
note:: GPU hardware reasoning before writing kernels: architecture, memory, warps/SIMT, occupancy, then CUDA, coalescing, tiling and profiling (56 chapters in 4 phases)
domain:: [[ML/Infrastructure]]
topic:: [[GPU Kernels]]
complexity:: intermediate
size:: deep-dive
concepts:: [[GPU Computing Basics]], [[GPU Memory Bandwidth]], [[GPU Memory Hierarchy]], [[Arithmetic Intensity]], [[SIMT and Warps]], [[Occupancy]], [[Memory Coalescing]], [[Performance Profiling]]
prerequisites:: [[C Basics]], [[Memory Management Concepts]], [[Concurrency Basics]]
picked:: [[2026-11-17]]
planned:: 2026-11

## Summary
A free online book in 56 short chapters that explains why GPUs are built the way they are before you write kernels. Phase 1 covers architecture, memory bandwidth, warps, SIMT and occupancy. Phase 2 covers CUDA's model (kernels, blocks, shared memory, syncthreads, async launches). Phases 3-4 cover the memory wall, register pressure and spilling, coalescing, tiling, GEMM and Nsight profiling.

## Key Takeaways
- GPUs trade per-thread latency for throughput: thousands of simple cores, latency hidden by switching warps
- Most kernels are memory-bound; arithmetic intensity decides which roofline ceiling you hit
- Warps execute in lockstep (SIMT), so branch divergence and uncoalesced access waste lanes and transactions
- Occupancy is a ratio and not the goal; register pressure and spilling can dominate
- Measure with Nsight Systems/Compute before optimizing

## Checklist
- [x] Phase 1 · Part 1: The Architecture (ch 1–3)
- [x] Phase 1 · Part 2: Feeding the Beast (ch 4–6)
- [ ] Phase 1 · Part 3: Inside the Silicon (ch 7–10)
- [ ] Phase 1 · Part 4: Putting it Together (ch 11–15)
- [ ] Phase 2 · The Translation Barrier (ch 16–18)
- [ ] Phase 2 · The Hardware Hierarchy (ch 19–22)
- [ ] Phase 2 · Synchronization & Hazards (ch 23–25)
- [ ] Phase 2 · Scale & Performance (ch 26–32)
- [ ] Phase 3 · The Memory Wall (ch 33–35)
- [ ] Phase 3 · The Register Physics (ch 36–39)
- [ ] Phase 3 · Register Spilling (ch 40–42)
- [ ] Phase 3 · Global Memory & Coalescing (ch 43–45)
- [ ] Phase 3 · Shared Memory & Tiling (ch 46–48)
- [ ] Phase 3 · GEMM & The Synthesis (ch 49–52)
- [ ] Phase 4 · The Measurement Mandate (ch 53–56)
