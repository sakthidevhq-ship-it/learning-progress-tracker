title:: Speculative Decoding for LLMs
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[Transformer Architecture]], [[KV Cache]], [[Attention Mechanisms]], [[Autoregressive Decoding]]
concepts:: [[Speculative Decoding]], [[Draft Model]], [[Token Verification]], [[Acceptance Rate]], [[Parallel Verification]]
tags:: speculative-decoding
source:: https://arxiv.org/abs/2305.18290
ingested:: [[2026-07-09]]
priority:: 41

## Summary
Technique to speed up LLM inference by using a small draft model to propose multiple tokens, then verifying them in parallel with the large model. Achieves 2-3x speedup with mathematically guaranteed identical output distribution.

## Key Takeaways
- Small draft model proposes tokens, large model verifies in one forward pass
- Output distribution is mathematically identical to standard decoding
- Speedup depends on acceptance rate — domain-matched drafts perform best

## Prerequisites
- [[Transformer Architecture]]
- [[KV Cache]]
- [[Attention Mechanisms]]
- [[Autoregressive Decoding]]

## My Notes
