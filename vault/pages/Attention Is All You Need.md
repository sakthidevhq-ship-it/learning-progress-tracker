title:: Attention Is All You Need
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Model Architecture]]
engagement:: read
status:: completed
progress:: 100
complexity:: intermediate
size:: medium
medium:: paper
prerequisites:: [[Linear Algebra Basics]], [[Neural Network Fundamentals]]
concepts:: [[Transformer Architecture]], [[Self-Attention]], [[Multi-Head Attention]], [[Positional Encoding]], [[Encoder-Decoder]]
tags:: transformers, foundational
source:: https://arxiv.org/abs/1706.03762
ingested:: [[2026-07-08]]
priority:: 42

## Summary
The foundational paper introducing the Transformer architecture. Proposes replacing recurrence and convolution entirely with self-attention mechanisms. Introduces multi-head attention, positional encoding, and the encoder-decoder structure that became the basis for GPT, BERT, and virtually all modern language models.

## Key Takeaways
- Self-attention allows modeling dependencies regardless of distance in the sequence
- Multi-head attention lets the model attend to different representation subspaces
- Parallelizable training — no sequential bottleneck like RNNs

## Prerequisites
- [[Linear Algebra Basics]]
- [[Neural Network Fundamentals]]

## My Notes
