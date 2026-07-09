title:: vLLM - Efficient LLM Serving
type:: docs
domain:: [[ML/Infrastructure]]
topic:: [[LLM Serving]]
engagement:: read
status:: in-progress
progress:: 20
complexity:: intermediate
size:: deep-dive
medium:: docs
prerequisites:: [[Transformer Architecture]], [[KV Cache]], [[GPU Computing Basics]]
concepts:: [[PagedAttention]], [[Continuous Batching]], [[Speculative Decoding]], [[Prefix Caching]], [[Tensor Parallelism]], [[Pipeline Parallelism]]
tags:: vllm, serving
source:: https://docs.vllm.ai/en/latest/
ingested:: [[2026-07-08]]
priority:: 42

## Summary
Documentation and architecture guide for vLLM, the high-throughput LLM serving engine. Covers PagedAttention (its core innovation), continuous batching, speculative decoding, prefix caching, multi-GPU support via tensor/pipeline parallelism, and integration with HuggingFace models.

## Key Takeaways
- PagedAttention manages KV cache like virtual memory — non-contiguous physical blocks
- Speculative decoding uses a smaller draft model to speed up large model inference
- Prefix caching avoids recomputing shared prompt prefixes across requests

## Prerequisites
- [[Transformer Architecture]]
- [[KV Cache]]
- [[GPU Computing Basics]]

## My Notes
