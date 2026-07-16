title:: Matryoshka Representation Learning
type:: paper
domain:: [[ML/Foundations]]
topic:: [[Representation Learning]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[Neural Network Fundamentals]], [[Word Embeddings]], [[Linear Algebra Basics]]
concepts:: [[Matryoshka Embeddings]], [[Nested Representations]], [[Adaptive Retrieval]], [[Embedding Truncation]], [[Coarse-to-Fine Search]], [[Representation Learning]]
tags:: embeddings, matryoshka, retrieval
source:: https://arxiv.org/abs/2205.13147
ingested:: [[2026-07-16]]
priority:: 26

## Summary
Introduces Matryoshka Representation Learning (MRL): training embeddings so that nested prefixes of a single vector are themselves valid, high-quality representations at multiple granularities — like nesting dolls. One 2048-d embedding contains usable 8, 16, ... 1024-d embeddings, letting you trade accuracy for compute/storage at inference time without retraining. Powers adaptive retrieval (coarse shortlist with tiny prefixes, rerank with full vectors) and is used in production embedding APIs (e.g. OpenAI text-embedding-3 dimension truncation).

## Key Takeaways
- A single embedding can nest many smaller valid embeddings — train once, choose dimension at inference
- MRL loss simply supervises every prefix length simultaneously; negligible training overhead
- Adaptive retrieval with short prefixes + full-vector reranking gives ~14x real-world speedups at equal accuracy
- Connects directly to your compression=prediction notes: it's rate-distortion thinking applied to embedding dimensions

## Prerequisites
- [[Neural Network Fundamentals]]
- [[Word Embeddings]]
- [[Linear Algebra Basics]]

## My Notes
