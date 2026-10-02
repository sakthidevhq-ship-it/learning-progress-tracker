title:: Kernel ladder: vector add to flash attention
type:: practice
state:: collected
ingested:: [[2026-10-03]]
note:: Benchmark each one against the torch baseline and profile it.
domain:: [[ML/Infrastructure]]
topic:: [[GPU Kernels]]
complexity:: intermediate
size:: deep-dive
concepts:: [[Triton]], [[Attention Mechanisms]]
prerequisites:: [[GPU Computing Basics]]

## Summary
Write a ladder of kernels of increasing difficulty, each benchmarked against PyTorch and profiled with Nsight Compute. Flash attention at the top is the rite of passage.

## Checklist
- [ ] Vector add
- [ ] Reduction
- [ ] Fused softmax
- [ ] RMSNorm
- [ ] Tiled GEMM
- [ ] Flash attention
