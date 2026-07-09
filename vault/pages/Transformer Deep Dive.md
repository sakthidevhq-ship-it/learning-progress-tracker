title:: Transformer Deep Dive
type:: docs
domain:: [[ML/Infrastructure]]
topic:: [[Model Architecture]]
engagement:: implement
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: docs
prerequisites:: [[Transformer Architecture]], [[Attention Mechanisms]], [[Self-Attention]]
concepts:: [[Positional Encoding]], [[Multi-Head Attention]], [[Grouped Query Attention]], [[FlashAttention]], [[Transformer Architecture]]
tags:: transformers, positional-encoding, mha
source:: https://github.com/ml-curriculum/transformer-deep-dive
ingested:: [[2026-07-09]]
priority:: 39

## Summary
An in-depth curriculum module on modern Transformer internals: positional encoding schemes (RoPE, ALiBi), attention variants (MHA, MQA, GQA), FlashAttention, feed-forward network improvements, and how these pieces compose in production LLM architectures.

## Key Takeaways
- RoPE and ALiBi encode positional information relatively rather than absolutely, improving length generalization
- GQA and MQA trade some representational capacity for dramatically reduced KV cache size and faster inference
- FlashAttention reorders the attention computation to minimize HBM reads/writes rather than reducing FLOPs, yielding large real-world speedups

## Prerequisites
- [[Transformer Architecture]]
- [[Attention Mechanisms]]
- [[Self-Attention]]

## My Notes
