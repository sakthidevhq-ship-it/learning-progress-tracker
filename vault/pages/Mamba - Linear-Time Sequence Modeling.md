title:: Mamba - Linear-Time Sequence Modeling
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Model Architecture]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[Transformer Architecture]], [[Linear Algebra Basics]], [[GPU Computing Basics]]
concepts:: [[State Space Models]], [[Selective Scan]], [[Linear Attention]], [[Hardware-Aware Design]], [[Sequence Modeling]]
tags:: mamba, ssm
source:: https://arxiv.org/abs/2402.17764
ingested:: [[2026-07-09]]
priority:: 37

## Summary
Introduces Mamba, a selective state space model that matches Transformer quality while scaling linearly with sequence length. Replaces attention with a hardware-aware selective scan algorithm. Shows strong results on language, audio, and genomics.

## Key Takeaways
- Selection mechanism lets SSMs focus on relevant input like attention does
- Linear-time complexity enables million-token context windows
- Hardware-aware scan algorithm achieves 5x faster training than Transformers on long sequences

## Prerequisites
- [[Transformer Architecture]]
- [[Linear Algebra Basics]]
- [[GPU Computing Basics]]

## My Notes
