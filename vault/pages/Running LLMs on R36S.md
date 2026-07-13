title:: Running LLMs on R36S
type:: docs
domain:: [[Embedded/Gaming]]
topic:: [[Edge AI]]
engagement:: implement
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: docs
prerequisites:: [[LLM Basics]], [[Linux Embedded Systems]], [[ARM Architecture]], [[KV Cache]]
concepts:: [[Cross-Compilation]], [[Model Quantization]], [[llama.cpp]], [[ARM NEON]], [[Edge Inference]]
tags:: r36s, llm, edge
source:: https://r36s-llm-experiments
ingested:: [[2026-07-09]]
priority:: 25

## Summary
Experimenting with running small language models on the R36S handheld (Allwinner H700, 1GB RAM). Explores llama.cpp cross-compilation for ARM, model quantization to fit in memory, and practical limitations of edge inference on ultra-low-power devices.

## Key Takeaways
- 4-bit quantization is minimum viable for 1GB RAM devices
- llama.cpp ARM NEON support enables surprisingly usable 1B parameter models
- KV cache management is the primary bottleneck on memory-constrained devices

## Prerequisites
- [[LLM Basics]]
- [[Linux Embedded Systems]]
- [[ARM Architecture]]
- [[KV Cache]]

## My Notes
