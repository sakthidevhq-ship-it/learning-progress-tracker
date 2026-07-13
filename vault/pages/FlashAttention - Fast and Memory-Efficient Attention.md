title:: FlashAttention - Fast and Memory-Efficient Attention
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Model Architecture]]
engagement:: read
status:: in-progress
progress:: 40
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[Attention Mechanisms]], [[GPU Computing Basics]], [[Transformer Architecture]]
concepts:: [[IO-Aware Algorithms]], [[GPU Memory Hierarchy]], [[Attention Tiling]], [[SRAM vs HBM]], [[Kernel Fusion]]
tags:: flash-attention, optimization
source:: https://arxiv.org/abs/2205.14135
ingested:: [[2026-07-08]]
priority:: 37

## Summary
Introduces FlashAttention, an IO-aware exact attention algorithm that reduces memory usage from quadratic to linear while being 2-4x faster than standard attention. Achieves this by tiling the attention computation to avoid materializing the full N×N attention matrix in GPU HBM, instead keeping working data in fast SRAM.

## Key Takeaways
- Standard attention is memory-bound, not compute-bound — IO is the bottleneck
- Tiling attention into blocks that fit in SRAM avoids slow HBM reads/writes
- Exact computation — no approximation — while using O(N) memory instead of O(N²)

## Prerequisites
- [[Attention Mechanisms]]
- [[GPU Computing Basics]]
- [[Transformer Architecture]]

## My Notes
