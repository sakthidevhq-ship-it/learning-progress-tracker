title:: Attention Is All You Need
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Model Architecture]]
engagement:: read
complexity:: intermediate
size:: medium
medium:: paper
prerequisites:: [[Linear Algebra Basics]], [[Neural Network Fundamentals]]
concepts:: [[Transformer Architecture]], [[Self-Attention]], [[Multi-Head Attention]], [[Positional Encoding]], [[Encoder-Decoder]]
tags:: transformers, foundational
source:: https://arxiv.org/abs/1706.03762
ingested:: [[2026-07-08]]
state:: picked
picked:: [[2026-10-25]]
planned:: 2026-10

## Summary
The foundational paper introducing the Transformer architecture. Proposes replacing recurrence and convolution entirely with self-attention mechanisms. Introduces multi-head attention, positional encoding, and the encoder-decoder structure that became the basis for GPT, BERT, and virtually all modern language models.

## Key Takeaways
- Self-attention allows modeling dependencies regardless of distance in the sequence
- Multi-head attention lets the model attend to different representation subspaces
- Parallelizable training — no sequential bottleneck like RNNs

## Prerequisites
- [[Linear Algebra Basics]]
- [[Neural Network Fundamentals]]

## Notes
2026-10-30: committed to sit down tonight (with Zero to Hero).

## Checklist
- [ ] Read §3 and redraw the architecture (encoder, decoder, attention blocks) from memory
- [ ] Implement scaled dot-product and multi-head attention from scratch in PyTorch, with a causal mask
- [ ] Show numerically why scores are scaled by √d_k (softmax saturation without it)
- [ ] Implement sinusoidal positional encoding and plot it
- [ ] Train a char-level decoder-only transformer on Tiny Shakespeare in a Kaggle notebook (free GPU) and sample text
- [ ] Ablate on Shakespeare: 1 vs 4 heads, with and without positional encoding; compare val loss
- [ ] Count parameters and FLOPs per token for your model
