title:: GPU kernels and inference: open-source roadmap
type:: project
state:: collected
ingested:: [[2026-10-03]]
note:: An alternate roadmap from earlier: open source first, academic route (part-time PhD / IISc M.Tech Research) second.
domain:: [[ML/Infrastructure]]
topic:: [[GPU Kernels]]
complexity:: advanced
size:: deep-dive
concepts:: [[Triton]], [[GPU Computing Basics]], [[Nsight Compute]], [[Continuous Batching]], [[PagedAttention]]
prerequisites:: [[Python]], [[GPU Computing Basics]]

## Summary
Path into inference and kernel work through open source: Triton before CUDA, PMPP and roofline foundations, a benchmarked kernel ladder up to flash attention, then contributions to CUTLASS/CuPy, vLLM and SGLang. Angle: real-time and streaming inference, plus the less crowded AMD side.

## Checklist
- [ ] Learn Triton (before CUDA C++)
- [ ] PMPP through the memory-hierarchy chapters, plus roofline thinking
- [ ] Get fluent with Nsight Compute: profile before changing anything
- [ ] Kernel ladder up to flash attention
- [ ] Join GPU MODE: lectures, leaderboard, reviews
- [ ] CUTLASS / CuPy good first issues
- [ ] vLLM, then SGLang
- [ ] Look at the AMD side (ROCm upstreaming in vLLM and SGLang)
- [ ] First PR: run their benchmarks, find a regression or unhandled shape, file an issue with numbers and a profile
- [ ] Push the niche: audio/streaming, TTFT and tail latency in these engines

## Notes
Good instinct on ordering — do the open source first and the academic route second, because in a part-time PhD or an IISc M.Tech (Research) the actual gate is a supervisor who wants you, and commits are the cheapest way to become that person.

Learn Triton before CUDA. This surprises people, but it's where the real work is now: Triton is the default kernel layer in PyTorch 2.x — torch.compile lowers to it by default, and vLLM's attention backends (PagedAttention, RoPE, RMSNorm) are all written in Triton, while SGLang uses it for RadixAttention. You get to the production frontier in Python instead of spending three months on C++ template errors first. Learn CUDA C++ later, when you hit something Triton can't express.

Foundations worth actually doing. Programming Massively Parallel Processors through the memory-hierarchy chapters, enough roofline thinking to reason about arithmetic intensity, and real fluency with Nsight Compute. The discipline that separates people who write kernels from people who optimize them is always profiling before changing anything.

The kernel ladder, each one benchmarked against the torch baseline and profiled: vector add → reduction → fused softmax → RMSNorm → tiled GEMM → flash attention. That last one is the rite of passage. GPU MODE is where this community lives — lectures, a kernel leaderboard, and people who'll review your work.

Repos, in ascending order of hostility to newcomers. CUTLASS and CuPy first — no ML theory required, active good first issue triage, and CUTLASS is the production version of the GEMM you just wrote. Then vLLM and SGLang. Useful context: the vLLM V1 redesign specifically made continuous batching, paged attention, speculative decoding, chunked prefill and prefix caching all compose properly, which changed things down at the kernel level — a lot of surface area is still being reworked.

Consider the AMD side. It's much less crowded than CUDA, AMD is actively upstreaming into both vLLM and SGLang, and vLLM V1 on Triton delivered 10% higher throughput on MI300X than the old custom C++/HIP path. Fewer contributors, faster recognition.

Your unfair advantage. Almost everyone optimizing inference is chasing throughput. You've spent two years on the other axis — time-to-first-token, tail latency, jitter, streaming under telephony constraints. Audio and streaming support in these engines is comparatively thin, and there are very few contributors who've actually run real-time speech inference against live traffic. That's a niche, not a queue.

How to land the first PR. Don't open with a new kernel. Run their benchmark suite on your hardware, find a regression or an unhandled shape, and file an issue with numbers and a profile. Maintainers respond to measurements. Fix that, then go bigger.

Hardware: rent, don't buy. An L4 or a 4090 on RunPod or Vast is plenty for kernel work — you don't need an H100 to learn occupancy.
