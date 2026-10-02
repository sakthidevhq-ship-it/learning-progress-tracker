title:: Don't Quant the KV Cache — Local LLM Field Notes
type:: article
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
engagement:: background
complexity:: intermediate
size:: quick-read
medium:: article
prerequisites:: [[KV Cache]], [[Model Quantization]], [[Attention Mechanisms]]
concepts:: [[KV Cache Quantization]], [[Numerical Precision]], [[VRAM Budgeting]], [[Local Inference Tuning]]
tags:: kv-cache, quantization, local-llm, reddit
source:: https://www.reddit.com/r/LocalLLM/comments/1v9cnd9/thank_you_whoever_said_dont_quant_the_kv/
ingested:: [[2026-07-30]]
state:: collected

## Summary
r/LocalLLM community thread on why quantizing the KV cache degrades output quality far more than quantizing model weights. Practitioners report that aggressive KV cache quantization (q4/q8 cache flags in llama.cpp and similar) causes subtle coherence loss, repetition, and reasoning failures even when weight quantization is fine — because attention scores are numerically sensitive to cache precision. Practical guidance: spend your VRAM budget on cache precision before weight precision when quality matters.

## Key Takeaways
- Weight quantization and KV cache quantization fail differently — cache precision errors compound across every generated token
- Attention logits are sensitive to small cache perturbations; q4 cache can silently break long-context reasoning
- Practical VRAM triage: shrink weights (or context) before shrinking cache precision

## Prerequisites
- [[KV Cache]]
- [[Model Quantization]]
- [[Attention Mechanisms]]

## Notes
