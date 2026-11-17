title:: MoE Expert Offloading Bench: SSD → RAM → GPU
type:: project
state:: collected
ingested:: [[2026-11-18]]
my-priority:: now
note:: Next up. Hack project: a repeatable benchmark for running a big MoE (target DeepSeek V4 Flash, 284B/13B active) from NVMe by streaming expert chunks SSD → RAM → GPU, then tinker with expert selection, caching and prefetch to raise tok/s. Start CPU-only on the Linux laptop (6c/12t AMD, 16 GB dual-channel DDR4-2666, Gen3 NVMe 250 GB) with a stand-in model; buy the GPU later (most VRAM with working software, ideally 24 GB).
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: advanced
size:: deep-dive
concepts:: [[Mixture of Experts]], [[Expert Offloading]], [[Expert Caching]], [[Expert Prefetching]], [[Memory Hierarchy]], [[GPU Memory Bandwidth]], [[Quantization]], [[Containers]]
prerequisites:: [[Mixture of Experts]], [[Linux Basics]], [[Memory Management Concepts]]
planned:: 2026-11

## Summary
A personal benchmark harness for running a large MoE model (DeepSeek V4 Flash: 284B total, 13B active, ~150 GB at 4-bit) from NVMe on consumer hardware, streaming routed experts SSD → RAM → GPU. Decoding is SSD-bound (about 6.5 GB of weights per token, ~1 tok/s on a 3-6 GB/s drive), so the game is cutting SSD reads with pinning, caching, prefetching and layout. It starts CPU-only on a 16 GB laptop with a stand-in model at the same model-to-RAM ratio, in a pinned Podman image, with a trace-replay simulator for fast policy experiments.

## Key Takeaways
- Token generation is bound by bytes read from SSD per token, not GPU compute; RAM and SSD set the ceiling and can be upgraded later, the GPU's VRAM can't
- Pin always-used weights (attention, shared experts, router, embeddings); only routed experts move
- Cache by frequency and recency, pre-warm from domain profiles, and prefetch by running the next layer's router on the current hidden state
- Store each expert contiguously so a load is one sequential read; batch or speculative decoding amortizes each read over several tokens
- Prefill streams the whole model once (~30-60 s at 150 GB) regardless of prompt length
- Make the benchmark trustworthy: fixed prompts, greedy decoding, cold and warm runs, median of 3, identical output for lossless policies; record a router trace and replay it in a simulator to test policies in seconds

## Checklist
- [ ] Measure the laptop's real SSD read speed with fio (1–4 MB reads) and record kernel, filesystem, I/O scheduler, CPU governor
- [ ] Podman bench image: pinned llama.cpp commit, quant checksums, run_bench.sh, config/laptop.yaml, mounted results/ (model on a host bind mount)
- [ ] Fixed workload: 20–50 prompts across domains, greedy, fixed seed and output length; never change it
- [ ] Baseline: gpt-oss-120b (or Qwen3-Next-80B-A3B) on llama.cpp mmap, CPU-only, 6 threads, cold and warm, median of 3
- [ ] Log per run: tok/s, time to first token, SSD bytes per token, RAM hit rate, SSD MB/s, CPU clock/temperature
- [ ] Record a router trace and measure token-to-token expert reuse, popularity skew, and how well the previous layer predicts the next
- [ ] Trace-replay simulator for cache and prefetch policies, calibrated to the measured SSD speed
- [ ] Pin always-used weights (attention, shared experts, router, embeddings)
- [ ] Frequency vs recency cache policy, then pre-warm from a workload profile
- [ ] Prefetch next layer's experts by running its router on the current hidden state
- [ ] SSD layout: each expert contiguous, co-firing experts placed together
- [ ] Amortize reads: batching or speculative decoding
- [ ] Lossy tricks with quality checks: low-bit cold experts, cache-aware routing
- [ ] Choose the GPU: most VRAM (ideally 24 GB) with confirmed V4 kernel support; check case, PSU and slot
- [ ] Scale up to DeepSeek V4 Flash with the same config-driven bench

## Notes
Back-of-envelope estimates from the planning chat (not benchmarks). V4 Flash at 4-bit is ~150 GB with ~6.5 GB read per token: SSD-only ~0.5–0.8 tok/s, good cache hits ~1–2 tok/s, all tricks together maybe 2–3 tok/s. Prefill is one full model read (~30–60 s). Laptop stand-in: gpt-oss-120b (~60 GB, ~2.5 GB/token) ~0.7–1.5 tok/s warm; Qwen3-Next-80B-A3B ~1.5–3 tok/s. Usable page cache ~11–13 GB. Podman tricks: --memory to fake a smaller RAM and --device-read-bps to fake a slower SSD; validate both against real runs. Drop caches on the host before cold runs. Check whether mainline llama.cpp supports V4 (PR 24162) and the real V4 quant sizes before buying storage.
