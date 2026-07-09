title:: Compression = Prediction — Personal Notes
type:: docs
domain:: [[Systems]]
topic:: [[Compression]]
engagement:: background
status:: unread
progress:: 0
complexity:: intermediate
size:: quick-read
medium:: docs
prerequisites:: [[GPU Computing Basics]], [[Neural Network Fundamentals]]
concepts:: [[Information Theory]], [[Prediction-Compression Duality]], [[Multi-Algorithm Compression]], [[GPU Memory Bandwidth]], [[Quantization]], [[KV Cache]], [[Hardware Sparsity]]
tags:: compression, information-theory, personal-notes
source:: /private/tmp/compression-notes.md
ingested:: [[2026-07-09]]
priority:: 37

## Summary
Personal brainstorm connecting compression theory to LLMs and GPU architecture. Core insight: prediction and compression are mathematically equivalent — better prediction means fewer bits. Explores multi-algorithm compression (already used in HTTP, PNG, video codecs), how GPUs use the exact same per-block mode-selection pattern at hardware level for memory bandwidth, and how LLM inference optimizations (quantization, KV-cache compression, hardware sparsity) are all fundamentally 'send less data between memory and compute' tricks.

## Key Takeaways
- Training an LLM is finding the model that compresses training data best — prediction IS compression
- Multi-algorithm compression (send algo ID + compressed data) is used everywhere from HTTP to GPU hardware
- GPUs are bandwidth-bottlenecked, not compute-bottlenecked — all optimizations reduce data movement
- LLM quantization, KV-cache eviction, and 2:4 sparsity are all compression tricks for the memory-compute pipe

## Prerequisites
- [[GPU Computing Basics]]
- [[Neural Network Fundamentals]]

## My Notes
